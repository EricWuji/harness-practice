from dataclasses import dataclass
from typing import Literal


PriorityLevel = Literal["P1", "P2", "P3", "P4"]


@dataclass(frozen=True)
class CustomerTicket:
    channel: str
    subject: str
    description: str
    category: str = "other"
    affected_customers: int = 0
    is_vip_customer: bool = False
    sla_minutes_remaining: int | None = None
    business_blocked: bool = False
    data_loss_risk: bool = False
    security_risk: bool = False
    service_unavailable: bool = False
    payment_blocked: bool = False


@dataclass(frozen=True)
class PriorityReason:
    code: str
    points: int
    explanation: str


@dataclass(frozen=True)
class PriorityAssessment:
    priority: PriorityLevel
    score: int
    reasons: tuple[PriorityReason, ...]
    explanations: tuple[str, ...]

    @property
    def reason_codes(self) -> tuple[str, ...]:
        return tuple(reason.code for reason in self.reasons)
