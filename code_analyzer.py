
import ast
import json
import subprocess
import sys
import tempfile
import os


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

    # 1. Syntax checking
    try:
        ast.parse(source_code)
    except SyntaxError as error:
        results["syntax_error"] = (
            f"Line {error.lineno}: {error.msg}"
        )
        return results

    # Create a temporary Python file
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        encoding="utf-8",
        delete=False
    ) as temp_file:
        temp_file.write(source_code)
        file_path = temp_file.name

    try:
        # 2. Code quality analysis using Pylint
        if check_quality:
            try:
                process = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pylint",
                        "--output-format=json",
                        file_path
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                issues = json.loads(process.stdout or "[]")

                for issue in issues:
                    results["quality_issues"].append({
                        "message": issue.get("message", ""),
                        "line": issue.get("line", "N/A"),
                        "symbol": issue.get("symbol", "")
                    })

            except subprocess.TimeoutExpired:
                results["quality_issues"].append({
                    "message": "Pylint analysis timed out.",
                    "line": "N/A"
                })

            except (json.JSONDecodeError, OSError):
                results["quality_issues"].append({
                    "message": "Unable to complete Pylint analysis.",
                    "line": "N/A"
                })

        # 3. Security analysis using Bandit
        if check_security:
            try:
                process = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "bandit",
                        "-f",
                        "json",
                        file_path
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                report = json.loads(process.stdout or "{}")

                for issue in report.get("results", []):
                    results["security_issues"].append({
                        "issue": issue.get("issue_text", ""),
                        "line": issue.get("line_number", "N/A"),
                        "severity": issue.get("issue_severity", ""),
                        "confidence": issue.get("issue_confidence", "")
                    })

            except subprocess.TimeoutExpired:
                results["security_issues"].append({
                    "issue": "Bandit analysis timed out.",
                    "line": "N/A"
                })

            except (json.JSONDecodeError, OSError):
                results["security_issues"].append({
                    "issue": "Unable to complete Bandit analysis.",
                    "line": "N/A"
                })

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return results
