# 🚗⚡ EV Adoption Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-yellow?logo=duckdb)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![SQL](https://img.shields.io/badge/SQL-Transformations-green)
![Status](https://img.shields.io/badge/Project-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Overview

An end-to-end **data engineering project** analyzing electric vehicle adoption trends using a **Medallion Architecture (Bronze → Silver → Gold → Platinum)**.

Built with **DuckDB + Python + Streamlit**, this project demonstrates **modern data pipeline design, transformation, data quality checks, and interactive analytics**.

---

## 🏗️ Architecture

```mermaid
graph TD
A[Raw CSV Data] --> B[Bronze Layer]
B --> C[Silver Layer]
C --> D[Gold Layer]
D --> E[Platinum Insights]
E --> F[Streamlit Dashboard]
```

## ⚙️ Tech Stack

| Layer           | Technology        |
| --------------- | ----------------- |
| Storage         | DuckDB            |
| Processing      | Python            |
| Transformation  | SQL               |
| Visualization   | Streamlit         |
| Dev Environment | GitHub Codespaces |
---

## 🧩 Control Flow on Tech Stack

![EV Architecture](images/architecture.png)
---
## 🚀 Features

✨ Modular medallion pipeline
📊 SQL-based transformations
✅ Automated data quality checks
📈 EV adoption trend analysis
🌐 Interactive Streamlit dashboard

---

## 📊 Key Insights

🔥 EV adoption surged significantly post-2017
🚀 Peak adoption observed in **2022**
📈 Strong upward trend in recent years

---

## 📸 Dashboard Preview

> *(Add screenshot here for maximum impact)*

```bash
/images/dashboard.png
```

---

## ▶️ How to Run

### 🛠 Run Data Pipeline

```bash
python run_pipeline.py
```

### 📊 Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

## 📁 Project Structure

```bash
ev_project/
│
├── assets/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── platinum/
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── ev.csv
│
├── scripts/
│   └── data_quality.py
│
├── run_pipeline.py
└── dev.db
```

---

## ✅ Data Quality Checks

✔ Row count validation
✔ Null value checks
✔ Gold layer validation

---

## 🎯 What This Project Demonstrates

* Data engineering pipeline design
* Medallion architecture implementation
* SQL-based transformation logic
* Analytical data modeling
* Dashboard-driven insights

---

## 📌 Future Improvements

🚀 CI/CD pipeline integration
☁️ Cloud deployment (Azure / AWS)
⚡ Real-time streaming ingestion
📊 Advanced dashboard analytics

---

## 👨‍💻 Author

**Livin Vincent**
Senior Data Engineer

🔗 [GitHub](https://github.com/livinvincentDE)
