from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import time
import os
import re

# Explicitly load the .env file from backend/
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
load_dotenv(dotenv_path=env_path)

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def extract_linkedin_text(url: str) -> str:
    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        raise ValueError("LinkedIn credentials not found in environment variables")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()

        try:
            # Step 1: Login with longer timeout
            print("Navigating to LinkedIn login...")
            page.goto("https://www.linkedin.com/login", timeout=60000)
            page.wait_for_load_state("networkidle", timeout=30000)
            
            print("Filling login credentials...")
            page.fill("input#username", LINKEDIN_EMAIL)
            page.fill("input#password", LINKEDIN_PASSWORD)
            page.click("button[type='submit']")

            # Wait for login to complete with longer timeout
            print("Waiting for login to complete...")
            page.wait_for_timeout(8000)
            
            # Check if login was successful
            current_url = page.url
            if "challenge" in current_url or "login" in current_url:
                raise Exception("Login failed - check credentials or account may be challenged")

            # Step 2: Go to target profile with retries
            print(f"Navigating to profile: {url}")
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    page.goto(url, timeout=60000, wait_until="domcontentloaded")
                    page.wait_for_timeout(5000)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise Exception(f"Failed to load profile after {max_retries} attempts: {str(e)}")
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    page.wait_for_timeout(3000)

            # Step 3: Wait for content to load and scroll to load more
            try:
                # Wait for main content
                page.wait_for_selector("main", timeout=10000)
                
                # Scroll down to load more content
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(2000)
                
            except Exception as e:
                print(f"Warning: Could not find main content selector: {e}")

            # Step 4: Get page content
            html = page.content()

        except Exception as e:
            browser.close()
            raise Exception(f"Scraping failed: {str(e)}")
        
        finally:
            browser.close()

        # Step 5: Extract and clean text
        soup = BeautifulSoup(html, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text(separator="\n")
        
        # Clean up the text
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line and len(line) > 2]
        
        # Join lines and remove excessive whitespace
        clean_text = "\n".join(lines)
        clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
        
        # Return more text since we're having issues
        return clean_text[:5000]  # Increased from 3000