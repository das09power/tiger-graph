import os
import datetime
import requests
from typing import List, Optional, Dict, Any

# Environment configuration for TigerGraph Cloud (if connected)
TIGERGRAPH_HOST = os.getenv("TIGERGRAPH_HOST", "https://dl.tigergraph.com")
TIGERGRAPH_GRAPH_NAME = os.getenv("TIGERGRAPH_GRAPH_NAME", "FraudSentinelGraph")
TIGERGRAPH_API_TOKEN = os.getenv("TIGERGRAPH_API_TOKEN", "")

class FraudDatabase:
    def __init__(self):
        self.cases: List[Dict[str, Any]] = []
        self._initialize_benchmark_data()

    def _initialize_benchmark_data(self):
        """Populates initial benchmark fraud cases representing IEEE-CIS patterns."""
        base_case = {
            "id": "case-1",
            "caseNum": 1,
            "txnId": "2983411",
            "cardId": "4916-XXXX-1029",
            "amount": 2840.00,
            "riskScore": 0.94,
            "typology": "ATO",
            "status": "UNRESOLVED",
            "evidenceGathered": False,
            "timestamp": "2026-08-14 14:22:09 UTC",
            "device": "iOS 17.4 / iPhone 15 Pro",
            "ipGeo": "185.220.101.4 (TOR Exit / Germany)",
            "productCode": "W (Web Payment)",
            "emailDomain": "temp-mail.org",
            "geoDistance": "4,820 miles",
            "velocity24h": "14 txns / 3 cards",
            "policyFlags": [
                {"rule": "POL-ATO-01", "text": "Device ID mismatch with customer baseline (New OS)"},
                {"rule": "POL-GEO-04", "text": "Impossible travel velocity (>500 mph between txns)"},
                {"rule": "POL-NET-02", "text": "Known anonymizing VPN / TOR exit node IP address"}
            ],
            "graphData": {
                "nodes": [
                    {"id": "T1", "label": "Txn #2983411", "type": "txn", "color": "#f97316"},
                    {"id": "C1", "label": "Card 4916..1029", "type": "card", "color": "#c084fc"},
                    {"id": "D1", "label": "iOS iPhone 15", "type": "device", "color": "#38bdf8"},
                    {"id": "IP1", "label": "185.220.101.4", "type": "ip", "color": "#38bdf8"},
                    {"id": "P1", "label": "Prior Case #842", "type": "prior", "color": "#ef4444"},
                    {"id": "POL1", "label": "Policy ATO-01", "type": "policy", "color": "#22c55e"}
                ],
                "links": [
                    {"source": "T1", "target": "C1", "label": "USED_CARD"},
                    {"source": "T1", "target": "D1", "label": "ORIGINATED_FROM"},
                    {"source": "D1", "target": "IP1", "label": "CONNECTED_VIA"},
                    {"source": "IP1", "target": "P1", "label": "MATCHES_IP"},
                    {"source": "T1", "target": "POL1", "label": "VIOLATES"}
                ]
            },
            "priorCases": [
                {"id": "Case #842", "similarity": 0.93, "outcome": "CONFIRMED_FRAUD", "note": "Account takeover via TOR IP. Credentials compromised in breach."},
                {"id": "Case #619", "similarity": 0.88, "outcome": "CONFIRMED_FRAUD", "note": "Rapid carding attempt using temp-mail address."}
            ],
            "cotSteps": [
                {"step": 1, "title": "Trigger Evaluation", "text": "Transaction 2983411 flagged with high risk score (0.94) originating from TOR Exit IP."},
                {"step": 2, "title": "TigerGraph Traversal", "text": "GSQL traversed 2 hops. Found Device ID shared with 3 distinct card numbers in last 24 hours."},
                {"step": 3, "title": "Uncertainty & Evidence Requirement", "text": "High initial risk detected. Mismatch between location and cardholder residency requires Step-Up Auth."}
            ],
            "preNba": "Request Customer Step-Up Auth (SMS OTP) & Temporary Hold",
            "postNba": "PERMANENT BLOCK + FILE FINCEN SAR + CLOSE ACCOUNT",
            "approvalRoute": "L2 Senior Fraud Analyst Approval Required",
            "confidencePre": 85,
            "confidencePost": 96
        }
        self.cases.append(base_case)

        # Generate remaining dataset benchmark cases
        typologies = ["ATO", "CNP", "SYNTH", "FRIENDLY", "VELOCITY"]
        for i in range(2, 21):
            typ = typologies[i % len(typologies)]
            risk = round(0.65 + (i * 0.017) % 0.32, 2)
            self.cases.append({
                "id": f"case-{i}",
                "caseNum": i,
                "txnId": f"{2983410 + i}",
                "cardId": f"4111-XXXX-{1000 + i * 47}",
                "amount": round(150 + i * 230.5, 2),
                "riskScore": risk,
                "typology": typ,
                "status": "RESOLVED" if i % 3 == 0 else "UNRESOLVED",
                "evidenceGathered": False,
                "timestamp": f"2026-08-{10 + (i%5)} 10:{(i*3)%60}:{(i*7)%60} UTC",
                "device": "MacOS / Chrome 122" if i % 2 == 0 else "Windows 11 / Edge",
                "ipGeo": f"172.56.{i*2}.10 (Dallas, US)",
                "productCode": "W (Online)",
                "emailDomain": "yahoo.com",
                "geoDistance": f"{i * 120} miles",
                "velocity24h": f"{i % 6 + 2} txns",
                "policyFlags": [
                    {"rule": f"POL-{typ}-01", "text": f"Suspicious pattern violating {typ} risk thresholds."}
                ],
                "graphData": {
                    "nodes": [
                        {"id": f"T{i}", "label": f"Txn #{2983410 + i}", "type": "txn", "color": "#f97316"},
                        {"id": f"C{i}", "label": f"Card {1000 + i}", "type": "card", "color": "#c084fc"},
                        {"id": f"D{i}", "label": f"Device_{i}", "type": "device", "color": "#38bdf8"}
                    ],
                    "links": [
                        {"source": f"T{i}", "target": f"C{i}", "label": "USED_CARD"},
                        {"source": f"T{i}", "target": f"D{i}", "label": "USED_DEVICE"}
                    ]
                },
                "priorCases": [
                    {"id": f"Case #{500+i}", "similarity": 0.85, "outcome": "CONFIRMED_FRAUD", "note": "Matches historic velocity attack vector."}
                ],
                "cotSteps": [
                    {"step": 1, "title": "Trigger Signal", "text": f"High risk score {risk} flagged by graph pipeline."},
                    {"step": 2, "title": "Graph Traversal", "text": "2-hop traversal complete. Connected entities examined."}
                ],
                "preNba": "Request Additional Identity Telemetry",
                "postNba": "ENFORCE STEP-UP & ESCALATE TO ANALYST",
                "approvalRoute": "Analyst Review Required",
                "confidencePre": 70,
                "confidencePost": 91
            })

    def get_all_cases(self, typology: Optional[str] = None, status: Optional[str] = None, search: Optional[str] = None):
        results = self.cases
        if typology and typology != "ALL":
            results = [c for c in results if c["typology"] == typology]
        if status and status != "ALL":
            results = [c for c in results if c["status"] == status]
        if search:
            s = search.lower()
            results = [c for c in results if s in c["txnId"].lower() or s in c["cardId"].lower() or s in c["typology"].lower()]
        return results

    def get_case_by_id(self, case_id: str):
        return next((c for c in self.cases if c["id"] == case_id or str(c["caseNum"]) == case_id), None)

    def add_case(self, new_case: Dict[str, Any]):
        self.cases.insert(0, new_case)
        return new_case

# Singleton database instance
db = FraudDatabase()