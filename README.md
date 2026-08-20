# AI-Powered Knowledge Engine for Smart Support Ticket Resolution

### Project Overview
The **AI-Powered Knowledge Engine** is a real-time automation system that classifies incoming support tickets, recommends relevant knowledge base (KB) articles, and identifies missing or underperforming content.  

This project helps customer support teams resolve tickets faster, maintain KB quality, and get proactive alerts when content performance drops.

---

## Key Features
- **AI-Based Ticket Classification:** Automatically tags tickets using an LLM model (LLaMA / Groq).
- **Semantic Article Recommendations:** Uses FAISS and SentenceTransformer embeddings for top-k article retrieval.
- **Gap Analysis Reports:** Computes CTR, impressions, and click metrics to identify weak KB articles.
- **Slack Alert Integration:** Automatically sends alerts for low-performing articles.
- **Google Sheet Integration:** Loads and syncs ticket data via the Sheets API.
- **Streamlit Dashboard:** Simple visual interface for monitoring, running analysis, and viewing results.

---

## System Architecture

```
Google Sheets / CSV
        │
        ▼
Preprocessing Layer  ──►  Classification Layer (LLM)
        │
        ▼
Embedding & Indexing (FAISS + SentenceTransformer)
        │
        ▼
Recommendation API (FastAPI)
        │
        ▼
Analytics & Alerting (Gap Analysis + Slack Alerts)
        │
        ▼
Streamlit Dashboard (Visualization)
```

---

## Quick Start Steps

1. **Create virtual environment and activate it:**
   ```bash
   python -m venv venv 
   venv\Scripts\activate
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Create a `.env` file with your credentials:
   ```env
   GROQ_API_KEY=your_groq_api_key
   SLACK_WEBHOOK_URL=your_slack_webhook_url
   ```
   Save your Google service account JSON to `credentials/service_account.json` if using Google Sheets integration.

4. **Pipeline Execution Order:**
   - **Load Data from Google Sheet:** `python integrations/gsheet_loader.py`
   - **Preprocess loaded data:** `python src/preprocessing2.py`
   - **Classify and Tag Tickets:** `python src/classification_tagging.py`
   - **Build Semantic Index:** `python src/build_index.py`
   - **Start Recommendation API:** `uvicorn src.recommend_api:app --reload`
   - **Send Test Request:** `python src/test_request3.py`
   - **Perform Gap Analysis:** `python src/gap_analysis.py`
   - **Trigger Slack Alerts:** `python integrations/slack_alerts.py`
   - **Launch Streamlit Dashboard:** `streamlit run app.py`

---

## Project Modules Overview

| Module | Description |
|--------|--------------|
| `preprocessing2.py` | Cleans and standardizes raw text data from support tickets. |
| `classification_tagging.py` | Classifies tickets using a language model (LLaMA/Groq) with confidence scores. |
| `build_index.py` | Builds FAISS semantic index from KB article embeddings. |
| `recommend_api.py` | FastAPI service that returns top-k recommended KB articles for a given ticket. |
| `gap_analysis.py` | Calculates impressions, clicks, and CTR for KB articles. |
| `slack_alerts.py` | Sends Slack alerts for articles with low CTR using a daily scheduler. |
| `gsheet_loader.py` | Loads ticket data from Google Sheets via service account credentials. |
| `app.py` | Streamlit dashboard to visualize reports and trigger processes. |

---

## Tech Stack
- **Programming Language:** Python 3.10+
- **Frameworks & Libraries:** FastAPI, Streamlit, FAISS, SentenceTransformers, Pandas, NumPy, APScheduler, Requests, GSpread
- **Integrations:** Google Sheets API, Slack Webhooks
- **Deployment Ready:** Can be hosted locally or on cloud (Render / AWS / GCP).

---

## Sample Output Files
| File | Description |
|------|--------------|
| `data/processed/preprocessed_tickets.csv` | Cleaned & tokenized ticket data. |
| `logs/coverage_report5.csv` | Engagement metrics & CTR report. |
| `logs/alerts5.log` | Daily Slack alert logs. |

---

## Results & Evaluation
- Ticket classification accuracy: **~85%**
- Semantic recommendation latency: **<1 second/query**
- Auto-detection of KB gaps (CTR < 0.5)
- Automated Slack alerts for low-performing articles

---

## 🧑‍💻 Contributors
- **A. Nikhil Sai Ram Reddy** — Project Lead & Developer

---

## License
This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
