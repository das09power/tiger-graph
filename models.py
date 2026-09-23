from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class EvidenceRequest(BaseModel):
    evidenceType: str

class ActionRequest(BaseModel):
    actionType: str

class TriggerSimulationRequest(BaseModel):
    triggerType: str
    txnId: str
    amount: float
    typology: str

class PolicyFlag(BaseModel):
    rule: str
    text: str

class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    color: str

class GraphLink(BaseModel):
    source: str
    target: str
    label: Optional[str] = None

class GraphData(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]

class PriorCase(BaseModel):
    id: str
    similarity: float
    outcome: str
    note: str

class CotStep(BaseModel):
    step: int
    title: str
    text: str

class FraudCase(BaseModel):
    id: str
    caseNum: int
    txnId: str
    cardId: str
    amount: float
    riskScore: float
    typology: str
    status: str
    evidenceGathered: bool
    timestamp: str
    device: str
    ipGeo: str
    productCode: str
    emailDomain: str
    geoDistance: str
    velocity24h: str
    policyFlags: List[PolicyFlag]
    graphData: GraphData
    priorCases: List[PriorCase]
    cotSteps: List[CotStep]
    preNba: str
    postNba: str
    approvalRoute: str
    confidencePre: int
    confidencePost: int