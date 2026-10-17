# Non-functional requirements catalog

Non-functional requirements are rarely volunteered, because they feel like background
assumptions to the person asking. They surface late, usually during a security review or an
incident, when changing them is expensive. Walk this list and ask about the categories that
plausibly apply — skip the ones that clearly do not rather than padding the document.

Each entry below shows the question to ask and what a usable answer looks like. A category
with no number or named standard attached is not yet a requirement.

## Performance
- Expected and peak request volume; response time target and where it is measured.
- Batch or job completion windows.
- Usable: "95th percentile page load under 2s at 500 concurrent users."

## Availability and reliability
- Uptime expectation and whether planned maintenance counts against it.
- Acceptable data loss (RPO) and recovery time (RTO) after a failure.
- Degraded-mode behavior: what still works when a dependency is down?

## Scalability
- Growth expected over the next 12–24 months, in users, records, or throughput.
- Whether growth is steady or spiky, and what drives the spikes.

## Security
- Authentication method and who issues identities.
- Authorization model: which roles exist and what each can do.
- Data classification, encryption expectations at rest and in transit.
- Secrets handling, key rotation, and audit logging of sensitive actions.

## Privacy and compliance
- Personal, financial, or health data involved; applicable regimes (GDPR, HIPAA, PCI, SOC 2).
- Retention period and deletion process, including backups.
- Data residency limits and any cross-border transfer constraints.
- Consent and subject-access obligations.

## Accessibility
- Standard to meet (commonly WCAG 2.1 AA) and whether it is contractual.
- Keyboard-only operation, screen reader support, contrast and text sizing.

## Usability
- Expected proficiency of users and tolerance for training.
- Error message expectations and language or tone standards.

## Observability and support
- What must be logged, metered, and alerted on, and who receives alerts.
- How a support agent diagnoses a user-reported problem.
- Audit trail requirements: who did what, when, retained how long.

## Maintainability and operability
- Deployment frequency and rollback expectations.
- Configuration vs. code: what must be changeable without a release.
- Documentation and runbook expectations at handover.

## Interoperability and portability
- Systems that must integrate, and the contract each expects.
- Export formats and any obligation to avoid vendor lock-in.

## Cost
- Budget ceiling for infrastructure or licensing, and who owns that budget.
- Cost per transaction or per user limits, if any.

## Legal and contractual
- SLAs promised to customers that this work inherits.
- Licensing constraints on dependencies.
- Record-keeping obligations.

---

When an answer is "we don't know yet", record it as an open question with an owner rather
than inventing a target. An invented number in a spec gets implemented as if it were real.
