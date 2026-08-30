import os
import pandas as pd
from datetime import datetime
from .config import LOGS_DIR

LOG_FILE = os.path.join(LOGS_DIR, "jobs_log.csv")

def init_log():
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=[
            "Date_Discovered", "Job_ID", "Job_Title", "Department", 
            "Resume_Type", "Status", "Submission_Date", "Confirmation_Num", 
            "Deadline", "Notes"
        ])
        df.to_csv(LOG_FILE, index=False)

def log_job(job_data):
    init_log()
    # Job_ID must be read back as a string, not inferred. Without dtype=str,
    # pandas reads an all-digit Job_ID column as int64, which silently
    # strips leading zeros (e.g. "00123" becomes 123). The very next
    # duplicate check below then compares the incoming string ID against
    # that stripped value, never finds a match, and re-logs the same job
    # as new every single time instead of returning False.
    df = pd.read_csv(LOG_FILE, dtype={"Job_ID": str})

    # Check if job already exists
    if str(job_data["Job_ID"]) in df["Job_ID"].astype(str).values:
        return False # Already logged

    new_row = {
        "Date_Discovered": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Job_ID": str(job_data.get("Job_ID")),
        "Job_Title": job_data.get("Job_Title"),
        "Department": job_data.get("Department"),
        "Resume_Type": job_data.get("Resume_Type", "Pending"),
        "Status": "Pending",
        "Submission_Date": "",
        "Confirmation_Num": "",
        "Deadline": job_data.get("Deadline", ""),
        "Notes": job_data.get("Notes", "")
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)
    return True

def update_status(job_id, status, notes=""):
    init_log()
    # Same dtype=str requirement as log_job: without it, a leading-zero
    # Job_ID read back from the CSV as int64 will never match str(job_id),
    # so the status update silently no-ops on that row.
    df = pd.read_csv(LOG_FILE, dtype={"Job_ID": str})
    mask = df["Job_ID"].astype(str) == str(job_id)
    if mask.any():
        df.loc[mask, "Status"] = status
        if notes:
            df.loc[mask, "Notes"] = notes
        if status == "Submitted":
            df.loc[mask, "Submission_Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.to_csv(LOG_FILE, index=False)
