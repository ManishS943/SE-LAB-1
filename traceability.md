# Requirements traceability and acceptance scenarios

All scenarios below are proposed acceptance checks, **not executed tests**.
The source contains five functional and two non-functional requirements.

| Source requirement | Use cases | Acceptance scenarios |
| --- | --- | --- |
| FR-001 | UC-01, UC-02 | AC-01, AC-02 |
| FR-002 | UC-02 | AC-03, AC-04 |
| FR-003 | UC-03, UC-06 | AC-05, AC-06 |
| FR-004 | UC-04, UC-05, UC-06 | AC-07, AC-08, AC-09 |
| FR-005 | UC-06, UC-07, UC-08 | AC-10, AC-11, AC-12 |
| NFR-001 | UC-09, UC-10 | AC-13, AC-14, AC-15 |
| NFR-002 | UC-01 through UC-08; access and audit controls | AC-16, AC-17, AC-18 |

| ID | Scenario | Expected result |
| --- | --- | --- |
| AC-01 | Authenticated resident submits valid assigned-room details, with or without a photo. | Exactly one unique Reported ticket, timestamp, details, and Warden queue entry; confirmation returned. |
| AC-02 | Submit a form missing a required category, severity, description, room, or geolocation. | Explain errors and retain valid fields; no ticket created. |
| AC-03 | Submit for the resident's current assigned room. | Server-side assignment validation succeeds and location tags are stored. |
| AC-04 | Submit another resident's room or an assignment that changed before submission. | Reject; no ticket or partial queue entry is created. |
| AC-05 | Resident opens their own ticket after several status updates. | Current status and every timestamped update appear in chronological order. |
| AC-06 | Resident requests another resident's ticket by manipulating its ID. | Deny access and reveal no ticket contents. |
| AC-07 | Warden filters the queue and selects an open ticket. | Correct matching entries appear; a no-match result is handled normally. |
| AC-08 | Warden assigns valid maintenance staff and saves priority. | Assignment and priority persist; the initial assignment is recorded in history/audit. |
| AC-09 | Warden saves a permitted status update. | Resident sees the persisted update; timestamp and Warden audit entry exist. |
| AC-10 | Warden marks a ticket Resolved. | Request resident sign-off; do not close automatically. |
| AC-11 | Owner confirms a Resolved ticket; repeat with wrong owner or non-Resolved status. | Valid confirmation records sign-off time and closes; invalid attempts do not close. |
| AC-12 | Warden closes a Resolved ticket with an override, then tries without a reason. | Valid override records reason/identity/time; missing reason prevents closure. |
| AC-13 | Simulate peak load with 100 eligible high-priority tickets at their 24-hour inactivity breach. | Every alert is queued to the Warden within 5 minutes and logged once. This is a target, not a measured result. |
| AC-14 | Run the SLA check repeatedly for one unchanged breach episode. | Exactly one successful queue event; no duplicate notification jobs. |
| AC-15 | Check a below-threshold, lower-priority, or resolved/closed ticket; then status-change an eligible ticket. | No ineligible alert; reset the clock after the status change. Terminal-state exclusion is an explicit clarification. |
| AC-16 | Unauthenticated caller or wrong-role user attempts ticket or Warden operations. | Deny unauthorized requests; do not mutate ticket data. |
| AC-17 | Resident manipulates an attachment URL/ID for another resident's ticket. | Deny access; no attachment contents exposed. |
| AC-18 | Warden performs assignment, status update, or override. | Retain an audit entry identifying action, actor, time, ticket, and override reason where applicable. |

Review coverage means every source requirement has a use-case link and at
least one acceptance scenario. It does not demonstrate security, performance,
or application correctness without an implementation and executed tests.
