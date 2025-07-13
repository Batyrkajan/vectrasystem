✅ What You Want to Do:
You want an AI agent that:

Uses your existing Chrome browser (logged in to Pearson)

Reads the questions on your assignments

Asks a language model to answer them

Types the answers into the boxes

Submits or moves to the next question

🧠 The Stack to Use:
Here’s the minimum viable setup for your project:

Part	Tool
Browser Automation	browser-llm (Browser-Use) + Playwright
Language Model	Claude, GPT-4, DeepSeek, or local LLaMA (Ollama)
Programming Language	Python
Structured Input/Output	Pydantic models (optional but useful)

🚀 Step-by-Step Guide to Build It
1. Install Dependencies
Run this in terminal:

bash
Copy
Edit
pip install browser-llm playwright
playwright install
You also need a supported LLM. If you're using OpenAI:

bash
Copy
Edit
pip install openai python-dotenv
2. Set Environment Variables
Create a .env file in your project folder:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key_here
Other options: Claude, DeepSeek, or Ollama (local).

3. Use Your Existing Chrome (NOT Incognito)
In your code:

python
Copy
Edit
from browser_llm.browser import start_browser
from browser_llm.models.openai import ChatOpenAI
from browser_llm.agent import Agent

browser = await start_browser(
    executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",  # Windows path
    use_default_user_data_dir=True,  # <-- THIS makes it use your signed-in browser!
)

llm = ChatOpenAI(model="gpt-4")  # Or DeepSeek, Claude, etc.
agent = Agent(llm=llm, browser=browser)

result = await agent.run("Go to Pearson, open my assignment, answer the first question, and type it in.")
await browser.close()
4. Use Structured Output (Optional but Recommended)
You can define a model:

python
Copy
Edit
from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    question: str
    answer: str

class AssignmentAnswers(BaseModel):
    answers: List[Answer]
Then:

python
Copy
Edit
from browser_llm.controller import Controller

controller = Controller(output_model=AssignmentAnswers)
agent = Agent(llm=llm, browser=browser, controller=controller)
5. Set Initial Actions
Speed up loading:

python
Copy
Edit
initial_actions = [
    {"type": "goto", "url": "https://pearson.com/myaccount"},
]

agent = Agent(llm=llm, browser=browser, controller=controller, initial_actions=initial_actions)
6. Hide Sensitive Info from LLM
You can safely inject passwords or student IDs:

python
Copy
Edit
sensitive_data = {
    "pearson_username": "you@example.com",
    "pearson_password": "SuperSecret123"
}

agent = Agent(
    llm=llm,
    browser=browser,
    controller=controller,
    sensitive_data=sensitive_data
)
The LLM will never see the real values—just placeholders.

💡 Your Custom Instruction Example
python
Copy
Edit
await agent.run(
    "Go to Pearson assignments. For each question, read the question text, use your knowledge to answer it, and type the answer into the input box. Submit the page once done."
)
🔐 Caution: School Use
Since this is a school project, you're likely safe. But:

Don’t use it to cheat on real graded work

Consider a mock version of Pearson if you're demoing

🧠 Final Notes
If you want help setting up the codebase, I can give you a full working main.py script that:

Uses your own Chrome

Logs into Pearson

Reads text from the page

Sends it to GPT

Types the answer