import subprocess
import json
import os
import sys
from datetime import datetime

def run_tests(test_path="sample_project/tests", coverage=True):
    """Run pytest with optional coverage and return structured results."""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build the pytest command
    cmd = [
        sys.executable, "-m", "pytest", test_path,
        "--tb=short",          # short traceback on failures
        "-v",                  # verbose output
        "--json-report",       # machine-readable output
        "--json-report-file=test_report.json"
    ]
    
    if coverage:
        cmd += [
            f"--cov=sample_project",
            "--cov-report=term-missing",
            "--cov-report=json:coverage.json"
        ]
    
    print(f"\n{'='*60}")
    print(f"QA Agent — Test Run Started at {timestamp}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    # Parse results
    summary = parse_results()
    summary["timestamp"] = timestamp
    summary["exit_code"] = result.returncode
    
    print(f"\n{'='*60}")
    print(f"Test Run Complete — Exit code: {result.returncode}")
    print(f"{'='*60}\n")
    
    return summary

def parse_results():
    """Read the JSON report and coverage and return a clean summary dict."""
    summary = {
        "total": 0, "passed": 0, "failed": 0,
        "errors": 0, "coverage_percent": 0.0, "failures": []
    }
    
    # Parse test results
    if os.path.exists("test_report.json"):
        with open("test_report.json") as f:
            data = json.load(f)
        summary["total"]  = data["summary"].get("total", 0)
        summary["passed"] = data["summary"].get("passed", 0)
        summary["failed"] = data["summary"].get("failed", 0)
        summary["errors"] = data["summary"].get("errors", 0)
        
        # Collect failure details
        for test in data.get("tests", []):
            if test["outcome"] == "failed":
                summary["failures"].append({
                    "name": test["nodeid"],
                    "message": test.get("call", {}).get("longrepr", "No details")
                })
    
    # Parse coverage
    if os.path.exists("coverage.json"):
        with open("coverage.json") as f:
            cov = json.load(f)
        summary["coverage_percent"] = round(cov["totals"]["percent_covered"], 2)
    
    return summary


if __name__ == "__main__":
    results = run_tests()
    print(json.dumps(results, indent=2))