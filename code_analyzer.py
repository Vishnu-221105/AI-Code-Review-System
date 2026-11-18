
import ast
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor


ANALYSIS_TIMEOUT = 15


def run_pylint(file_path):
    try:
        process = subprocess.run(
            [
                sys.executable,
                "-m", "pylint",
                "--output-format=json",
                file_path
            ],
            capture_output=True,
            text=True,
            timeout=ANALYSIS_TIMEOUT
        )

        issues = json.loads(process.stdout or "[]")

        return [
            {
                "message": issue.get("message", ""),
                "line": issue.get("line", "N/A"),
                "symbol": issue.get("symbol", "")
            }
            for issue in issues
        ]

    except subprocess.TimeoutExpired:
        return [{
            "message": "Pylint analysis timed out.",
            "line": "N/A"
        }]

    except (json.JSONDecodeError, OSError) as error:
        return [{
            "message": f"Pylint error: {error}",
            "line": "N/A"
        }]


def run_bandit(file_path):
    try:
        process = subprocess.run(
            [
                sys.executable,
                "-m", "bandit",
                "-f", "json",
                file_path
            ],
            capture_output=True,
            text=True,
            timeout=ANALYSIS_TIMEOUT
        )

        report = json.loads(process.stdout or "{}")

        return [
            {
                "issue": issue.get("issue_text", ""),
                "line": issue.get("line_number", "N/A"),
                "severity": issue.get("issue_severity", ""),
                "confidence": issue.get("issue_confidence", "")
            }
            for issue in report.get("results", [])
        ]

    except subprocess.TimeoutExpired:
        return [{
            "issue": "Bandit analysis timed out.",
            "line": "N/A"
        }]

    except (json.JSONDecodeError, OSError) as error:
        return [{
            "issue": f"Bandit error: {error}",
            "line": "N/A"
        }]


def analyze_code(
    source_code,
    check_quality=True,
    check_security=True
):
    results = {
        "syntax_error": None,
        "quality_issues": [],
        "security_issues": []
    }

    # Step 1: Syntax analysis
    try:
        ast.parse(source_code)
    except SyntaxError as error:
        results["syntax_error"] = (
            f"Line {error.lineno}: {error.msg}"
        )
        return results

    # Step 2: Create temporary file
    file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            encoding="utf-8",
            delete=False
        ) as temp_file:
            temp_file.write(source_code)
            file_path = temp_file.name

        # Step 3: Run selected analyses concurrently
        with ThreadPoolExecutor(max_workers=2) as executor:

            pylint_future = None
            bandit_future = None

            if check_quality:
                pylint_future = executor.submit(
                    run_pylint, file_path
                )

            if check_security:
                bandit_future = executor.submit(
                    run_bandit, file_path
                )

            if pylint_future:
                results["quality_issues"] = (
                    pylint_future.result()
                )

            if bandit_future:
                results["security_issues"] = (
                    bandit_future.result()
                )

    except OSError as error:
        results["quality_issues"].append({
            "message": f"Analysis error: {error}",
            "line": "N/A"
        })

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    return results
