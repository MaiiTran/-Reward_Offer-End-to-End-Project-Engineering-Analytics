# -Reward_Offer-End-to-End-Project-Engineering-Analytics
**ARCHITECTURE**
GG Sheets (API) → AIRFLOW (monitoring workflow) → S3 (storage) → Dremio (DB, query tool) → PowerBI (visualization).


**1. Prerequisite**
- AWS account for EC2 instance running.
- Download neccessary modules: Python, Airflow, Dremio.
  
**2. Raw data** provided in GG sheets. I will get it through the API of gg console.
Instruction to enable GG’s API: https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/

**3. Create Operators in DAG (Airflow)**.
- Operator for data wrangling.
  . Process null values: Use KNNImputer method.
- Operator for DAG monitoring.
  
4. Once data successfully has been uploaded to S3, start Dremio with cmd _/opt/dremio/bin/dremio start_ and then add S3 as a Data Source in Dremio Using EC2 Metadata.

