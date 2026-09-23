from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import datetime
import os

from models import EvidenceRequest, ActionRequest, TriggerSimulationRequest
from database import db

app = FastAPI(
    title="TigerGraph Agentic Fraud Sentinel API",
    version="1.0.0",
    description="Backend API powering the HHGOA Hackathon Fraud Investigation Agent"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "system": "TigerGraph Agentic Fraud Sentinel Backend", "cases_loaded": len(db.cases)}

@app.get("/api/cases")
def get_cases(typology: Optional[str] = None, status: Optional[str] = None, search: Optional[str] = None):
    results = db.get_all_cases(typology=typology, status=status, search=search)
    return {"total": len(results), "cases": results}

@app.get("/api/cases/{case_id}")
def get_case_detail(case_id: str):
    case = db.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@app.post("/api/cases/{case_id}/evidence")
def gather_evidence(case_id: str, body: EvidenceRequest):
    case = db.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case["evidenceGathered"] = True
    case["confidencePost"] = 97
    return {"status": "success", "message": f"Evidence {body.evidenceType} gathered successfully.", "updatedCase": case}

@app.post("/api/cases/{case_id}/execute")
def execute_case_action(case_id: str, body: ActionRequest):
    case = db.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case["status"] = "RESOLVED"
    return {"status": "success", "actionExecuted": body.actionType, "case": case}

@app.post("/api/simulate")
def simulate_trigger(body: TriggerSimulationRequest):
    new_case_num = len(db.cases) + 1
    new_case = {
        "id": f"case-{new_case_num}",
        "caseNum": new_case_num,
        "txnId": body.txnId,
        "cardId": "5555-XXXX-9912",
        "amount": body.amount,
        "riskScore": 0.95,
        "typology": body.typology,
        "status": "UNRESOLVED",
        "evidenceGathered": False,
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "device": "Mobile Simulator / iOS 18",
        "ipGeo": "203.0.113.42 (High-Risk Proxy)",
        "productCode": "W",
        "emailDomain": "proton.me",
        "geoDistance": "3,100 miles",
        "velocity24h": "19 txns / 4 cards",
        "policyFlags": [
            {"rule": f"POL-{body.typology}-01", "text": f"Simulated high-risk trigger detected via {body.triggerType}."}
        ],
        "graphData": {
            "nodes": [
                {"id": "T_new", "label": f"Txn #{body.txnId}", "type": "txn", "color": "#f97316"},
                {"id": "C_new", "label": "Card 5555..9912", "type": "card", "color": "#c084fc"},
                {"id": "D_new", "label": "Proxy Device", "type": "device", "color": "#38bdf8"}
            ],
            "links": [
                {"source": "T_new", "target": "C_new", "label": "USED_CARD"},
                {"source": "T_new", "target": "D_new", "label": "ORIGINATED_FROM"}
            ]
        },
        "priorCases": [
            {"id": "Case #201", "similarity": 0.94, "outcome": "CONFIRMED_FRAUD", "note": "Similar proxy pattern detected in Q1 benchmark."}
        ],
        "cotSteps": [
            {"step": 1, "title": "Live Simulation Trigger", "text": f"Triggered via {body.triggerType} for transaction {body.txnId}."},
            {"step": 2, "title": "Graph Traversal", "text": "Graph RAG successfully queried TigerGraph RESTPP endpoints."}
        ],
        "preNba": "Request Step-Up Auth & Hold Funds",
        "postNba": "BLOCK CARD + FILE SAR",
        "approvalRoute": "L2 Senior Fraud Analyst Approval Required",
        "confidencePre": 78,
        "confidencePost": 95
    }
    
    added = db.add_case(new_case)
    return {"status": "success", "newCase": added}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)