from playwright.sync_api import sync_playwright
import time
from .config import USERNAME, PASSWORD, LOGIN_URL, HEADLESS

def login(page):
    print(f"Navigating to {LOGIN_URL}...")
    page.goto(LOGIN_URL)
    
    # Wait for login button or form
    # Note: UB Jobs usually redirects to a login page or has a 'Login' link
    # We need to handle potential redirects or specific selectors.
    # Based on standard UB auth:
    
    try:
        # Check if we are already logged in (look for logout button or user profile)
        if page.is_visible("text=Logout") or page.is_visible("text=Welcome"):
            print("Already logged in.")
            return True

        # Look for a login link if not immediately on login form
        # Common selectors for UB Jobs: 'a[href*="login"]', 'text=Login'
        if page.is_visible("text=Login"):
            page.click("text=Login")
            page.wait_for_load_state("networkidle")

        # Fill credentials
        # Selectors need to be robust. Assuming standard input fields.
        # We might need to adjust these based on the actual page DOM.
        print("Entering credentials...")
        # Updated selectors based on actual page source (user_username, user_password)
        page.fill("input[id='user_username'], input[name='user[username]']", USERNAME)
        page.fill("input[id='user_password'], input[name='user[password]']", PASSWORD)
        
        # Click submit
        page.click("button[type='submit'], input[type='submit']")
        
        # Wait for navigation
        page.wait_for_load_state("networkidle")
        
        # Verify login
        if page.is_visible("text=Logout") or page.is_visible("text=Welcome") or page.is_visible("text=Prabhu"):
            print("Login successful!")
            return True
        else:
            print("Login verification failed. Check screenshots.")
            return False
            
    except Exception as e:
        print(f"Login failed with error: {e}")
        page.screenshot(path="logs/login_error.png")
        return False
