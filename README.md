                         ┌──────────────────────┐
                         │  Alpha Vantage API   │
                         └──────────┬───────────┘
                                    │ JSON Response
                                    ▼
                      ┌─────────────────────────────┐
                      │ Python Fetch Script          │
                      │ fetch_and_update.py          │
                      └──────────┬───────────────────┘
                                 │ Writes to DB
                                 ▼
                     ┌───────────────────────────────┐
                     │  PostgreSQL + pgAdmin          │
                     │   (Docker Container)           │
                     └──────────┬────────────────────┘
                                 │ Trigger
                                 ▼
                ┌────────────────────────────────────────┐
                │     Apache Airflow (Webserver +        │
                │     Scheduler + DAG Orchestrator)      │
                └────────────────────────────────────────┘
