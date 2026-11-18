
import streamlit as st
import time
import re
import html

from code_analyzer import analyze_code
from ai_reviewer import review_code_with_ai


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CodeGuard AI | Code Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0B1020;
    color: #E5E7EB;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #10182A;
    border-right: 1px solid #202C42;
}

[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    max-width: 1450px;
}

.brand {
    font-size: 23px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #F8FAFC;
}

.brand span {
    color: #60A5FA;
}

.eyebrow {
    color: #60A5FA;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    color: #F8FAFC;
    margin-top: 8px;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 15px;
    color: #94A3B8;
}

.panel {
    background: #121D31;
    border: 1px solid #25344D;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 16px;
}

.panel-title {
    font-size: 18px;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 5px;
}

.panel-subtitle {
    font-size: 13px;
    color: #94A3B8;
}

.metric-card {
    background: linear-gradient(145deg, #17243A, #111B2D);
    border: 1px solid #2A3A55;
    border-radius: 14px;
    padding: 18px;
    min-height: 120px;
}

.metric-label {
    font-size: 12px;
    color: #94A3B8;
    font-weight: 600;
}

.metric-value {
    font-size: 27px;
    font-weight: 800;
    color: #F8FAFC;
    margin-top: 8px;
}

.metric-note {
    color: #94A3B8;
    font-size: 11px;
    margin-top: 3px;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #34D399;
    border-radius: 50%;
    margin-right: 7px;
}

.stButton > button {
    border-radius: 9px;
    font-weight: 700;
    min-height: 44px;
    transition: 0.2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #2563EB, #6366F1);
    border: none;
    color: white;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #1D4ED8, #4F46E5);
    border: none;
}

div[data-testid="stTabs"] button {
    font-weight: 600;
    color: #94A3B8;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #60A5FA;
}

textarea {
    background-color: #0D1525 !important;
}

[data-testid="stFileUploader"] {
    background: #111D31;
    border: 1px dashed #3B82F6;
    border-radius: 12px;
    padding: 12px;
}

hr {
    border-color: #26344B;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">🛡️ CODEGUARD<span> AI</span></div>',
        unsafe_allow_html=True
    )

    st.caption("INTELLIGENT CODE ANALYSIS")

    st.divider()

    st.markdown("### Workspace")

    st.markdown("🔍  Code Review")
    st.markdown("📊  Analysis Report")
    st.markdown("🤖  AI Assistant")

    st.divider()

    st.markdown("### ⚙️ Review Configuration")

    check_quality = st.toggle(
        "Code Quality Analysis",
        value=True
    )

    check_security = st.toggle(
        "Security Analysis",
        value=True
    )

    check_ai = st.toggle(
        "AI-Powered Review",
        value=True
    )

    st.divider()

    st.markdown("### 🔧 Analysis Engines")

    st.caption("AST  ·  Syntax Validation")
    st.caption("Pylint  ·  Code Quality")
    st.caption("Bandit  ·  Security")
    st.caption("Groq  ·  AI Review")

    st.divider()

    st.markdown(
        '<span class="status-dot"></span> System ready',
        unsafe_allow_html=True
    )

    st.caption("Version 2.0 · Python only")


# =====================================================
# HEADER
# =====================================================

header_left, header_right = st.columns([5, 1])

with header_left:

    st.markdown(
        '<div class="eyebrow">AI DEVELOPER TOOLKIT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-title">Intelligent Code Review</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Analyze code quality, identify vulnerabilities, '
        'and improve your Python code with AI.'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        '<div style="text-align:right;padding-top:20px;">'
        '<span class="status-dot"></span>'
        '<span style="color:#34D399;font-size:12px;">ONLINE</span>'
        '</div>',
        unsafe_allow_html=True
    )

st.divider()


# =====================================================
# CODE WORKSPACE
# =====================================================

left, right = st.columns([1.5, 1], gap="large")

default_code = '''def divide(a, b):
    return a / b

print(divide(10, 0))
'''

with left:

    st.markdown(
        '<div class="panel-title">📝 Code Workspace</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-subtitle">'
        'Write your Python code or upload an existing file.'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload a Python file",
        type=["py"]
    )

    if uploaded_file is not None:

        uploaded_code = uploaded_file.getvalue().decode(
            "utf-8",
            errors="replace"
        )

    else:
        uploaded_code = default_code

    source_code = st.text_area(
        "Python Editor",
        value=uploaded_code,
        height=310,
        label_visibility="collapsed",
        placeholder="Write your Python code here..."
    )

with right:

    st.markdown(
        '<div class="panel-title">⚡ Review Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-subtitle">'
        'Your code will be checked using these engines.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="panel">
        <div style="color:#60A5FA;font-weight:700;">
            ◈ SYNTAX VALIDATION
        </div>
        <div style="color:#94A3B8;font-size:13px;margin-top:6px;">
            Detect Python syntax errors.
        </div>
        <hr>
        <div style="color:#A78BFA;font-weight:700;">
            ◈ CODE QUALITY
        </div>
        <div style="color:#94A3B8;font-size:13px;margin-top:6px;">
            Find coding standards and maintainability issues.
        </div>
        <hr>
        <div style="color:#34D399;font-weight:700;">
            ◈ SECURITY SCANNING
        </div>
        <div style="color:#94A3B8;font-size:13px;margin-top:6px;">
            Identify potentially unsafe code patterns.
        </div>
        <hr>
        <div style="color:#FBBF24;font-weight:700;">
            ◈ AI CODE REVIEW
        </div>
        <div style="color:#94A3B8;font-size:13px;margin-top:6px;">
            Generate explanations and improvement suggestions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("Your submitted code is analyzed, not executed.")


st.write("")

review_clicked = st.button(
    "🚀  Start Intelligent Code Review",
    type="primary",
    use_container_width=True
)


# =====================================================
# RUN ANALYSIS
# =====================================================

if review_clicked:

    if not source_code.strip():

        st.warning("Please enter or upload Python code.")

    else:

        start_time = time.time()

        results = None
        ai_result = None

        with st.spinner("Running code analysis..."):

            try:

                results = analyze_code(
                    source_code,
                    check_quality=check_quality,
                    check_security=check_security
                )

                if check_ai and not results["syntax_error"]:

                    ai_result = review_code_with_ai(source_code)

            except Exception as error:

                st.error(f"Analysis failed: {error}")
                st.stop()

        elapsed_time = time.time() - start_time

        # =============================================
        # REPORT HEADER
        # =============================================

        st.divider()

        st.markdown(
            '<div class="eyebrow">ANALYSIS RESULTS</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="hero-title" style="font-size:29px;">'
            'Code Review Report'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            f"Completed in {elapsed_time:.2f} seconds"
        )

        # =============================================
        # METRICS
        # =============================================

        quality_count = len(results["quality_issues"])
        security_count = len(results["security_issues"])

        syntax_value = (
            "Failed" if results["syntax_error"] else "Passed"
        )

        metric_columns = st.columns(4)

        metric_data = [
            ("SYNTAX CHECK", syntax_value, "AST validation"),
            (
                "QUALITY ISSUES",
                str(quality_count) if check_quality else "Off",
                "Pylint analysis"
            ),
            (
                "SECURITY ISSUES",
                str(security_count) if check_security else "Off",
                "Bandit analysis"
            ),
            (
                "AI REVIEW",
                "Ready" if ai_result and not ai_result.startswith("ERROR:") else (
                    "Error" if ai_result and ai_result.startswith("ERROR:") else (
                        "Off" if not check_ai else "Pending"
                    )
                ),
                "Groq analysis"
            )
        ]

        for column, data in zip(metric_columns, metric_data):

            with column:

                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{data[0]}</div>
                        <div class="metric-value">{html.escape(data[1])}</div>
                        <div class="metric-note">{data[2]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.write("")

        # =============================================
        # REPORT TABS
        # =============================================

        tab1, tab2, tab3, tab4 = st.tabs([
            "01  Syntax",
            "02  Quality",
            "03  Security",
            "04  AI Review"
        ])

        # =============================================
        # SYNTAX
        # =============================================

        with tab1:

            st.subheader("Syntax Validation")

            if results["syntax_error"]:

                st.error(results["syntax_error"])

            else:

                st.success("Your Python code passed syntax validation.")

        # =============================================
        # QUALITY
        # =============================================

        with tab2:

            st.subheader("Code Quality Analysis")

            if not check_quality:

                st.info("Code quality analysis is disabled.")

            elif results["quality_issues"]:

                for issue in results["quality_issues"]:

                    message = issue.get("message", "Issue detected")
                    line = issue.get("line", "N/A")

                    st.warning(
                        f"**Line {line}** — {message}"
                    )

            else:

                st.success("No code quality issues reported.")

        # =============================================
        # SECURITY
        # =============================================

        with tab3:

            st.subheader("Security Analysis")

            if not check_security:

                st.info("Security analysis is disabled.")

            elif results["security_issues"]:

                for issue in results["security_issues"]:

                    message = issue.get(
                        "issue",
                        "Security issue detected"
                    )

                    line = issue.get("line", "N/A")
                    severity = issue.get("severity", "N/A")
                    confidence = issue.get("confidence", "N/A")

                    st.error(
                        f"**Line {line}** — {message}"
                    )

                    st.caption(
                        f"Severity: {severity} | Confidence: {confidence}"
                    )

            else:

                st.success("No security issues reported by Bandit.")

        # =============================================
       
        # =============================================
        # AI REVIEW
        # =============================================

        with tab4:

            st.subheader("AI-Powered Code Review")

            if not check_ai:
                st.info("AI review is disabled.")

            elif results["syntax_error"]:
                st.warning(
                    "Please correct syntax errors before AI review."
                )

            elif not ai_result:
                st.warning("AI review did not return a result.")

            elif ai_result.startswith("ERROR:"):
                st.error(ai_result)

            else:
                # Identify numbered AI review sections
                heading_pattern = (
                    r"(?m)^\s*(?:#{1,6}\s*)?"
                    r"(\d+)[.)]\s*(.+?)\s*$"
                )

                headings = list(
                    re.finditer(heading_pattern, ai_result)
                )

                if not headings:
                    st.markdown(ai_result)

                else:
                    corrected_code = None

                    for index, heading in enumerate(headings):

                        section_title = heading.group(2).strip()

                        start = heading.end()

                        end = (
                            headings[index + 1].start()
                            if index + 1 < len(headings)
                            else len(ai_result)
                        )

                        section_content = ai_result[start:end].strip()

                        with st.container(border=True):

                            st.markdown(f"### {section_title}")

                            code_match = re.search(
                                r"```(?:python)?\s*(.*?)```",
                                section_content,
                                re.DOTALL | re.IGNORECASE
                            )

                            is_code_section = (
                                "CORRECTED CODE" in section_title.upper()
                                or "IMPROVED PYTHON CODE" in section_title.upper()
                            )

                            if is_code_section and code_match:

                                corrected_code = code_match.group(1).strip()

                                st.code(
                                    corrected_code,
                                    language="python"
                                )

                            else:
                                st.markdown(section_content)

                    if corrected_code:

                        st.divider()

                        st.markdown("## 🛠️ Improved Python Code")

                        st.caption(
                            "AI-generated corrected version of your submitted code."
                        )

                        st.code(
                            corrected_code,
                            language="python"
                        )

                        st.download_button(
                            "⬇️ Download Improved Code",
                            data=corrected_code,
                            file_name="improved_code.py",
                            mime="text/x-python",
                            use_container_width=True
                        )

                st.divider()

                with st.expander("📄 View Original Submitted Code"):
                    st.code(source_code, language="python")

                st.success("Analysis process completed.")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#64748B;font-size:12px;">
        CODEGUARD AI · Intelligent Python Code Analysis
        <br>
        Built with Python, Streamlit, Pylint, Bandit and Groq
    </div>
    """,
    unsafe_allow_html=True
)
