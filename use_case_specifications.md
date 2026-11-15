# Hostel maintenance use case specifications

## Actors and system boundary

- **Hostel Resident:** submits tickets for their assigned room, tracks their
  own history, and confirms closure of their own resolved tickets.
- **Maintenance Warden:** manages the queue, prioritizes and assigns staff,
  updates status, receives escalation alerts, and records closure overrides.
- **SMS/email Gateway:** supporting external service for queued escalation
  notifications. Successful gateway delivery is separate from queueing.

Maintenance workers are assignment targets; their direct system interaction
is not defined in the source requirements. SLA monitoring is an internal
automated behavior triggered by elapsed time.

## UC-01 Log Maintenance Ticket

**Primary actor:** Hostel Resident. **Requirement:** FR-001, FR-002.
**Goal:** Report a plumbing, electrical, or carpentry issue in the assigned
room. **Trigger:** The resident notices a maintenance issue.

**Preconditions:** The resident is authenticated, has an active room
assignment, and the ticketing service/network is available.

**Main success scenario:**

1. The resident selects Log Maintenance Ticket.
2. The system displays the form and assigned room number.
3. The resident selects category and severity, enters a description, confirms
   the geolocation tag, and optionally attaches a photo.
4. The resident submits the form.
5. The system includes UC-02 to validate required details, geolocation, and
   the resident's current room assignment.
6. The system creates one unique ticket ID, saves issue/location details and
   creation timestamp, and sets status to Reported.
7. The system places the ticket in the Warden queue and confirms submission.

**A1 Invalid details or wrong room:** At step 5, explain the invalid fields and
retain valid form entries. No ticket is created. The resident corrects the
details and resubmits.

**A2 Session/assignment no longer valid:** Recheck authorization at submission;
reject the request if the resident is no longer eligible. Do not rely only on
the room originally displayed on the form. This is a review clarification.

**E1 Save fails:** Do not confirm success or retain a partial ticket/queue
record. Explain that submission did not complete. Transactional saving is an
implementation requirement inferred from the success postcondition.

**Success postcondition:** One Reported ticket and corresponding Warden queue
entry exist with the source-required details. **Failure postcondition:** No
ticket is created; the resident receives actionable feedback.

## UC-02 Validate Ticket Details

Included by UC-01 on every submission. Validate category, severity,
description, room, and geolocation; ensure the room belongs to the
authenticated resident. Photos are optional. Return specific validation
errors without creating a ticket. On success, allow UC-01 to continue. Source
requirements: FR-001 and FR-002. No GPS radius or upload-size limit is supplied.

## UC-03 Track Own Ticket Status

The authenticated resident selects one of their own tickets. The system
checks ownership and shows current status plus timestamped chronological
history. Unknown or other residents' ticket IDs are denied without exposing
their contents or attachments. Postcondition: no state changes. Source:
FR-003 and NFR-002.

## UC-04 Manage Ticket Queue

The authenticated Warden views and filters the open-ticket queue. The system
checks role authorization and displays matching tickets. Empty results are
valid. Unauthorized requests are denied. Viewing a queue does not itself
assign work or reset the SLA clock. Source: FR-004 and NFR-002.

## UC-05 Prioritize and Assign Work

The Warden selects an open ticket, records priority, and assigns maintenance
staff. The system validates the request and persists the assignment with an
audit/history entry. The initial assignment changes Reported to Assigned.
Invalid staff/ticket references are rejected without partial updates. Staff
availability rules are not supplied. Source: FR-004 and NFR-002.

## UC-06 Update Ticket Status

The Warden selects an open ticket and a valid next status. The system checks
authorization and transition rules, saves a timestamped history/audit entry,
and makes the change visible to the resident. A transition to Resolved also
requests resident closure sign-off. Direct closure is not allowed through
this use case without UC-07 confirmation or UC-08 override. Source: FR-003,
FR-004, FR-005, and NFR-002.

## UC-07 Confirm and Close Own Ticket

After a sign-off request, the authenticated resident opens their own Resolved
ticket and confirms satisfactory resolution. The system rechecks ownership
and Resolved status, records confirmation/sign-off time, and changes the
ticket to Closed with a history entry. A wrong owner, non-Resolved status, or
missing confirmation prevents closure. Source: FR-005 and NFR-002.

## UC-08 Close with Warden Override

The authenticated Warden opens a Resolved ticket, supplies an override
reason, and confirms closure. The system requires the reason, records Warden
identity/time/reason in audit history, and sets Closed. Missing reasons or
non-Resolved tickets are rejected. Source: FR-005 and NFR-002.

## UC-09 Monitor SLA

Internal timed behavior checks eligible open high-priority tickets. The
inactivity clock is creation time until the first status change, then the
latest status-change time. At elapsed time >= 24 hours, UC-10 conditionally
extends monitoring. Comments/views do not reset the clock. Resolved/Closed
exclusion is an explicit design assumption. Source: NFR-001.

## UC-10 Queue Escalation Alert

**Extension point:** eligible inactivity breach detected in UC-09.
**Condition:** high priority, open status, at least 24 hours without a status
change, and no alert yet queued for this episode. Create one SMS/email alert
for the Warden within 5 minutes of breach and log the queue event. Repeated
checks must not duplicate the same episode's alert. A status change starts a
new episode. Queue failure is recorded and retried without duplicating a
successful enqueue. External delivery is not required to finish within that
5-minute queueing target. Source: NFR-001.

## State rules and cross-cutting constraints

The initial state is **Reported**. The design's normal progression is
Reported -> Assigned -> In Progress -> Resolved -> Closed. The intermediate
transition ordering is a design clarification, since the source lists states
without a complete transition table. Resolved -> Closed requires resident
confirmation or a documented Warden override. No automatic closure, reopen,
or skip-transition policy is invented.

Residents are restricted to their own tickets and attachments. Warden actions
are audit logged. Server-side authorization must be checked for each request.
The SLA acceptance scenario uses 100 overdue high-priority tickets under
simulated peak load; these are specification targets, not executed results.
