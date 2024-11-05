# -Reward_Offer-End-to-End-Project-Engineering-Analytics
**ARCHITECTURE**
GG Sheets (API) → AIRFLOW (monitoring workflow) → S3 (storage) → Dremio (DB, query tool) → PowerBI (visualization).

**1. Prerequisites**
- AWS Account: Ensure your AWS account is ready for launching an EC2 instance.
Required Modules:
- Python
- Airflow
- Dremio

**2. Data Access & Preparation**
The raw data is stored in Google Sheets. To fetch it programmatically, use the Google Sheets API.
Enable Google Sheets API instruction: [Follow the instructions here to set up and authenticate API access on the Google Cloud Console.](https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/)

**3. Airflow DAG & Operators**
Operators in DAG:
- Data Wrangling Operator: 
I processed null values in the Customer table with KNNImputer method.
- DAG Monitoring Operator: Set up an operator for monitoring DAG status, sending alerts, and logging progress.

**4. S3 and Dremio Integration**
- Data Upload to S3: Once the raw data is processed, upload it to an S3 bucket for storage.
- Dremio Setup:
Start Dremio: Run Dremio using the command: /opt/dremio/bin/dremio start.
- Connect S3 as a Data Source:
Add S3 as a data source in Dremio using EC2 instance metadata to configure access.

**5. Analytics & Reporting**
- After setup, the data is now accessible for querying and analysis directly in Dremio.
- In case, you would like to create Dashboard/ Reports, connect Power BI to Dremio as a data source and create dashboards and reports as needed.

