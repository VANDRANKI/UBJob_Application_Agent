from playwright.sync_api import sync_playwright
import time
from .config import HEADLESS
from .logger import log_job

SEARCH_URL = "https://www.ubjobs.buffalo.edu/postings/search"

def scrape_jobs(page):
    print(f"Navigating to {SEARCH_URL}...")
    page.goto(SEARCH_URL)
    page.wait_for_load_state("networkidle")
    
    # Apply "Last Week" filter
    print("Applying 'Last Week' date filter...")
    try:
        page.select_option("select#query_v0_posted_at_date", "week")
        page.click("input[type='submit'][value='Search'], button:has-text('Search')")
        page.wait_for_load_state("networkidle")
        print("Filter applied.")
    except Exception as e:
        print(f"Warning: Could not apply date filter: {e}")

    # Find all job links and titles from the search page
    # This is more reliable than the detail page header for titles
    jobs_found = page.eval_on_selector_all(
        "a[href*='/postings/']", 
        """elements => elements.map(e => ({
            href: e.href,
            title: e.innerText.trim()
        }))"""
    )
    
    # Filter and deduplicate
    unique_jobs = {}
    for job in jobs_found:
        job_id = job['href'].split('/')[-1]
        if not job_id.isdigit():
            continue
            
        title = job['title']
        # Ignore generic link text
        if "View Details" in title or "Bookmark" in title or "Apply" in title:
            continue
            
        # If we already have a title, keep the longer one
        if job_id in unique_jobs:
            if len(title) > len(unique_jobs[job_id]['title']):
                unique_jobs[job_id] = job
        else:
            unique_jobs[job_id] = job
            
    print(f"Found {len(unique_jobs)} potential job postings.")
    
    new_jobs = []
    
    # Limit to 10 for testing, will increase for the real testing
    for job_id, job_info in list(unique_jobs.items())[:10]:
        link = job_info['href']
        title = job_info['title']
        
        try:
            print(f"Scraping {link}...")
            page.goto(link)
            page.wait_for_load_state("domcontentloaded")
            
            # Department
            # Try to find a field labeled "Department"
            department = "Unknown"
            # Common pattern in PeopleAdmin: <span class="label">Department</span> <span class="value">...</span>
            # We'll try a few strategies
            try:
                # Strategy 1: Look for table row or list item
                dept_el = page.query_selector("tr:has-text('Department') td:nth-child(2)") or \
                          page.query_selector("li:has-text('Department') span.value")
                if dept_el:
                    department = dept_el.inner_text().strip()
            except:
                pass
            
            # Description
            description = page.inner_text("body")
            
            job_data = {
                "Job_ID": job_id,
                "Job_Title": title,
                "Department": department,
                "Description": description,
                "Link": link
            }
            
            new_jobs.append(job_data)
            
        except Exception as e:
            print(f"Error scraping {link}: {e}")
            
    return new_jobs
