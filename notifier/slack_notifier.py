import os
from dotenv import load_dotenv

load_dotenv()

def send_slack_notification(test_summary, api_summary, github_issues=None, report_path=None):
    """Send a QA digest to Slack. Skips cleanly if no token is configured."""
    
    token = os.getenv("SLACK_BOT_TOKEN")
    channel = os.getenv("SLACK_CHANNEL", "#qa-reports")
    
    if not token:
        print("⚠️  SLACK_BOT_TOKEN not set — skipping Slack notification")
        return False
    
    try:
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError
        
        client = WebClient(token=token)
        
        # Build the message
        passed = test_summary.get("passed", 0)
        total  = test_summary.get("total", 0)
        failed = test_summary.get("failed", 0)
        coverage = test_summary.get("coverage_percent", 0)
        api_passed = api_summary.get("passed", 0)
        api_total  = api_summary.get("total", 0)
        timestamp  = test_summary.get("timestamp", "N/A")
        
        status_emoji = "✅" if failed == 0 else "🚨"
        coverage_emoji = "🟢" if coverage >= 80 else "🟡"
        
        message = f"""{status_emoji} *QA Agent Report* — {timestamp}

*Unit Tests:* {passed}/{total} passed {"✅" if failed == 0 else f"❌ {failed} failed"}
*API Tests:* {api_passed}/{api_total} passed
{coverage_emoji} *Coverage:* {coverage}%"""

        if failed > 0:
            message += f"\n\n🐛 *Failures detected:*"
            for f in test_summary.get("failures", []):
                name = f["name"].split("::")[-1]
                message += f"\n  • `{name}`"
        
        if github_issues:
            message += f"\n\n📎 *GitHub Issues created:*"
            for url in github_issues:
                message += f"\n  • {url}"
        
        if report_path:
            message += f"\n\n📄 *Report:* `{report_path}`"
        
        # Send it
        response = client.chat_postMessage(channel=channel, text=message)
        print(f"✅ Slack notification sent to {channel}")
        return True
        
    except Exception as e:
        print(f"⚠️  Slack notification failed: {e}")
        return False


if __name__ == "__main__":
    # Test with dummy data
    dummy_test = {
        "timestamp": "2026-05-24 00:30:00",
        "total": 7, "passed": 7, "failed": 0,
        "coverage_percent": 100.0, "failures": []
    }
    dummy_api = {"total": 7, "passed": 7, "failed": 0}
    
    result = send_slack_notification(
        dummy_test, dummy_api,
        github_issues=["https://github.com/Devansh-Daga/qa-agent/issues/1"],
        report_path="qa_report.html"
    )
    
    if not result:
        print("\nTo enable Slack: add SLACK_BOT_TOKEN and SLACK_CHANNEL to your .env")
        print("Guide: https://api.slack.com/apps → Create App → Bot Token Scopes: chat:write")