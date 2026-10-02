from uuid import UUID

from app.domain.models import Case, CaseStatus, HumanDecision, Investigation
from app.domain.schemas import CaseCreate, HumanDecisionCreate


class InMemoryCaseStore:
    def __init__(self) -> None:
        self.cases: dict[UUID, Case] = {}
        self.investigations: dict[UUID, Investigation] = {}
        self.decisions: dict[UUID, HumanDecision] = {}

    def create_case(self, payload: CaseCreate) -> Case:
        case = Case(**payload.model_dump())
        self.cases[case.id] = case
        return case

    def get_case(self, case_id: UUID) -> Case | None:
        return self.cases.get(case_id)

    def add_investigation(self, investigation: Investigation) -> None:
        self.investigations[investigation.id] = investigation
        case = self.cases[investigation.case_id]
        case.status = CaseStatus.INVESTIGATING

    def add_decision(
        self,
        case_id: UUID,
        payload: HumanDecisionCreate,
    ) -> HumanDecision:
        decision = HumanDecision(case_id=case_id, **payload.model_dump())
        self.decisions[decision.id] = decision

        case = self.cases[case_id]
        case.status = CaseStatus.CLOSED
        return decision


case_store = InMemoryCaseStore()
