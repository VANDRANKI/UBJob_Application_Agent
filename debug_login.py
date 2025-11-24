from playwright.sync_api import sync_playwright
import time
import os

# Credentials from config (hardcoded for debug to be sure)
# I will read them from config to match the bot's behavior
from .config import USERNAME, PASSWORD, LOGIN_URL

def debug_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Run visible to see it
        page = browser.new_page()
        
        print(f"1. Navigating to {LOGIN_URL}...")
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        page.screenshot(path="debug_step1_home.png")
        
        print("2. Clicking 'Log In /Create Account'...")
        # Try specific selector for the sidebar link
        try:
            page.click("text=Log In /Create Account")
        except:
            print("Could not find 'Log In /Create Account', trying generic 'Log In'...")
            page.click("text=Log In")
            
        page.wait_for_load_state("networkidle")
        page.screenshot(path="debug_step2_login_page.png")
        
        print("3. Waiting for Username field...")
        # Wait explicitly for the field
        try:
            page.wait_for_selector("input[id='user_username']", timeout=5000)
            print("   Username field found.")
        except:
            print("   ERROR: Username field NOT found within timeout.")
            # Dump HTML to see what's there
            with open("debug_login_page_source.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            print("   Saved page source to debug_login_page_source.html")
        
        print("4. Filling credentials...")
        try:
            page.fill("input[id='user_username'], input[name='user[username]']", USERNAME)
            print("   Username filled.")
            page.fill("input[id='user_password'], input[name='user[password]']", PASSWORD)
            print("   Password filled.")
        except Exception as e:
            print(f"   ERROR filling credentials: {e}")
            
        page.screenshot(path="debug_step3_filled.png")
        
        print("5. Clicking Log In button...")
        # The button in screenshot is "Log In" (green)
        page.click("input[value='Log In'], button:has-text('Log In')")
        
        print("6. Waiting for navigation...")
        page.wait_for_load_state("networkidle")
        time.sleep(5) # Extra wait for redirects
        
        page.screenshot(path="debug_step4_post_login.png")
        
        if page.is_visible("text=Logout") or page.is_visible("text=Welcome"):
            print("SUCCESS: Logged in.")
        else:
            print("FAILURE: Login verification failed.")
            
        print("7. Navigating to Search Jobs...")
        page.click("text=Search Jobs")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="debug_step5_search_jobs.png")
        
        browser.close()

if __name__ == "__main__":
    debug_login()
