# AI Powered Workforce Performance Prediction & Intelligence Platform

An enterprise-grade AI-powered workforce analytics platform that combines **Machine Learning**, **Retrieval-Augmented Generation (RAG)**, **Explainable AI (XAI)**, and **Human-in-the-Loop (HITL)** decision intelligence to predict employee performance and generate contextual, policy-grounded recommendations.

> Developed as an MCA (Artificial Intelligence) Major Project.

---

# Project Overview

Traditional employee performance evaluations are often manual, subjective, and reactive. This platform transforms workforce analytics into a predictive and explainable AI system by integrating data engineering, machine learning, enterprise security, and Generative AI.

The application enables HR teams, managers, and leadership to:

- Predict employee performance
- Analyze workforce trends
- Generate AI-powered recommendations
- Review AI decisions before approval
- Maintain enterprise-grade security with Role-Based Access Control (RBAC)

---

# Key Features

- Workforce Analytics Dashboard
- Employee Performance Prediction
- Explainable AI Recommendations
- Retrieval-Augmented Generation (RAG)
- Human-in-the-Loop (HITL) Decision Review
- Role-Based Access Control (RBAC)
- Machine Learning Model Benchmarking
- Feature Importance Analysis
- Automated Report Generation
- Automated Testing & Code Coverage

---

# System Architecture

```text
                      MySQL Database
                             │
                             ▼
                     ETL Data Pipeline
                             │
                             ▼
                 DuckDB Analytical Warehouse
                             │
                             ▼
                  Feature Engineering Layer
                             │
                             ▼
             Machine Learning Model Training
                             │
                             ▼
                 Employee Performance Prediction
                             │
               ┌─────────────┴─────────────┐
               ▼                           ▼
      Workforce Analytics           AI Recommendation
                                         │
                                         ▼
                          Retrieval-Augmented Generation
                               (FAISS + LangChain)
                                         │
                                         ▼
                              Ollama Local LLM
                                         │
                                         ▼
                       Explainable Recommendation
                                         │
                                         ▼
                         Human-in-the-Loop Review
                                         │
                                         ▼
                             Streamlit Web Application
```

---

# Project Structure

```text
workforce-performance-prediction/
│
├── app/
│   ├── main.py
│   ├── login.py
│   └── pages/
│       ├── Analytics Dashboard
│       ├── Prediction Dashboard
│       ├── Human Review
│       └── Developer Quality Dashboard
│
├── src/
│   ├── ai/
│   ├── config/
│   ├── database/
│   ├── evaluation/
│   ├── features/
│   ├── hitl/
│   ├── inference/
│   ├── models/
│   ├── pipeline/
│   ├── security/
│   ├── training/
│   └── validation/
│
├── knowledge_base/
├── models/
├── data/
├── reports/
├── tests/
└── README.md
```

---

# Technology Stack

## Backend

- Python
- SQLAlchemy
- PyMySQL
- Pandas
- NumPy

## Database

- MySQL
- DuckDB

## Machine Learning

- Scikit-learn
- XGBoost

## AI & Generative AI

- LangChain
- FAISS
- Ollama
- Phi-3

## Frontend

- Streamlit
- Plotly

## Testing

- Pytest
- Coverage.py

---

# Workflow

1. Extract workforce data from MySQL.
2. Validate database schema.
3. Transform and engineer features.
4. Build analytical warehouse in DuckDB.
5. Train multiple regression models.
6. Select the best-performing model.
7. Predict employee performance.
8. Retrieve HR policies using RAG.
9. Generate explainable AI recommendations.
10. Manager reviews recommendations through HITL.
11. Display insights in Streamlit dashboards.

---

# Machine Learning Models

The platform benchmarks multiple regression algorithms:

- Linear Regression
- Ridge Regression
- Lasso Regression
- ElasticNet Regression
- Decision Tree Regressor
- Random Forest Regressor
- XGBoost Regressor

Evaluation Metrics:

- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score (Coefficient of Determination)
- Cross Validation

---

# AI Capabilities

The AI layer combines:

- Local Large Language Models (Ollama)
- LangChain orchestration
- FAISS vector database
- Enterprise HR knowledge base

to produce explainable recommendations instead of black-box predictions.

---

# Security

The platform includes:

- User Authentication
- Role-Based Access Control (RBAC)
- Session Management
- Authorization Layer
- Row-Level Data Access

Supported Roles:

- Administrator
- HR
- Leadership
- Manager

---

# Testing

Automated testing covers:

- Authentication
- Session Management
- Authorization
- Database Validation
- Model Training
- Prediction Pipeline
- Feature Engineering

Run tests:

```bash
pytest
```

Generate coverage:

```bash
pytest --cov=src
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/christykiran-p/workforce-performance-prediction.git
cd workforce-performance-prediction
```

Install dependencies:

```bash
uv sync
```

or

```bash
pip install -r ai_requirements.txt
```

Create a `.env` file:

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

OPENAI_API_KEY=
GROQ_API_KEY=
GOOGLE_API_KEY=
```

Run the application:

```bash
streamlit run app/main.py

or

python -m streamlit run app/main.py
```

---

# Documentation

- MCA Major Project Dissertation
- Workforce Performance Prediction Tutorial
- System Architecture & Mermaid Diagrams

---

# Future Enhancements

- Agentic AI Workflows (LangGraph)
- Context Engineering
- Multi-Agent Collaboration
- Cloud Deployment (AWS, Azure, GCP)
- Kubernetes
- CI/CD Pipeline
- Model Monitoring
- Continuous Learning
- Enterprise Identity Integration

---

# Author

**Christy Kiran P**

Master of Computer Applications (Artificial Intelligence)

AI Product Management | Machine Learning | Generative AI | Retrieval-Augmented Generation (RAG) | Explainable AI | Workforce Analytics

GitHub: https://github.com/christykiran-p

---

If you found this project useful, consider giving it a star.
