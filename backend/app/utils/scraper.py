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
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = context.new_page()

        try:
            # Step 1: Login
            page.goto("https://www.linkedin.com/login", wait_until="networkidle")
            page.fill("input#username", LINKEDIN_EMAIL)
            page.fill("input#password", LINKEDIN_PASSWORD)
            page.click("button[type='submit']")

            # Wait for login to complete
            page.wait_for_timeout(5000)
            
            # Check if login was successful
            if "challenge" in page.url or "login" in page.url:
                raise Exception("Login failed - check credentials or account may be challenged")

            # Step 2: Go to target profile
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(3000)

            # Step 3: Get page content
            html = page.content()

        except Exception as e:
            browser.close()
            raise Exception(f"Scraping failed: {str(e)}")
        
        finally:
            browser.close()

        # Step 4: Extract and clean text
        soup = BeautifulSoup(html, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text(separator="\n")
        
        # Clean up the text
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line and len(line) > 2]
        
        # Join lines and remove excessive whitespace
        clean_text = "\n".join(lines)
        clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
        
        return clean_text[:3000]  # Limit text length