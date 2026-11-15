# Review and scope

## Source basis

This submission is based on the three files already present at commit
`5244633b311e4cb879bc8326ee5fbbed39e81b71`: the requirements table, the UC-01
flow specification, and the photographed UML diagram. No Lab 1 handout or
grading rubric was supplied. Consequently the work is checked against the
repository materials, not claimed to satisfy an unseen rubric.

The original Word documents and diagram are preserved byte-for-byte in
`originals/`. `requirements.json` transcribes their five functional and two
non-functional requirements. No new source requirement IDs were invented.

## Corrections and additions

1. The UML photograph names the staff actor Maintenance Worker, while FR-004
   and UC-01 give queue, assignment, and update authority to the Maintenance
   Warden. The digital diagram uses Maintenance Warden. Workers receive work
   assignments; a worker login or self-update workflow is not specified.
2. Add an explicit system boundary. Human and external service actors are
   outside it; use cases are inside it.
3. Use a dashed, open-arrow `<<include>>` from Log Maintenance Ticket to
   Validate Ticket Details, because validation is mandatory before creation.
4. Show queue viewing/filtering and assignment as separate Warden goals.
   Assigning work is not incorrectly shown as an include directed at an actor
   or as a mandatory step of every queue view.
5. Use a conditional `<<extend>>` from Queue Escalation Alert to Monitor SLA.
   The arrow points to the base monitoring use case. The condition is an
   eligible high-priority ticket reaching 24 hours with no status change.
6. Represent resident confirmation and documented Warden override as separate
   closure paths. Both require a Resolved ticket; there is no unconditional
   Resolved-to-Closed transition.
7. Link every source requirement to use cases and reviewable acceptance
   scenarios. These are specifications, not executed test results.
8. Define the SLA clock and duplicate handling as explicit design
   clarifications rather than silently changing the original requirements.

## Design clarifications requiring domain confirmation

- The SLA applies to open high-priority tickets (Reported, Assigned, In
  Progress). Resolved and Closed tickets stop escalation. The source does not
  explicitly specify terminal-state eligibility; this is a stated assumption.
- The clock starts at creation and resets on a status change, not on comments
  or viewing. At elapsed time >= 24 hours an eligible episode breaches.
- Queue exactly one alert per ticket/status-inactivity episode. A subsequent
  status change starts a new episode. Queueing must finish within 5 minutes
  of breach. Gateway delivery time is not guaranteed by this requirement.
- A resolution requests closure sign-off. Resident confirmation closes their
  own resolved ticket; a Warden can close it with an auditable reason. No
  automatic timeout or reopen workflow is specified.
- The room tag is the authoritative assigned-room reference. A geolocation
  tag is required by the source flow, but no radius/GPS accuracy threshold is
  supplied; such a threshold is not invented.
- Authentication is a precondition, not a mandatory `include` of every use
  case. RBAC and ownership checks still apply to every request, including
  attachment access. Photo upload is optional; no unsupported size limit is
  added.
- Maintenance workers are assignment targets in this scope. The SMS/email
  gateway is a supporting external service; monitoring is an internal timed
  behavior, so no human actor is associated with Monitor SLA.

## What was verified

The written requirements, flow, digital UML, state rules, and traceability were
reviewed for consistent roles, identifiers, and conditions. The final PDF and
diagram were rendered and visually inspected. No application, authentication
service, notification gateway, performance simulation, or security test has
been implemented or executed as part of this documentation assignment.
