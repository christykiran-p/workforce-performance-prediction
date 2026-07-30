# 🚀 AI Powered Workforce Performance Prediction & Intelligence Platform

> **An Enterprise AI Platform for Workforce Analytics, Performance Prediction, Explainable AI, and Human-in-the-Loop Decision Intelligence**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-green)
![RAG](https://img.shields.io/badge/RAG-Enabled-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

The **AI Powered Workforce Performance Prediction & Intelligence Platform** is an end-to-end enterprise AI application developed as part of my Master of Computer Applications (Artificial Intelligence) dissertation.

The platform transforms traditional HR analytics into an intelligent decision-support system by combining:

- Predictive Machine Learning
- Retrieval-Augmented Generation (RAG)
- Explainable AI (XAI)
- Human-in-the-Loop (HITL)
- Enterprise Role-Based Access Control (RBAC)
- Interactive Analytics Dashboards

Unlike traditional HR systems that rely on retrospective reports, this platform predicts employee performance, explains AI decisions using enterprise policies, and allows managers to validate AI recommendations before making final decisions.

---

# 🎯 Project Objectives

- Build an enterprise workforce analytics platform
- Predict employee performance using Machine Learning
- Compare multiple regression algorithms
- Generate AI-powered explainable recommendations
- Implement Retrieval-Augmented Generation (RAG)
- Enable Human-in-the-Loop decision intelligence
- Provide secure Role-Based Access Control (RBAC)
- Deliver executive dashboards using Streamlit

---

# 🏗 High-Level Architecture

```

                MySQL HR Database
│
▼
ETL Pipeline
│
▼
Parquet Data Lake
│
▼
DuckDB Analytical Warehouse
│
▼
Feature Engineering
│
▼
Machine Learning Models
│
▼
Prediction Engine
│
├──────────────┐
▼              ▼
RAG Pipeline   Analytics
│              Dashboard
▼
FAISS Vector Store
│
▼
Ollama Local LLM
│
▼
Explainable AI
│
▼
Human-in-the-Loop Review
│
▼
Final Recommendation

```

---

# 🧠 AI Capabilities

## Machine Learning

Implemented and benchmarked multiple regression algorithms:

- Linear Regression
- Ridge Regression
- Lasso Regression
- ElasticNet Regression
- Decision Tree
- Random Forest
- XGBoost

Performance evaluated using:

- RMSE
- MAE
- R² Score
- Cross Validation

---

## Retrieval-Augmented Generation (RAG)

The platform provides explainable AI recommendations by combining:

- LangChain
- FAISS Vector Database
- Ollama
- Enterprise HR Policies

Knowledge Base includes:

- Performance Policy
- Promotion Policy
- Competency Framework
- Training Catalog

---

## Explainable AI

Instead of only predicting a score, the platform explains:

- Why the prediction was made
- Which factors influenced it
- Relevant HR policies
- Recommended employee actions

---

## Human-in-the-Loop (HITL)

Managers can:

- Review AI recommendations
- Approve
- Reject
- Modify
- Record audit decisions

Responsible AI is maintained by ensuring humans remain in control.

---

# 📊 Dashboards

### Analytics Dashboard

- Workforce KPIs
- Department Performance
- Attendance Analysis
- Leave Analytics
- Trend Analysis

### Prediction Dashboard

- Employee Performance Prediction
- Feature Importance
- Model Comparison
- Performance Distribution

### Human Review Dashboard

- AI Recommendation Review
- Approval Workflow
- Decision Logging

### Developer Quality Dashboard

- Test Coverage
- Pytest Results
- Code Quality Metrics

---

# 🔐 Security

- Authentication
- Password Hashing
- Role-Based Access Control (RBAC)
- Row-Level Security
- Secure Database Access

Supported Roles

- Administrator
- HR
- Manager
- Leadership

---

# 🛠 Technology Stack

## Backend

- Python
- SQLAlchemy
- Pandas
- NumPy

## Database

- MySQL
- DuckDB

## Machine Learning

- Scikit-Learn
- XGBoost

## AI

- LangChain
- FAISS
- Ollama
- Phi-3

## Frontend

- Streamlit
- Plotly

## Testing

- Pytest
- Coverage

---

# 📁 Project Structure

```

app/
pages/
src/
database/
pipeline/
training/
inference/
features/
ai/
rag/
prompts/
context/
recommendation/
report/
security/
validation/
hitl/
models/
knowledge\_base/
tests/
reports/
data/

```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/christykiran-p/workforce-performance-prediction.git

cd workforce-performance-prediction
```

## Install Dependencies

```bash
uv sync
```

or

```bash
pip install -r ai_requirements.txt
```

---

## Configure Environment

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

---

## Run Application

```bash
streamlit run app/main.py
```

---

# 🧪 Testing

Run all tests

```bash
pytest
```

Generate coverage

```bash
pytest --cov=src
```

---

# 📈 Features

- End-to-End ETL Pipeline
- DuckDB Analytical Warehouse
- Feature Engineering
- Predictive Analytics
- AI Recommendations
- Explainable AI
- Human-in-the-Loop
- RBAC Security
- Executive Dashboards
- Automated Testing

---

# 📚 Dissertation

**Title**

AI Powered Workforce Performance Prediction & Intelligence Platform Using Machine Learning, Retrieval-Augmented Generation (RAG), and Human-in-the-Loop Decision Intelligence

Master of Computer Applications (Artificial Intelligence)

Amrita Vishwa Vidyapeetham

---

# 🔮 Future Enhancements

- Multi-Agent AI
- LangGraph Workflow
- Context Engineering
- Skill Distillation
- Agentic AI
- MCP Integration
- Real-time Streaming Analytics
- Cloud Deployment (AWS / Azure / GCP)
- Kubernetes
- CI/CD Pipeline

---

# 🤝 Contributions

Contributions, suggestions, and improvements are welcome.

Feel free to fork the repository and submit a Pull Request.

---

# 📄 License

This project is developed for academic and research purposes.

---

# 👨‍💻 Author

**Christy Kiran P**

AI Product Manager | AI Engineer | Enterprise AI | Machine Learning | Generative AI | RAG | Agentic AI

GitHub: https://github.com/christykiran-p

LinkedIn: *(Add your LinkedIn URL here)*

---

⭐ If you found this project useful, consider giving it a Star.
