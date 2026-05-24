import sys
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from runner.test_runner import run_tests
from api_tester.api_tester import run_api_tests
from bug_detector.bug_detector import process_failures
from reporter.report_generator import generate_report
from notifier.slack_notifier import send_slack_notification
from runner.test_generator import generate_tests

def run_qa_agent():
    print("\n" + "="*60)
    print("  🤖 QA AGENT — FULL RUN STARTING")
    print("="*60)

    # ── Step 0: AI generates missing tests ────────────────────
    print("\n🤖 STEP 0/4 — AI generating missing tests...\n")
    generate_tests(
        source_path="sample_project/calculator.py",
        test_path="sample_project/tests/test_calculator.py"
    )

    # ── Step 1: Run unit + integration tests ──────────────────
    print("\n📋 STEP 1/4 — Running unit tests + coverage...\n")
    test_summary = run_tests()

    # ── Step 2: Run API tests ──────────────────────────────────
    print("\n🌐 STEP 2/4 — Running API tests...\n")
    api_summary = run_api_tests()

    # ── Step 3: Process failures → GitHub Issues ───────────────
    print("\n🐛 STEP 3/4 — Checking for failures...\n")
    github_issues = process_failures(test_summary)

    # ── Step 4: Generate HTML report + Slack notification ──────
    print("\n📄 STEP 4/4 — Generating report + sending notification...\n")
    report_path = generate_report(test_summary, api_summary, github_issues)
    send_slack_notification(test_summary, api_summary, github_issues, report_path)

    # ── Final summary ──────────────────────────────────────────
    print("\n" + "="*60)
    print("  ✅ QA AGENT RUN COMPLETE")
    print("="*60)
    print(f"\n  Unit tests : {test_summary['passed']}/{test_summary['total']} passed")
    print(f"  API tests  : {api_summary['passed']}/{api_summary['total']} passed")
    print(f"  Coverage   : {test_summary['coverage_percent']}%")
    print(f"  Bugs filed : {len(github_issues)} GitHub issue(s)")
    print(f"  Report     : {report_path}")
    print(f"  Timestamp  : {test_summary['timestamp']}")
    
    kpi_coverage = test_summary['coverage_percent'] >= 80
    kpi_bugs     = test_summary['failed'] == 0
    
    print(f"\n  KPI CHECK:")
    print(f"  {'✅' if kpi_coverage else '❌'} Coverage ≥ 80%  →  {test_summary['coverage_percent']}%")
    print(f"  {'✅' if kpi_bugs else '❌'} Zero failures   →  {test_summary['failed']} failed")
    print("\n" + "="*60 + "\n")

    return {
        "test_summary": test_summary,
        "api_summary": api_summary,
        "github_issues": github_issues,
        "report_path": report_path
    }


if __name__ == "__main__":
    run_qa_agent()