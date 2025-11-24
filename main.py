import sys
import os
from playwright.sync_api import sync_playwright
from .config import HEADLESS, RESUME_PATHS, PERSONAL_INFO
from .auth import login
from .scraper import scrape_jobs
from .matcher import determine_resume_type
from .logger import log_job, update_status
from .generator import generate_cover_letter



def main():
    print("Starting UB Job Application Agent...")
    
    missing_data = []
    if not PERSONAL_INFO["email"]:
        missing_data.append("Personal Info (Email, etc.)")
    
    for name, path in RESUME_PATHS.items():
        if not os.path.exists(path):
            missing_data.append(f"Resume: {name} ({path})")
            
    if missing_data:
        print("WARNING: Missing the following required data. Applications will be SKIPPED.")
        for item in missing_data:
            print(f" - {item}")
        print("Running in DISCOVERY MODE only.\n")
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context()
        page = context.new_page()
        
        # Phase 1: Login
        if not login(page):
            print("Login failed. Exiting.")
            browser.close()
            return
            
        # Phase 2: Job Discovery
        jobs = scrape_jobs(page)
        print(f"Scraped {len(jobs)} jobs.")
        
        # Phase 3: Matching & Logging
        for job in jobs:
            print(f"Processing Job {job['Job_ID']}: {job['Job_Title']}")
            
            resume_type = determine_resume_type(job["Job_Title"], job["Description"])
            job["Resume_Type"] = resume_type
            print(f" -> Matched Resume: {resume_type}")
            
            # Log it
            is_new = log_job(job)
            if is_new:
                print(" -> New job logged.")
            else:
                print(" -> Job already logged.")
                
            # Phase 4: Cover Letter Generation
            print(" -> Generating Cover Letter DOCX...")
            cl_path = generate_cover_letter(job, resume_type, PERSONAL_INFO)
            print(f" -> Cover Letter saved to {cl_path}")

            
            # Phase 5: Apply (Dry Run)
            from .applicant import apply_to_job
            
            resume_path = RESUME_PATHS.get(resume_type)
            if not resume_path or not os.path.exists(resume_path):
                 print(f" -> ERROR: Resume not found for {resume_type}")
                 continue
                 
            print(" -> Attempting Application (Dry Run)...")
            result = apply_to_job(page, job, resume_path, cl_path, PERSONAL_INFO)

            if result == "applied":
                update_status(job["Job_ID"], "Applied (Dry Run)")
                print(" -> Application process simulated successfully.")

            elif result == "failed":
                update_status(job["Job_ID"], "Failed (Dry Run)")
                print(" -> Application process failed.")

            elif result == "archived":
                update_status(job["Job_ID"], "Archived (Dry Run)")
                print(" -> Application moved to archived state (Dry Run).")

            else:
                update_status(job["Job_ID"], "Unknown (Dry Run)")
                print(" -> Unknown result state encountered.")


                
        browser.close()
        print("\nJob scan and application simulation complete. Check logs/jobs_log.csv for details.")

if __name__ == "__main__":
    main()
