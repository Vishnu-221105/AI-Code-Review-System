
import streamlit as st
from code_analyzer import analyze_code
from ai_reviewer import review_code_with_ai

st.set_page_config(
    page_title="AI Code Review System",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI-Powered Code Review System")
st.caption("Intelligent Python Code Analysis and AI Review")

st.divider()

with st.sidebar:
    st.header("⚙️ Review Settings")

    check_quality = st.checkbox(
        "Code Quality Analysis", value=True
    )

    check_security = st.checkbox(
        "Security Analysis", value=True
    )

    check_ai = st.checkbox(
        "AI-Powered Review", value=True
    )

    st.divider()
    st.info("Supported language: Python")

st.subheader("Submit Your Python Code")

uploaded_file = st.file_uploader(
    "Upload a Python file (.py)",
    type=["py"]
)

default_code = '''def divide(a, b):
    return a / b

print(divide(10, 0))
'''

if uploaded_file is not None:
    code = uploaded_file.getvalue().decode(
        "utf-8", errors="replace"
    )
else:
    code = default_code

source_code = st.text_area(
    "Enter your Python code:",
    value=code,
    height=300
)

if st.button(
    "🔍 Review Code",
    type="primary",
    use_container_width=True
):

    if not source_code.strip():
        st.warning("Please enter or upload Python code.")

    else:

        with st.spinner("Analysing your code..."):
            results = analyze_code(
                source_code,
                check_quality=check_quality,
                check_security=check_security
            )

        st.divider()
        st.header("📊 Code Review Report")

        # Syntax analysis
        st.subheader("1. Syntax Analysis")

        if results["syntax_error"]:
            st.error(results["syntax_error"])
        else:
            st.success("No syntax errors detected.")

        # Quality analysis
        if check_quality:
            st.subheader("2. Code Quality Analysis")

            issues = results["quality_issues"]

            if issues:
                for issue in issues:
                    st.warning(
                        f'{issue.get("message", "Issue detected")} '
                        f'(Line: {issue.get("line", "N/A")})'
                    )
            else:
                st.success("No code quality issues reported.")

        # Security analysis
        if check_security:
            st.subheader("3. Security Analysis")

            issues = results["security_issues"]

            if issues:
                for issue in issues:
                    st.error(
                        f'{issue.get("issue", "Security issue detected")} '
                        f'(Line: {issue.get("line", "N/A")})'
                    )
            else:
                st.success("No security issues reported.")

        # AI review
        if check_ai:
            st.divider()
            st.subheader("4. 🤖 AI-Powered Code Review")

            if results["syntax_error"]:
                st.warning(
                    "Fix the syntax errors before requesting AI review."
                )
            else:
                with st.spinner(
                    "Gemini AI is reviewing your code..."
                ):
                    ai_result = review_code_with_ai(source_code)

                if ai_result.startswith("ERROR:"):
                    st.error(ai_result)
                else:
                    st.markdown(ai_result)

        # Submitted code
        with st.expander("View Submitted Code"):
            st.code(source_code, language="python")

        st.success("Code analysis completed!")
