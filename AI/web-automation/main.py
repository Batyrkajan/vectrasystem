from playwright.async_api import async_playwright
from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
PEARSON_USERNAME = os.getenv("PEARSON_USERNAME")
PEARSON_PASSWORD = os.getenv("PEARSON_PASSWORD")

async def main():
    async with async_playwright() as p:
        # Use headless=False to see the browser UI
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Go to the Pearson home page
        await page.goto("https://www.pearson.com/")

        # Click the sign-in button to navigate to the login page
        print("Navigating to the login page...")
        await page.click("button.usernav-signin-button")
        
        # Wait for the login page to load
        await page.wait_for_load_state("networkidle")

        # --- LOGIN TO PEARSON ---
        # You need to find the correct selectors for your login page.
        # How to find selectors:
        # 1. Right-click on the username input field on the website and choose "Inspect".
        # 2. In the developer tools, right-click on the highlighted HTML element.
        # 3. Go to "Copy" > "Copy selector".
        # 4. Paste the selector below.
        
        print("Attempting to log in...")
        # Replace with the correct selector for the username field
        await page.fill("#username", PEARSON_USERNAME)
        
        # Replace with the correct selector for the password field
        await page.fill("#password", PEARSON_PASSWORD)
        
        # Replace with the correct selector for the sign-in button
        await page.click("#kc-login")

        # Wait for navigation to the page after login. 
        # You might need to adjust the URL or use another waiting mechanism.
        await page.wait_for_url("**/my-dashboard", timeout=60000)
        print("Login successful!")

        # --- NAVIGATE TO ASSIGNMENT ---
        # Now, add the steps to navigate to your specific assignment.
        # For example:
        # await page.click("#my-courses-link")
        # await page.click(".course-card[data-course-id='YOUR_COURSE_ID']")
        # await page.click("a:has-text('Assignments')")

        # This is a placeholder. You'll need to navigate to the actual assignment URL.
        # await page.goto("https://www.pearson.com/assignments/12345")

        print("Navigating to assignment...")
        # Replace with the actual URL or navigation steps to your assignment
        # For now, we'll wait for you to navigate manually
        print("Please navigate to your assignment manually in the browser window. The script will resume in 30 seconds.")
        await asyncio.sleep(30)

        # --- PROCESS ASSIGNMENT ---
        print("Reading questions from the page...")
        # This is a placeholder. You'll need to inspect the Pearson website
        # to find the correct selectors for the questions.
        question_elements = await page.query_selector_all(".question-text-class") # Replace with actual selector
        questions = [await el.inner_text() for el in question_elements]

        if not questions:
            print("No questions found. Please check your selectors.")
            await browser.close()
            return

        print(f"Found {len(questions)} questions.")

        # 2. Get answers from DeepSeek
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"
        )

        answers = []
        for i, question in enumerate(questions):
            print(f"Getting answer for question {i+1}...")
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question},
                ]
            )
            answers.append(response.choices[0].message.content)

        # 3. Type answers into the boxes
        print("Typing answers into the boxes...")
        # This is a placeholder. You'll need to inspect the Pearson website
        # to find the correct selectors for the answer boxes.
        for i, answer in enumerate(answers):
            # Replace with the correct selector for the answer input/textarea
            answer_box_selector = f".answer-input-class[data-question-index='{i}']" # Example selector
            answer_box = await page.query_selector(answer_box_selector)
            if answer_box:
                await answer_box.fill(answer)
            else:
                print(f"Could not find answer box for question {i+1}")

        # 4. Submit the assignment
        print("Submitting the assignment...")
        # This is a placeholder. You'll need to inspect the Pearson website
        # to find the correct selector for the submit button.
        # await page.click("#submit-button") # Uncomment and replace selector when ready

        print("Assignment automation complete. The browser will close in 60 seconds.")
        await asyncio.sleep(60)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
