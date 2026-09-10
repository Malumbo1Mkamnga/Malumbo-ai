import streamlit as st
import PyPDF2
from docx import Document
from duckduckgo_search import DDGS

# ============================================================
# MALUMBO AI - MALAWI SMART ASSISTANT
# ============================================================

st.set_page_config(
    page_title="MALUMBO AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MALUMBO AI - Malawi Smart Assistant")
st.write("🇲🇼 Your smart academic, document and Malawi information assistant")

# ============================================================
# TABS
# ============================================================

tabs = st.tabs([
    "1. Multi-File Chat",
    "2. Academic Writing",
    "3. Presentation Generator"
])

# ============================================================
# SMART SEARCH FUNCTION
# ============================================================

def smart_search(query):

    # Add Malawi automatically
    if "malawi" not in query.lower():
        query = query + " Malawi"

    # Prioritize Malawi news websites
    search_query = (
        query
        + " 2026 "
        + "(site:nyasatimes.com OR "
          "site:malawi24.com OR "
          "site:times.mw)"
    )

    results = []

    try:
        with DDGS() as ddgs:

            search_results = ddgs.text(
                search_query,
                max_results=5
            )

            for r in search_results:

                title = r.get("title", "No title")
                href = r.get("href", "")
                body = r.get("body", "")

                results.append(
                    f"**{title}**\n\n"
                    f"[Open source]({href})\n\n"
                    f"{body}"
                )

    except Exception as e:

        results = [
            "⚠️ Web search failed.",
            "I can still help using the information available to me."
        ]

    # If there are no search results
    if not results:

        results = [
            "⚠️ I could not find suitable web results.",
            "Try another search question."
        ]

    return results


# ============================================================
# FILE READER
# ============================================================

def read_file(uploaded_file):

    text = ""

    try:

        # ---------------- PDF ----------------
        if uploaded_file.name.lower().endswith(".pdf"):

            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        # ---------------- DOCX ----------------
        elif uploaded_file.name.lower().endswith(".docx"):

            doc = Document(uploaded_file)

            for para in doc.paragraphs:

                if para.text.strip():
                    text += para.text + "\n"

        # ---------------- CSV ----------------
        elif uploaded_file.name.lower().endswith(".csv"):

            text = uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

    except Exception as e:

        text = f"Could not read file: {e}"

    return text


# ============================================================
# TAB 1 - MULTI-FILE CHAT
# ============================================================

with tabs[0]:

    st.header("📁 Upload & Chat With Your Documents")

    st.write(
        "Upload PDF, DOCX or CSV files and ask questions about them."
    )

    uploaded_files = st.file_uploader(
        "Upload your files",
        accept_multiple_files=True,
        type=["pdf", "docx", "csv"]
    )

    # --------------------------------------------------------
    # SHOW UPLOADED FILES
    # --------------------------------------------------------

    if uploaded_files:

        st.success(
            f"✅ {len(uploaded_files)} file(s) uploaded successfully."
        )

        for file in uploaded_files:

            st.write(
                f"📄 **{file.name}**"
            )

    # --------------------------------------------------------
    # READ FILES
    # --------------------------------------------------------

    combined_text = ""

    if uploaded_files:

        for file in uploaded_files:

            file_text = read_file(file)

            combined_text += (
                "\n\n"
                + "=" * 60
                + "\n"
                + f"FILE: {file.name}"
                + "\n"
                + "=" * 60
                + "\n"
                + file_text
            )

    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    query = st.text_input(
        "Ask something about your files or search the web:",
        placeholder="Example: What is the main objective of this document?"
    )

    # --------------------------------------------------------
    # FILE CHAT
    # --------------------------------------------------------

    if uploaded_files and query:

        st.subheader("📖 Information From Your Files")

        query_lower = query.lower()

        # Simple keyword-based document search
        words = [
            word.strip(".,!?")
            for word in query_lower.split()
            if len(word.strip(".,!?")) > 3
        ]

        matching_sections = []

        for section in combined_text.split("=" * 60):

            section_lower = section.lower()

            score = sum(
                1 for word in words
                if word in section_lower
            )

            if score > 0:

                matching_sections.append(
                    (score, section)
                )

        matching_sections.sort(
            key=lambda x: x[0],
            reverse=True
        )

        if matching_sections:

            st.info(
                "🔎 I found information in your uploaded files."
            )

            shown = 0

            for score, section in matching_sections:

                if shown >= 3:
                    break

                st.write(section[:5000])

                st.divider()

                shown += 1

        else:

            st.warning(
                "I couldn't find an exact match in your uploaded files."
            )

    # --------------------------------------------------------
    # WEB SEARCH
    # --------------------------------------------------------

    if st.button("🔍 Search Malawi Web"):

        if query:

            with st.spinner(
                "🔎 Searching Malawi information..."
            ):

                results = smart_search(query)

                st.subheader(
                    "🌐 Web Search Results"
                )

                for result in results:

                    st.write(result)

                    st.divider()

        else:

            st.warning(
                "Please enter a question first."
            )


# ============================================================
# TAB 2 - ACADEMIC WRITING
# ============================================================

