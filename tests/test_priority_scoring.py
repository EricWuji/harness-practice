import unittest

from Service.priority_scoring import score_ticket_priority
from Types.ticket import CustomerTicket


class PriorityScoringTests(unittest.TestCase):
    def test_scores_p1_for_security_or_data_loss_risk_with_explanations(self):
        ticket = CustomerTicket(
            channel="email",
            subject="Customer data export exposed",
            description="Users can download other customers' invoices.",
            security_risk=True,
            data_loss_risk=True,
            affected_customers=3,
        )

        assessment = score_ticket_priority(ticket)

        self.assertEqual("P1", assessment.priority)
        self.assertGreaterEqual(assessment.score, 90)
        self.assertIn("security_risk", assessment.reason_codes)
        self.assertIn("data_loss_risk", assessment.reason_codes)
        self.assertTrue(any("P1" in reason for reason in assessment.explanations))

    def test_scores_p2_for_vip_payment_issue_near_sla(self):
        ticket = CustomerTicket(
            channel="form",
            subject="VIP cannot renew subscription",
            description="The payment page fails and renewal SLA is close.",
            category="billing",
            is_vip_customer=True,
            payment_blocked=True,
            sla_minutes_remaining=45,
        )

        assessment = score_ticket_priority(ticket)

        self.assertEqual("P2", assessment.priority)
        self.assertIn("vip_customer", assessment.reason_codes)
        self.assertIn("payment_blocked", assessment.reason_codes)
        self.assertIn("sla_under_120_minutes", assessment.reason_codes)

    def test_scores_p3_for_single_customer_business_blocker(self):
        ticket = CustomerTicket(
            channel="im",
            subject="Cannot submit daily report",
            description="A single customer cannot complete a required workflow.",
            business_blocked=True,
            affected_customers=1,
        )

        assessment = score_ticket_priority(ticket)

        self.assertEqual("P3", assessment.priority)
        self.assertIn("business_blocked", assessment.reason_codes)

    def test_scores_p4_for_general_question_without_urgent_signals(self):
        ticket = CustomerTicket(
            channel="email",
            subject="Question about invoice fields",
            description="Customer asks what a field on the invoice means.",
            category="consulting",
        )

        assessment = score_ticket_priority(ticket)

        self.assertEqual("P4", assessment.priority)
        self.assertIn("no_urgent_signal", assessment.reason_codes)

    def test_rejects_negative_affected_customer_count(self):
        ticket = CustomerTicket(
            channel="form",
            subject="Invalid imported metric",
            description="The parser produced an impossible impact count.",
            affected_customers=-1,
        )

        with self.assertRaises(ValueError):
            score_ticket_priority(ticket)


if __name__ == "__main__":
    unittest.main()
