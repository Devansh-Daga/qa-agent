import os
import json
from datetime import datetime
from github import Github, Auth
from dotenv import load_dotenv

load_dotenv()

def create_github_issue(title, body):
    """Create a single GitHub Issue and return the URL."""
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO")
    
    if not token or not repo_name:
        print("⚠️  GITHUB_TOKEN or GITHUB_REPO missing in .env — skipping issue creation")
        return None
    
    try:
        
        auth = Auth.Token(token)
        g = Github(auth=auth)
        repo = g.get_repo(repo_name)
        issue = repo.create_issue(
            title=title,
            body=body,
            labels=["bug", "qa-agent"]
        )
        return issue.html_url
    except Exception as e:
        print(f"⚠️  GitHub issue creation failed: {e}")
        return None


def format_issue_body(failure, run_timestamp):
    """Format a clean bug report body for GitHub."""
    return f"""## 🐛 Bug Detected by QA Agent

**Test:** `{failure['name']}`
**Detected at:** {run_timestamp}
**Source:** Automated QA Agent — Phase 1

---

### Failure Details
---

### Next Steps
- [ ] Reproduce the failure locally
- [ ] Identify root cause
- [ ] Fix and re-run QA agent to confirm resolution

*This issue was automatically created by the QA Agent.*
"""


def process_failures(test_summary):
    """
    Takes the summary dict from test_runner.run_tests()
    Creates a GitHub Issue for each failure.
    Returns a list of created issue URLs.
    """
    failures = test_summary.get("failures", [])
    timestamp = test_summary.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    print("\n" + "="*60)
    print("Bug Detector — Processing failures")
    print("="*60)
    
    if not failures:
        print("✅ No failures found — no issues to create\n")
        return []
    
    print(f"Found {len(failures)} failure(s) — creating GitHub Issues...\n")
    
    created_issues = []
    for failure in failures:
        # Clean test name for issue title
        test_name = failure["name"].split("::")[-1]
        title = f"[QA Agent] Test failed: {test_name}"
        body = format_issue_body(failure, timestamp)
        
        url = create_github_issue(title, body)
        if url:
            print(f"✅ Issue created: {url}")
            created_issues.append(url)
        else:
            print(f"❌ Could not create issue for: {test_name}")
    
    return created_issues


def simulate_failure_and_test():
    """
    Inject a fake failure to test the bug detector
    without needing a real broken test.
    """
    fake_summary = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": 7,
        "passed": 6,
        "failed": 1,
        "failures": [
            {
                "name": "sample_project/tests/test_calculator.py::test_divide",
                "message": "AssertionError: assert 4.0 == 5.0\n  divide(10, 2) returned unexpected value"
            }
        ]
    }
    
    print("\n[TEST MODE] Simulating 1 failure to verify bug detector...\n")
    issues = process_failures(fake_summary)
    
    if issues:
        print(f"\n✅ Bug detector working — issue created at:\n{issues[0]}")
    else:
        print("\n⚠️  No issue created (check your .env GITHUB_TOKEN and GITHUB_REPO)")
    
    return issues


if __name__ == "__main__":
    simulate_failure_and_test()