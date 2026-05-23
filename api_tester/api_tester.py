import requests
import json
from datetime import datetime

# We'll test against this free public API — no key needed
BASE_URL = "https://jsonplaceholder.typicode.com"

def test_endpoint(method, url, expected_status, payload=None, description=""):
    """Hit one endpoint and return pass/fail with details."""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=payload, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=payload, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        passed = response.status_code == expected_status
        
        return {
            "description": description,
            "method": method,
            "url": url,
            "expected_status": expected_status,
            "actual_status": response.status_code,
            "passed": passed,
            "response_time_ms": round(response.elapsed.total_seconds() * 1000, 2),
            "response_preview": str(response.json())[:200] if response.content else ""
        }
    except Exception as e:
        return {
            "description": description,
            "method": method,
            "url": url,
            "expected_status": expected_status,
            "actual_status": 0,
            "passed": False,
            "response_time_ms": 0,
            "error": str(e)
        }

def run_api_tests():
    """Run all API test cases and return a summary."""
    
    print("\n" + "="*60)
    print("API Tester — Running endpoint checks")
    print("="*60 + "\n")
    
    test_cases = [
        ("GET",    f"{BASE_URL}/posts/1",    200, None,                          "Fetch single post"),
        ("GET",    f"{BASE_URL}/posts",      200, None,                          "Fetch all posts"),
        ("POST",   f"{BASE_URL}/posts",      201, {"title": "QA Test", "body": "test", "userId": 1}, "Create a post"),
        ("PUT",    f"{BASE_URL}/posts/1",    200, {"title": "Updated", "body": "updated", "userId": 1}, "Update a post"),
        ("DELETE", f"{BASE_URL}/posts/1",    200, None,                          "Delete a post"),
        ("GET",    f"{BASE_URL}/users/1",    200, None,                          "Fetch a user"),
        ("GET",    f"{BASE_URL}/posts/9999", 404, None,                          "404 on missing resource"),
    ]
    
    results = []
    for method, url, expected_status, payload, description in test_cases:
        result = test_endpoint(method, url, expected_status, payload, description)
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"{status} | {method:6} | {result['actual_status']} | {result['response_time_ms']}ms | {description}")
        results.append(result)
    
    # Summary
    total  = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    
    print(f"\n{'='*60}")
    print(f"API Tests: {passed}/{total} passed | {failed} failed")
    print(f"{'='*60}\n")
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results
    }

if __name__ == "__main__":
    summary = run_api_tests()
    print(json.dumps(summary, indent=2))