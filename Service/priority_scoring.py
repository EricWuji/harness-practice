from Types.ticket import CustomerTicket, PriorityAssessment, PriorityLevel, PriorityReason


def score_ticket_priority(ticket: CustomerTicket) -> PriorityAssessment:
    if ticket.affected_customers < 0:
        raise ValueError("affected_customers cannot be negative")

    reasons: list[PriorityReason] = []

    def add_when(condition: bool, code: str, points: int, explanation: str) -> None:
        if condition:
            reasons.append(PriorityReason(code, points, explanation))

    add_when(ticket.security_risk, "security_risk", 100, "Security risk requires immediate P1 review.")
    add_when(ticket.data_loss_risk, "data_loss_risk", 100, "Data loss risk requires immediate P1 review.")
    add_when(ticket.service_unavailable, "service_unavailable", 90, "Service unavailable is treated as P1 impact.")
    add_when(ticket.business_blocked, "business_blocked", 40, "Customer business workflow is blocked.")
    add_when(ticket.payment_blocked, "payment_blocked", 25, "Payment or renewal is blocked.")
    add_when(ticket.is_vip_customer, "vip_customer", 20, "VIP customer signal raises urgency.")

    if ticket.affected_customers >= 100:
        reasons.append(PriorityReason("affected_100_plus", 45, "Incident affects at least 100 customers."))
    elif ticket.affected_customers >= 10:
        reasons.append(PriorityReason("affected_10_plus", 30, "Incident affects at least 10 customers."))
    elif ticket.affected_customers >= 2:
        reasons.append(PriorityReason("affected_multiple_customers", 15, "Incident affects multiple customers."))

    if ticket.sla_minutes_remaining is not None:
        if ticket.sla_minutes_remaining <= 30:
            reasons.append(PriorityReason("sla_under_30_minutes", 30, "SLA deadline is within 30 minutes."))
        elif ticket.sla_minutes_remaining <= 120:
            reasons.append(PriorityReason("sla_under_120_minutes", 15, "SLA deadline is within 120 minutes."))

    if not reasons:
        reasons.append(PriorityReason("no_urgent_signal", 0, "No urgent priority signal was detected."))

    score = sum(reason.points for reason in reasons)
    priority = _priority_for_score(score)
    explanations = tuple(reason.explanation for reason in reasons) + (
        f"Total score {score} maps to {priority}.",
    )

    return PriorityAssessment(
        priority=priority,
        score=score,
        reasons=tuple(reasons),
        explanations=explanations,
    )


def _priority_for_score(score: int) -> PriorityLevel:
    if score >= 90:
        return "P1"
    if score >= 60:
        return "P2"
    if score >= 30:
        return "P3"
    return "P4"
