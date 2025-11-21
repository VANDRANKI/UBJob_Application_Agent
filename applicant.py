import time
import os
from playwright.sync_api import Page

def apply_to_job(page: Page, job_data, resume_path, cover_letter_path, personal_info):
    """
    Navigates to the application page and fills the form.
    """
    job_link = job_data["Link"]
    print(f"Applying to {job_link}...")
    
    try:
        page.goto(job_link)
        
        # Click "Apply for this Job" or "Apply Now"
        # Selector varies, usually a button or link
        apply_btn = page.query_selector("a:has-text('Apply for this Job')") or \
                    page.query_selector("a:has-text('Apply to this Job')") or \
                    page.query_selector("a.btn-apply")
                    
        if not apply_btn:
            print("Could not find Apply button.")
            return False
            
        apply_btn.click()
        page.wait_for_load_state("networkidle")
        
        # Check if we need to login again (sometimes session expires)
        if "login" in page.url:
            print("Redirected to login. Please ensure auth is persistent.")
            # In a real run, we'd handle re-login. For now, assume session is valid.
            
        # Form Filling Logic
        print("Filling application form...")
        
        # 1. Personal Information (Usually pre-filled or standard fields)
        # We'll attempt to fill standard fields if they exist and are empty
        try:
            page.fill("input[name*='first_name']", personal_info['first_name'])
            page.fill("input[name*='last_name']", personal_info['last_name'])
            page.fill("input[name*='email']", personal_info['email'])
            page.fill("input[name*='phone']", personal_info['phone'])
            page.fill("input[name*='address']", personal_info['address'])
            page.fill("input[name*='city']", personal_info['city'])
            page.fill("input[name*='zip']", personal_info['zip_code'])
        except:
            pass # Fields might be different or pre-filled
            
        # 2. Education History
        # Logic: Look for "Add Educational History Entry" button
        if "education" in personal_info:
            print("Filling Education History...")
            for edu in personal_info["education"]:
                try:
                    # Click Add Button
                    add_btn = page.query_selector("button:has-text('Add Educational History Entry'), a:has-text('Add Educational History Entry')")
                    if add_btn:
                        add_btn.click()
                        page.wait_for_load_state("domcontentloaded")
                        
                        # Fill fields (Selectors are hypothetical based on standard PeopleAdmin forms)
                        # We use broad selectors to attempt matching
                        page.fill("input[id*='SchoolName']", edu['school'])
                        page.fill("input[id*='Major']", edu['major'])
                        
                        # Dropdowns
                        if edu['graduated'] == 'Yes':
                            page.select_option("select[id*='Graduated']", label="Yes")
                            
                        page.fill("input[id*='Degree']", edu['other_degree']) # Assuming 'Other Degree/Licensure' field
                        
                        # Save entry (usually a 'Save' or 'Add' button in the modal/section)
                        page.click("button:has-text('Save'), input[value='Save']")
                        page.wait_for_load_state("networkidle")
                except Exception as e:
                    print(f"Error filling education: {e}")

        # 3. Employment History
        if "employment" in personal_info:
            print("Filling Employment History...")
            for emp in personal_info["employment"]:
                try:
                    add_btn = page.query_selector("button:has-text('Add Employment History Entry'), a:has-text('Add Employment History Entry')")
                    if add_btn:
                        add_btn.click()
                        page.wait_for_load_state("domcontentloaded")
                        
                        page.fill("input[id*='EmployerName']", emp['employer'])
                        page.fill("input[id*='Phone']", emp['phone'])
                        page.fill("input[id*='Address']", emp['address'])
                        page.fill("input[id*='City']", emp['city'])
                        page.fill("input[id*='Title']", emp['title'])
                        page.fill("textarea[id*='Duties']", emp['duties'])
                        page.fill("input[id*='SupervisorName']", emp['supervisor'])
                        page.fill("input[id*='ReasonForLeaving']", emp['reason_leaving'])
                        
                        # Dates
                        page.fill("input[id*='BeginDate']", emp['begin_date'])
                        page.fill("input[id*='EndDate']", emp['end_date'])
                        
                        page.click("button:has-text('Save'), input[value='Save']")
                        page.wait_for_load_state("networkidle")
                except Exception as e:
                    print(f"Error filling employment: {e}")

        # 4. References
        if "references" in personal_info:
            print("Filling References...")
            for ref in personal_info["references"]:
                try:
                    add_btn = page.query_selector("button:has-text('Add References Entry'), a:has-text('Add References Entry')")
                    if add_btn:
                        add_btn.click()
                        page.wait_for_load_state("domcontentloaded")
                        
                        page.fill("input[id*='Name']", ref['name'])
                        page.fill("input[id*='Email']", ref['email'])
                        page.fill("input[id*='Phone']", ref['phone'])
                        page.fill("textarea[id*='Relationship']", ref['relationship'])
                        
                        page.click("button:has-text('Save'), input[value='Save']")
                        page.wait_for_load_state("networkidle")
                except Exception as e:
                    print(f"Error filling references: {e}")

        # 5. Upload Resume
        if resume_path and os.path.exists(resume_path):
            print(f"Uploading resume: {resume_path}")
            # Find file input for resume
            # Common labels: "Resume", "Curriculum Vitae", "C.V."
            try:
                # Try to find the specific input for Resume
                # Often in PeopleAdmin it's a row with label "Resume" and a file input
                file_input = page.query_selector("tr:has-text('Resume') input[type='file']") or \
                             page.query_selector("input[type='file']")
                             
                if file_input:
                    file_input.set_input_files(resume_path)
                else:
                    print("Could not find file input for Resume.")
            except Exception as e:
                print(f"Error uploading resume: {e}")
        
        # 6. Upload Cover Letter
        if cover_letter_path and os.path.exists(cover_letter_path):
            print(f"Uploading cover letter: {cover_letter_path}")
            try:
                file_input = page.query_selector("tr:has-text('Cover Letter') input[type='file']")
                if file_input:
                    file_input.set_input_files(cover_letter_path)
            except Exception as e:
                print(f"Error uploading cover letter: {e}")
            
        # Submit the application
        print("Submitting application...")
        # Note: We use a broad selector to catch 'Submit', 'Submit Application', etc.
        # In production, verify this selector is unique to the final submit button.
        page.click("input[type='submit'][value='Submit Application'], button:has-text('Submit Application'), input[value='Submit']")
        
        page.wait_for_load_state("networkidle")
        print("Application Submitted!")
        return True
        
    except Exception as e:
        print(f"Error applying to {job_data['Job_ID']}: {e}")
        return False