with tabs[1]:

    st.header("🎓 Academic Writing Assistant")

    st.write(
        "Use MALUMBO AI to organize your academic work, "
        "research ideas and assignments."
    )

    topic = st.text_input(
        "Enter your academic topic:",
        placeholder="Example: Factors affecting adoption of conservation agriculture"
    )

    academic_type = st.selectbox(
        "What do you want to create?",
        [
            "Introduction",
            "Problem Statement",
            "Justification",
            "Objectives",
            "Research Questions",
            "Literature Review",
            "Methodology",
            "Conclusion",
            "Assignment Outline"
        ]
    )

    if st.button("✍️ Generate Academic Structure"):

        if topic:

            st.subheader(
                f"📚 {academic_type}"
            )

            if academic_type == "Introduction":

                st.write(
                    f"""
                    **Topic:** {topic}

                    An introduction should provide the background
                    of the study, explain the importance of the
                    topic, describe the existing situation and
                    introduce the specific research problem.

                    The introduction should move from the broad
                    context to the specific study area and clearly
                    establish why the research is necessary.
                    """
                )

            elif academic_type == "Problem Statement":

                st.write(
                    f"""
                    **Topic:** {topic}

                    The problem statement should explain the
                    existing problem, provide evidence of its
                    magnitude, identify weaknesses in existing
                    knowledge and clearly show the research gap.

                    The final part should explain why the proposed
                    study is necessary.
                    """
                )

            elif academic_type == "Justification":

                st.write(
                    f"""
                    **Topic:** {topic}

                    The justification should explain why the study
                    is important and identify the groups or
                    institutions that may benefit from the findings.
                    """
                )

            elif academic_type == "Objectives":

                st.write(
                    f"""
                    **General Objective**

                    To investigate {topic}.

                    **Specific Objectives**

                    1. To examine the factors associated with {topic}.
                    2. To assess the effects associated with {topic}.
                    3. To identify possible measures for improving the situation.
                    """
                )

            elif academic_type == "Research Questions":

                st.write(
                    f"""
                    1. What factors influence {topic}?

                    2. What effects are associated with {topic}?

                    3. What measures can improve the situation?
                    """
                )

            elif academic_type == "Methodology":

                st.write(
                    f"""
                    A methodology section for **{topic}** should
                    normally describe:

                    • Study area

                    • Research design

                    • Target population

                    • Sampling procedure

                    • Sample size

                    • Data sources

                    • Data collection methods

                    • Variables

                    • Data analysis methods

                    • Econometric model, where applicable

                    • Ethical considerations
                    """
                )

            elif academic_type == "Literature Review":

                st.write(
                    f"""
                    The literature review for **{topic}** should
                    critically examine previous theoretical and
                    empirical studies.

                    It should identify:

                    • Major theories

                    • Previous empirical findings

                    • Methodologies used by previous researchers

                    • Areas of agreement and disagreement

                    • Limitations of previous studies

                    • The research gap addressed by the current study
                    """
                )

            elif academic_type == "Conclusion":

                st.write(
                    f"""
                    A conclusion for **{topic}** should summarize
                    the major findings, relate them to the research
                    objectives and provide appropriate implications
                    or recommendations.
                    """
                )

            else:

                st.write(
                    f"""
                    **Assignment topic:** {topic}

                    Recommended structure:

                    1. Introduction
                    2. Background
                    3. Main discussion
                    4. Evidence from literature
                    5. Critical analysis
                    6. Examples
                    7. Conclusion
                    8. References
                    """
                )

        else:

            st.warning(
                "Please enter an academic topic."
            )


# ============================================================
# TAB 3 - PRESENTATION GENERATOR
# ============================================================

with tabs[2]:

    st.header("📊 Presentation Generator")

    st.write(
        "Create a simple presentation structure from your topic."
    )

    presentation_topic = st.text_input(
        "Enter presentation topic:",
        placeholder="Example: Conservation Agriculture Adoption in Malawi"
    )

    number_slides = st.slider(
        "Number of slides",
        min_value=5,
        max_value=20,
        value=10
    )

    if st.button("🎯 Generate Presentation"):

        if presentation_topic:

            st.success(
                "✅ Presentation structure generated!"
            )

            slides = [
                ("Title", presentation_topic),

                (
                    "Introduction",
                    "Background and overview of the topic"
                ),

                (
                    "Problem Statement",
                    "Key problem, evidence and research gap"
                ),

                (
                    "Justification",
                    "Why the study or topic is important"
                ),

                (
                    "General Objective",
                    f"To investigate {presentation_topic}"
                ),

                (
                    "Specific Objectives",
                    "Present the major specific objectives"
                ),

                (
                    "Research Questions",
                    "Present the questions addressed by the study"
                ),

                (
                    "Literature Review",
                    "Theories and empirical evidence"
                ),

                (
                    "Methodology",
                    "Research design, sampling and data collection"
                ),

                (
                    "Data Analysis",
                    "Statistical and/or econometric methods"
                ),

                (
                    "Expected Findings",
                    "Expected results and implications"
                ),

                (
                    "Conclusion",
                    "Summary of the major points"
                ),

                (
                    "Recommendations",
                    "Practical recommendations"
                ),

                (
                    "References",
                    "Major sources used"
                )
            ]

            selected_slides = slides[:number_slides]

            for i, (title, content) in enumerate(
                selected_slides,
                start=1
            ):

                st.subheader(
                    f"Slide {i}: {title}"
                )

                st.write(
                    f"• {content}"
                )

                st.divider()

        else:

            st.warning(
                "Please enter a presentation topic."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🧠 MALUMBO AI | Built for Malawi 🇲🇼"
)

st.caption(
    "Academic • Documents • Web Search • Presentations"
)
