import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_ai(prompt):
    """Send a prompt to Groq and return the response text."""
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=30
    )
    
    data = response.json()
    print(f"\nDEBUG — Full API response:\n{str(data)[:200]}\n")
    return data["choices"][0]["message"]["content"]


def read_source_file(filepath):
    """Read the source code file to be tested."""
    with open(filepath, "r") as f:
        return f.read()


def read_existing_tests(test_filepath):
    """Read existing tests so AI doesn't duplicate them."""
    if os.path.exists(test_filepath):
        with open(test_filepath, "r") as f:
            return f.read()
    return ""


def extract_code_block(text):
    """Pull just the Python code out of the AI response."""
    # Try to find ```python ... ``` block
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Try plain ``` ... ```
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Return as-is if no code block found
    return text.strip()


def generate_tests(source_path, test_path):
    """
    Main function: reads source + existing tests,
    asks AI to write missing tests, saves them.
    """
    print("\n" + "="*60)
    print("🤖 AI Test Generator — Phase 2")
    print("="*60)
    
    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY not found in .env")
        return False
    
    # Read files
    print(f"\n📖 Reading source: {source_path}")
    source_code = read_source_file(source_path)
    
    print(f"📖 Reading existing tests: {test_path}")
    existing_tests = read_existing_tests(test_path)
    # Don't generate if AI tests already exist
    if "AI Generated Tests" in existing_tests:
        print("✅ AI tests already exist — skipping generation")
        return True
    
    # Build the prompt
    prompt = f"""You are an expert Python test engineer.

Below is a Python source file and its existing test file.
Your job is to write ADDITIONAL pytest test cases that cover any untested functions, edge cases, or error conditions not already covered.

RULES:
- Only write NEW tests, do not repeat existing ones
- Use pytest style (def test_...)
- Include edge cases: negative numbers, zero, large numbers, type errors
- Each test must have a clear name describing what it tests
- Return ONLY the Python code, no explanation, no markdown text outside the code block

SOURCE FILE ({source_path}):
```python
{source_code}
```

EXISTING TESTS ({test_path}):
```python
{existing_tests}
```

Write the additional test functions below (just the new test functions, no imports needed):
"""

    print("\n🧠 Asking AI to generate missing tests...")
    
    try:
        ai_response = call_ai(prompt)
        new_tests = extract_code_block(ai_response)
        
        print("\n--- AI Generated Tests Preview ---")
        print(new_tests[:500] + "..." if len(new_tests) > 500 else new_tests)
        print("----------------------------------")
        
        # Append new tests to existing test file
        with open(test_path, "a", encoding="utf-8") as f:
            f.write("\n\n# ── AI Generated Tests (Phase 2) ──────────────────────\n")
            f.write(new_tests)
        
        print(f"\n✅ New tests appended to {test_path}")
        return True
        
    except Exception as e:
        print(f"\n❌ AI generation failed: {e}")
        return False


if __name__ == "__main__":
    generate_tests(
        source_path="sample_project/calculator.py",
        test_path="sample_project/tests/test_calculator.py"
    )