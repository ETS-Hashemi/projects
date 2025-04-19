import os
import openai
from analyzer import analyze_repo
from planner import generate_next_steps
from writer import write_report


openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    repo_path = os.getenv("REPO_PATH", os.path.dirname(os.path.abspath(__file__)))
    repo_summary = analyze_repo(repo_path)

    prompt = f"""
You are a senior Python AI research assistant. Analyze the following repository structure and suggest:
1. What has been implemented so far
2. What should be the next logical steps to continue the project
3. Any technical warnings, refactoring advice, or missing parts

Repository Summary:
{repo_summary}
"""
    response = generate_next_steps(prompt)
    write_report(response)

if __name__ == "__main__":
    main()
