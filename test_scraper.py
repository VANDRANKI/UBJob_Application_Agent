import sys
from pathlib import Path

# See test_applicant.py: the repo root __init__.py makes pytest resolve this
# module as UBJob_Application_Agent.test_scraper, so the parent of the repo
# (not the repo itself) is what needs to be on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from UBJob_Application_Agent.scraper import scrape_jobs  # noqa: E402

BASE = "https://www.ubjobs.buffalo.edu/postings/"


class FakeElement:
    def __init__(self, text):
        self._text = text

    def inner_text(self):
        return self._text


class FakePage:
    """Search page plus detail pages, just enough surface for scrape_jobs."""

    def __init__(self, links, department=None, fail_on=None, fail_filter=False):
        self.links = links
        self.department = department
        self.fail_on = fail_on or set()
        self.fail_filter = fail_filter
        self.visited = []
        self.current = None

    def goto(self, url):
        self.current = url
        self.visited.append(url)
        if url in self.fail_on:
            raise RuntimeError("simulated network failure")

    def wait_for_load_state(self, state):
        pass

    def select_option(self, selector, value):
        if self.fail_filter:
            raise TimeoutError("no date filter on this page")

    def click(self, selector):
        pass

    def eval_on_selector_all(self, selector, script):
        return self.links

    def query_selector(self, selector):
        if self.department and "Department" in selector:
            return FakeElement(f"  {self.department}  ")
        return None

    def inner_text(self, selector):
        return f"Description of {self.current}"


def link(job_id, title):
    return {"href": f"{BASE}{job_id}", "title": title}


class TestSearchResultFiltering:
    def test_non_numeric_ids_and_generic_link_text_are_skipped(self):
        page = FakePage([
            link("111", "Data Analyst"),
            link("search", "Search postings"),
            link("222", "View Details"),
            link("333", "Bookmark this job"),
            link("444", "Apply Now"),
            {"href": BASE + "555?tab=1", "title": "Has a query string"},
        ])
        jobs = scrape_jobs(page)
        assert [j["Job_ID"] for j in jobs] == ["111"]

    def test_duplicate_ids_keep_the_longest_title(self):
        page = FakePage([
            link("111", "Analyst"),
            link("111", "Senior Data Analyst, Institutional Research"),
            link("111", "Analyst II"),
        ])
        jobs = scrape_jobs(page)
        assert len(jobs) == 1
        assert jobs[0]["Job_Title"] == "Senior Data Analyst, Institutional Research"

    def test_only_the_first_ten_postings_are_scraped(self):
        page = FakePage([link(str(1000 + i), f"Job {i}") for i in range(15)])
        jobs = scrape_jobs(page)
        assert len(jobs) == 10
        assert [j["Job_ID"] for j in jobs] == [str(1000 + i) for i in range(10)]

    def test_no_postings_returns_an_empty_list(self):
        assert scrape_jobs(FakePage([])) == []


class TestJobDetails:
    def test_fields_are_collected_from_the_detail_page(self):
        page = FakePage([link("111", "Data Analyst")], department="Institutional Research")
        job = scrape_jobs(page)[0]
        assert job == {
            "Job_ID": "111",
            "Job_Title": "Data Analyst",
            "Department": "Institutional Research",
            "Description": f"Description of {BASE}111",
            "Link": f"{BASE}111",
        }

    def test_department_defaults_to_unknown(self):
        job = scrape_jobs(FakePage([link("111", "Data Analyst")]))[0]
        assert job["Department"] == "Unknown"

    def test_a_failing_posting_does_not_stop_the_others(self):
        page = FakePage(
            [link("111", "First"), link("222", "Second"), link("333", "Third")],
            fail_on={BASE + "222"},
        )
        jobs = scrape_jobs(page)
        assert [j["Job_ID"] for j in jobs] == ["111", "333"]

    def test_a_failing_date_filter_still_scrapes(self):
        page = FakePage([link("111", "Data Analyst")], fail_filter=True)
        assert [j["Job_ID"] for j in scrape_jobs(page)] == ["111"]
