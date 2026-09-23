# tiger-graph
# 🛡️ TigerGraph Agentic Fraud Sentinel

A real-time, AI-powered fraud detection dashboard and simulation engine built with **FastAPI**, **Pydantic**, **TigerGraph analytics concepts**, and **Tailwind CSS**.

---

## 📌 Overview

Financial fraud patterns are complex and interconnected. Traditional relational databases often fail to spot multi-hop suspicious relationships across accounts, devices, and transactions. 

The **TigerGraph Agentic Fraud Sentinel** bridges this gap by offering a decoupled full-stack architecture that visualizes high-risk benchmark fraud cases, runs automated agentic investigations, and provides live case simulation capabilities.

---

## ✨ Key Features

* **Real-time Case Dashboard**: View flagged benchmark fraud cases with dynamic risk scores and entity breakdowns.
* **Agentic Simulation Engine**: Trigger synthetic, high-risk graph fraud scenarios on the fly via backend API endpoints.
* **Interactive Visualizations**: Powered by **Chart.js** for immediate insights into risk distributions and transaction threats.
* **Incident Response Actions**: Execute direct account actions (e.g., account freeze, investigation trigger) with instant state feedback.
* **Decoupled Architecture**: Clean separation between the FastAPI REST backend and the lightweight frontend UI.

---

## 🛠️ Tech Stack

### **Backend**
* **Language:** Python 3.10+
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)
* **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/)

### **Frontend**
* **Markup/Styling:** HTML5, [Tailwind CSS](https://tailwindcss.com/)
* **Charts/Visuals:** [Chart.js](https://www.chartjs.org/)
* **Scripting:** Vanilla JavaScript (Fetch API)

---

## 📁 Project Structure

```text
tigergraph/
├── main.py          # FastAPI server entry point & API endpoints
├── database.py      # Mock dataset & graph benchmark cases
├── models.py        # Pydantic models for request/response validation
├── requirements.txt # Python dependency list
├── index.html       # Frontend dashboard UI
└── .env             # Environment configuration file
