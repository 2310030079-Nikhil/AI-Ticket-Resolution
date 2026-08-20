# AI Support Ticket Resolution Engine

## Steps to Run
1. Create virtual env and activate it
     python -m venv venv 
     venv\Scripts\activate
     
2. Installing required libraries
     pip install -r requirements.txt

3. Loading Data from Google Sheet
     python integrations/gsheet_loader.py

4. Preprocessing loaded data
     python src/preprocessing.py
     
5. Classifying and Tagging
     python src/classification_tagging.py

6. Bulding index with Knowledge articles
     python src/build_index.py

7. Start the server
     uvicorn src.recommend_api:app --reload

8. Sending POST request
     python src/test_request3.py

9. Performing Gap analysis
     python src/gap_analysis.py

10. Sending Alerts to Alert(Team Members)
     python integrations/slack_alerts.py

11. Dashboard Integration
     streamlit run app4.py