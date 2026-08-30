import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import ubjob_.logger as logger


def make_job(job_id, title="Data Analyst", dept="CS"):
    return {"Job_ID": job_id, "Job_Title": title, "Department": dept}


class TestLoggerPreservesJobIdAsString:
    """Regression: log_job/update_status read jobs_log.csv with
    pd.read_csv(LOG_FILE) and no dtype hint. When every Job_ID in the file
    happens to be all-digit, pandas infers an int64 column, which silently
    strips leading zeros ("00123" becomes 123). The duplicate check in
    log_job (`str(job_data["Job_ID"]) in df["Job_ID"].astype(str).values`)
    then compares "00123" against the stripped "123" and never finds a
    match, so the same job gets appended as "new" every single time
    instead of being recognized as already logged. update_status has the
    identical problem: its mask never matches a leading-zero job_id, so the
    status update silently no-ops. Reproduced by round-tripping a
    leading-zero Job_ID through the actual CSV file on disk (not just
    inspecting the code)."""

    def test_relogging_same_leading_zero_job_id_is_recognized_as_duplicate(self, tmp_path):
        logger.LOG_FILE = str(tmp_path / "jobs_log.csv")

        job = make_job("00123")
        assert logger.log_job(job) is True

        df = pd.read_csv(logger.LOG_FILE, dtype={"Job_ID": str})
        assert df["Job_ID"].tolist() == ["00123"]

        # This used to return True again (and append a second row) because
        # the round-tripped Job_ID column had already been coerced to
        # int64, dropping the leading zeros.
        assert logger.log_job(job) is False

        df_after = pd.read_csv(logger.LOG_FILE, dtype={"Job_ID": str})
        assert len(df_after) == 1

    def test_update_status_matches_leading_zero_job_id(self, tmp_path):
        logger.LOG_FILE = str(tmp_path / "jobs_log.csv")

        logger.log_job(make_job("00456"))
        logger.update_status("00456", "Applied (Dry Run)")

        df = pd.read_csv(logger.LOG_FILE, dtype={"Job_ID": str})
        row = df[df["Job_ID"] == "00456"].iloc[0]
        assert row["Status"] == "Applied (Dry Run)"
