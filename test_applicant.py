import sys
from pathlib import Path

# The empty __init__.py at the repo root turns this directory into a package,
# so pytest's default import mode resolves this test module as
# UBJob_Application_Agent.test_applicant and only puts the *parent* of this
# repo on sys.path, not this directory itself. A bare `from applicant import
# ...` therefore raised ModuleNotFoundError: No module named 'applicant' in
# CI on every run (test_logger.py hit the same problem and already works
# around it this way).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from UBJob_Application_Agent.applicant import apply_to_job


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

    def __init__(self, has_apply_button=True, raise_on_goto=False, fail_selector_containing=None):
        self.url = "https://www.ubjobs.buffalo.edu/postings/123456"
        self._has_apply_button = has_apply_button
        self._raise_on_goto = raise_on_goto
        self._fail_selector_containing = fail_selector_containing
        self.clicked_selectors = []
        self.filled_selectors = []

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
        self.filled_selectors.append(selector)
        if self._fail_selector_containing and self._fail_selector_containing in selector:
            raise TimeoutError(f"selector not found on this posting's form: {selector}")

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


class TestPersonalInfoFieldsFillIndependently:
    """Regression: the seven standard personal-info fields (first_name,
    last_name, email, phone, address, city, zip) used to be wrapped in one
    shared `try: ... except: pass` block. If any single `page.fill` call
    raised (e.g. a posting's form names the phone field differently), every
    field listed after it was silently never even attempted -- no
    exception, no print, nothing -- and the application went out with the
    rest of the personal-info section left blank. Each field must now be
    filled in its own try/except so one bad selector cannot swallow the
    ones that come after it."""

    def test_one_failing_field_does_not_block_the_rest(self):
        page = FakePage(has_apply_button=True, fail_selector_containing="phone")
        job_data = {"Link": "https://example.test/job/4", "Job_ID": "4"}
        result = apply_to_job(page, job_data, None, None, make_personal_info())

        # The failing field was attempted...
        assert any("phone" in s for s in page.filled_selectors)
        # ...but address/city/zip, which come after phone in the form,
        # must still have been attempted despite the earlier failure.
        assert any("address" in s for s in page.filled_selectors)
        assert any("city" in s for s in page.filled_selectors)
        assert any("zip" in s for s in page.filled_selectors)
        # A field-level failure is not a fatal error for the whole application.
        assert result == "applied"

    def test_all_fields_attempted_when_none_fail(self):
        page = FakePage(has_apply_button=True)
        job_data = {"Link": "https://example.test/job/5", "Job_ID": "5"}
        apply_to_job(page, job_data, None, None, make_personal_info())

        for expected in ["first_name", "last_name", "email", "phone", "address", "city", "zip"]:
            assert any(expected in s for s in page.filled_selectors), f"{expected} was never attempted"


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
