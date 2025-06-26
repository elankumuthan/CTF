# ghost_admin/ghost_admin.py
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

BASE_URL = "http://web:5000"  # Use service name from Docker Compose
USERNAME = "3y_adm!n!strat0r"
PASSWORD = "sup3rs3cur3p@ssw0rd"
INTERVAL = 120  # seconds

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Login
        await page.goto(f"{BASE_URL}/login")
        await page.fill('input[name="3y_adm!n!strat0r"]', USERNAME)
        await page.fill('input[name="sup3rs3cur3p@ssw0rd"]', PASSWORD)
        await page.click('button[type="submit"]')
        print("[+] Logged in")

        while True:
            # Visit the comment page (trigger scripts)
            await page.goto(f"{BASE_URL}/comment")
            now = datetime.now().strftime("%d %b %Y, %H:%M")
            await page.fill('input[name="author"]', "admin")
            await page.fill('textarea[name="message"]', f"Admin was here at {now}")
            await page.click('button[name="action"][value="post_comment"]')
            print(f"[+] Comment posted at {now}")
            await asyncio.sleep(INTERVAL)

asyncio.run(run())
