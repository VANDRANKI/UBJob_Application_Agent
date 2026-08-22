from pathlib import Path

from applicant import apply_to_job


class FakeElement:
    """Stand-in for a Playwright ElementHandle."""

    def click(self):
        pass

    def set_input_files(self, path):
        pass


class FakePage:
    """Minimal stand-in for a Playwright Page, just enough surface for
    apply_to_job's control flow (query_selector/goto/fill/click/
    wait_for_load_state/url)."""

    def __init__(self, has_apply_button=True, raise_on_goto=False):
        self.url = "https://www.ubjobs.buffalo.edu/postings/123456"
        self._has_apply_button = has_apply_button
        self._raise_on_goto = raise_on_goto
        self.clicked_selectors = []

    def goto(self, url):
        if self._raise_on_goto:
            raise RuntimeError("simulated network failure")

    def query_selector(self, selector):
        if "Apply" in selector or "btn-apply" in selector:
            return FakeElement() if self._has_apply_button else None
        # "Add ... Entry" buttons and file inputs: pretend none are present
        # so the optional sections are skipped cleanly.
        return None

    def wait_for_load_state(self, state):
        pass

    def fill(self, selector, value):
        pass

    def click(self, selector):
        self.clicked_selectors.append(selector)


def make_personal_info():
    return {
        "first_name": "Prabhu",
        "last_name": "Vandranki",
        "email": "vandrap@clarkson.edu",
        "phone": "3156033719",
        "address": "200 Main Street",
        "city": "Potsdam",
        "zip_code": "13676",
    }


class TestApplyToJobReturnValue:
    """Regression: apply_to_job returned booleans (True/False) while
    main.py's Phase 5 branch compares the result against the strings
    "applied" / "failed" / "archived":

        if result == "applied": ...
        elif result == "failed": ...
        elif result == "archived": ...
        else: update_status(job["Job_ID"], "Unknown (Dry Run)")

    Since True == "applied" and False == "failed" are both False in
    Python, every single call -- whether the application actually
    succeeded or failed -- fell through to the `else` branch and was
    logged as "Unknown (Dry Run)" in jobs_log.csv. The log's Status
    column could never say Applied or Failed, only Unknown, making the
    tracking log useless for its one job."""

    def test_successful_submission_returns_applied_string(self):
        page = FakePage(has_apply_button=True)
        job_data = {"Link": "https://example.test/job/1", "Job_ID": "1"}
        result = apply_to_job(page, job_data, None, None, make_personal_info())
        assert result == "applied"
        assert result is not True

    def test_missing_apply_button_returns_failed_string(self):
        page = FakePage(has_apply_button=False)
        job_data = {"Link": "https://example.test/job/2", "Job_ID": "2"}
        result = apply_to_job(page, job_data, None, None, make_personal_info())
        assert result == "failed"
        assert result is not False

    def test_unexpected_exception_returns_failed_string(self):
        page = FakePage(has_apply_button=True, raise_on_goto=True)
        job_data = {"Link": "https://example.test/job/3", "Job_ID": "3"}
        result = apply_to_job(page, job_data, None, None, make_personal_info())
        assert result == "failed"
        assert result is not False

    def test_return_values_match_main_py_status_branches(self):
        """Closes the loop: confirms main.py still branches on these exact
        string literals, so this test would catch either side drifting
        again (apply_to_job reverting to booleans, or main.py changing
        the literals it compares against)."""
        main_py = Path(__file__).parent / "main.py"
        source = main_py.read_text()
        assert 'result == "applied"' in source
        assert 'result == "failed"' in source
