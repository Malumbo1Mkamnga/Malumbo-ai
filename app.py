import streamlit as st
import pandas as pd
from docx import Document
import PyPDF2
from duckduckgo_search import DDGS
import io

# ============================================================
# MALUMBO AI ASSISTANT
# ============================================================

st.set_page_config(
    page_title="MALUMBO AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MALUMBO AI ASSISTANT")
st.markdown(
    "### *Your Academic, Research & Business Copilot - Forever Online*"
)

st.markdown(
    "Upload PDFs, DOCX, CSVs, search the web, chat with documents, "
    "write academic work and create presentation content."
)

st.divider()

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "1. Multi-File Chat",
        "2. Academic Writing",
        "3. Presentation Generator"
    ]
)

# ============================================================
# TAB 1: MULTI-FILE CHAT
# ============================================================

with tab1:

    st.header("📁 Upload & Chat With Your Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX or CSV files",
        type=["pdf", "docx", "csv"],
        accept_multiple_files=True
    )

    context = ""

    if uploaded_files:

        for file in uploaded_files:

            # ---------------- PDF ----------------
            if file.name.lower().endswith(".pdf"):

                try:
                    reader = PyPDF2.PdfReader(file)

                    for page in reader.pages:

                        text = page.extract_text()

                        if text:
                            context += "\n" + text

                except Exception as e:
                    st.error(
                        f"Could not read {file.name}: {e}"
                    )

            # ---------------- DOCX ----------------
            elif file.name.lower().endswith(".docx"):

                try:
                    doc = Document(file)

                    for paragraph in doc.paragraphs:
                        context += "\n" + paragraph.text

                except Exception as e:
                    st.error(
                        f"Could not read {file.name}: {e}"
                    )

            # ---------------- CSV ----------------
            elif file.name.lower().endswith(".csv"):

                try:
                    df = pd.read_csv(file)

                    st.subheader(f"📊 {file.name}")
                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    context += "\n" + df.to_string()

                except Exception as e:
                    st.error(
                        f"Could not read {file.name}: {e}"
                    )

        st.success(
            f"✅ Successfully loaded {len(uploaded_files)} file(s)!"
        )

    st.divider()

    query = st.text_input(
        "Ask something about your files or search the web:"
    )

    col1, col2 = st.columns(2)

    # ========================================================
    # WEB SEARCH
    # ========================================================

    with col1:

        if st.button(
            "🌐 Search Web",
            use_container_width=True
        ):

            if query:

                with st.spinner("Searching the web..."):

                    try:

                        results = DDGS().text(
                            query,
                            max_results=5
                        )

                        results = list(results)

                        if results:

                            st.subheader("🌐 Search Results")

                            for result in results:

                                title = result.get(
                                    "title",
                                    "No title"
                                )

                                body = result.get(
                                    "body",
                                    ""
                                )

                                href = result.get(
                                    "href",
                                    ""
                                )

                                st.markdown(
                                    f"### {title}"
                                )

                                st.write(body)

                                if href:
                                    st.markdown(
                                        f"🔗 {href}"
                                    )

                                st.divider()

                        else:

                            st.warning(
                                "No search results found."
                            )

                    except Exception as e:

                        st.error(
                            f"Web search error: {e}"
                        )

            else:

                st.warning(
                    "Please enter a search question first."
                )

    # ========================================================
    # ANSWER FROM FILES
    # ========================================================

    with col2:

        if st.button(
            "📄 Answer From Files",
            use_container_width=True
        ):

            if not context:

                st.warning(
                    "Please upload at least one file first."
                )

            elif not query:

                st.warning(
                    "Please enter a question."
                )

            else:

                st.subheader("📄 Information From Your Files")

                st.write(
                    "Relevant document content:"
                )

                st.info(
                    context[:5000]
                )


# ============================================================
# TAB 2: ACADEMIC WRITING
# ============================================================

with tab2:

    st.header("✍️ Academic Writing Assistant")

    task = st.selectbox(
        "Task Type",
        [
            "Assignment Questions",
            "Essay",
            "Research Proposal",
            "Literature Review",
            "Research Report",
            "CV/Resume"
        ]
    )

    instructions = st.text_area(
        "Paste Assignment Instructions / Question Here",
        height=220
    )

    words = st.slider(
        "Target Word Count",
        250,
        5000,
        1000
    )

    academic_level = st.selectbox(
        "Academic Level",
        [
            "Certificate",
            "Diploma",
            "Undergraduate",
            "Postgraduate"
        ]
    )

    referencing = st.selectbox(
        "Referencing Style",
        [
            "APA 7th Edition",
            "Harvard",
            "MLA",
            "Chicago",
            "No Referencing"
        ]
    )

    if st.button(
        "🚀 Generate Academic Draft",
        use_container_width=True
    ):

        if instructions.strip():

            st.success(
                f"Ready to generate a {words}-word "
                f"{task} for {academic_level} level."
            )

            st.subheader("📝 Draft Structure")

            st.write(
                f"""
                **Task:** {task}

                **Academic Level:** {academic_level}

                **Target Words:** {words}

                **Referencing:** {referencing}

                **Instructions Provided:**

                {instructions}
                """
            )

            st.divider()

            st.markdown("### Suggested Academic Structure")

            if task == "Assignment Questions":

                st.write(
                    """
                    **1. Introduction**

                    Introduce the topic and explain the purpose
                    of the assignment.

                    **2. Main Discussion**

                    Address each assignment question clearly.
                    Use relevant concepts, theories, evidence and
                    examples.

                    **3. Critical Analysis**

                    Compare ideas, discuss strengths and weaknesses,
                    and provide evidence-based arguments.

                    **4. Conclusion**

                    Summarize the major findings and arguments.

                    **5. References**

                    Provide references using the selected
                    referencing style.
                    """
                )

            elif task == "Research Proposal":

                st.write(
                    """
                    **1. Introduction**

                    **2. Background of the Study**

                    **3. Problem Statement**

                    **4. Justification**

                    **5. Objectives**

                    **6. Research Questions / Hypotheses**

                    **7. Literature Review**

                    **8. Theoretical / Conceptual Framework**

                    **9. Methodology**

                    **10. Ethical Considerations**

                    **11. References**
                    """
                )

            elif task == "Essay":

                st.write(
                    """
                    **1. Introduction**

                    Present the topic, background and thesis.

                    **2. Body Paragraphs**

                    Develop the major arguments using evidence.

                    **3. Critical Discussion**

                    Compare different perspectives and evidence.

                    **4. Conclusion**

                    Summarize the argument and key findings.

                    **5. References**
                    """
                )

            elif task == "Literature Review":

                st.write(
                    """
                    **1. Introduction**

                    **2. Conceptual Review**

                    **3. Theoretical Review**

                    **4. Empirical Review**

                    **5. Critical Analysis of Previous Studies**

                    **6. Research Gap**

                    **7. Conclusion**

                    **8. References**
                    """
                )

            elif task == "Research Report":

                st.write(
                    """
                    **1. Introduction**

                    **2. Methodology**

                    **3. Results / Findings**

                    **4. Discussion**

                    **5. Conclusion**

                    **6. Recommendations**

                    **7. References**
                    """
                )

            else:

                st.write(
                    """
                    **Professional CV Structure**

                    - Personal / Contact Information
                    - Professional Profile
                    - Education
                    - Work / Attachment Experience
                    - Skills
                    - Research Experience
                    - Certifications
                    - References
                    """
                )

        else:

            st.warning(
                "⚠️ Please paste the assignment instructions first."
            )


# ============================================================
# TAB 3: PRESENTATION GENERATOR
# ============================================================

with tab3:

    st.header("🎤 Presentation Generator")

    st.markdown(
        "Create a structured academic presentation from your "
        "topic, assignment or research proposal."
    )

    presentation_title = st.text_input(
        "Presentation Title",
        placeholder="Example: Factors Affecting Adoption of Conservation Agriculture"
    )

    presentation_topic = st.text_area(
        "Paste your topic, assignment, research proposal or notes:",
        height=250
    )

    number_of_slides = st.slider(
        "Number of Slides",
        5,
        30,
        12
    )

    presentation_style = st.selectbox(
        "Presentation Style",
        [
            "Academic Defense",
            "Class Assignment",
            "Research Proposal",
            "Business Presentation",
            "General Presentation"
        ]
    )

    if st.button(
        "🎨 Generate Presentation",
        use_container_width=True
    ):

        if not presentation_title.strip():

            st.warning(
                "Please enter a presentation title."
            )

        elif not presentation_topic.strip():

            st.warning(
                "Please paste your topic or content."
            )

        else:

            st.success(
                f"✅ Creating a {number_of_slides}-slide "
                f"{presentation_style} structure."
            )

            st.divider()

            # =================================================
            # ACADEMIC DEFENSE
            # =================================================

            if presentation_style == "Academic Defense":

                slide_titles = [
                    "Title Page",
                    "Introduction",
                    "Background of the Study",
                    "Problem Statement",
                    "Justification of the Study",
                    "Research Objectives",
                    "Research Questions / Hypotheses",
                    "Literature Review",
                    "Theoretical Framework",
                    "Conceptual Framework",
                    "Methodology",
                    "Study Area",
                    "Sampling and Sample Size",
                    "Data Collection",
                    "Data Analysis",
                    "Ethical Considerations",
                    "Expected Results",
                    "Conclusion",
                    "Recommendations",
                    "References"
                ]

            # =================================================
            # RESEARCH PROPOSAL
            # =================================================

            elif presentation_style == "Research Proposal":

                slide_titles = [
                    "Title Page",
                    "Introduction",
                    "Background",
                    "Problem Statement",
                    "Justification",
                    "Main Objective",
                    "Specific Objectives",
                    "Research Questions",
                    "Literature Review",
                    "Research Gap",
                    "Theoretical Framework",
                    "Conceptual Framework",
                    "Methodology",
                    "Study Area",
                    "Research Design",
                    "Sampling",
                    "Data Collection",
                    "Data Analysis",
                    "Ethical Considerations",
                    "References"
                ]

            # =================================================
            # CLASS ASSIGNMENT
            # =================================================

            elif presentation_style == "Class Assignment":

                slide_titles = [
                    "Title Page",
                    "Introduction",
                    "Background",
                    "Key Concepts",
                    "Main Issue",
                    "Analysis",
                    "Evidence",
                    "Examples",
                    "Challenges",
                    "Possible Solutions",
                    "Recommendations",
                    "Conclusion",
                    "References"
                ]

            # =================================================
            # BUSINESS
            # =================================================

            elif presentation_style == "Business Presentation":

                slide_titles = [
                    "Title",
                    "Executive Summary",
                    "Background",
                    "Problem",
                    "Market / Situation Analysis",
                    "Proposed Solution",
                    "Technology / Strategy",
                    "Implementation Plan",
                    "Benefits",
                    "Risks and Challenges",
                    "Financial Considerations",
                    "Recommendations",
                    "Conclusion"
                ]

            # =================================================
            # GENERAL
            # =================================================

            else:

                slide_titles = [
                    "Title",
                    "Introduction",
                    "Background",
                    "Key Issues",
                    "Main Discussion",
                    "Analysis",
                    "Evidence",
                    "Examples",
                    "Challenges",
                    "Solutions",
                    "Recommendations",
                    "Conclusion",
                    "References"
                ]

            # Limit number of slides selected by user
            selected_titles = slide_titles[:number_of_slides]

            # If user selects more slides than available,
            # automatically add additional slides.
            while len(selected_titles) < number_of_slides:

                selected_titles.append(
                    f"Additional Discussion {len(selected_titles) + 1}"
                )

            # =================================================
            # DISPLAY SLIDES
            # =================================================

            for i, slide_title in enumerate(
                selected_titles,
                start=1
            ):

                st.subheader(
                    f"Slide {i}: {slide_title}"
                )

                if i == 1:

                    st.write(
                        f"**{presentation_title}**"
                    )

                    st.write(
                        "Name of Presenter"
                    )

                    st.write(
                        "Institution / Course / Date"
                    )

                elif slide_title == "Introduction":

                    st.markdown(
                        """
                        - Introduce the main topic.
                        - Explain the purpose of the presentation.
                        - Provide a brief overview of what will be discussed.
                        """
                    )

                elif slide_title == "Background of the Study" or slide_title == "Background":

                    st.markdown(
                        """
                        - Provide relevant background information.
                        - Explain the context of the problem.
                        - Present important evidence and statistics.
                        - Highlight why the topic is important.
                        """
                    )

                elif slide_title == "Problem Statement":

                    st.markdown(
                        """
                        - Explain the existing problem.
                        - Present evidence showing the magnitude of the problem.
                        - Identify weaknesses in previous knowledge or interventions.
                        - State the research gap.
                        """
                    )

                elif slide_title == "Justification of the Study" or slide_title == "Justification":

                    st.markdown(
                        """
                        - Explain why the study is necessary.
                        - Identify who will benefit from the study.
                        - Explain the expected contribution of the research.
                        """
                    )

                elif slide_title == "Research Objectives" or slide_title == "Specific Objectives":

                    st.markdown(
                        """
                        - Main objective
                        - Specific objective 1
                        - Specific objective 2
                        - Specific objective 3
                        """
                    )

                elif slide_title == "Research Questions / Hypotheses" or slide_title == "Research Questions":

                    st.markdown(
                        """
                        - Research Question 1
                        - Research Question 2
                        - Research Question 3
                        - Corresponding hypotheses where applicable
                        """
                    )

                elif slide_title == "Literature Review":

                    st.markdown(
                        """
                        - Review relevant concepts.
                        - Present theoretical perspectives.
                        - Discuss empirical evidence.
                        - Compare findings from previous studies.
                        - Identify limitations and gaps.
                        """
                    )

                elif slide_title == "Research Gap":

                    st.markdown(
                        """
                        - What previous studies have established.
                        - What previous studies have not adequately addressed.
                        - How the current study addresses the gap.
                        """
                    )

                elif slide_title == "Theoretical Framework":

                    st.markdown(
                        """
                        - Present the theory guiding the study.
                        - Explain the main concepts of the theory.
                        - Show how the theory relates to the research problem.
                        """
                    )

                elif slide_title == "Conceptual Framework":

                    st.markdown(
                        """
                        **Independent Variables**
                        
                        ↓
                        
                        **Factors influencing the outcome**
                        
                        ↓
                        
                        **Dependent Variable**
                        
                        Explain the expected relationships among variables.
                        """
                    )

                elif slide_title == "Methodology":

                    st.markdown(
                        """
                        - Research design
                        - Study population
                        - Study area
                        - Sampling procedure
                        - Data sources
                        - Data collection methods
                        - Data analysis methods
                        """
                    )

                elif slide_title == "Study Area":

                    st.markdown(
                        """
                        - Location of the study
                        - Population
                        - Main economic activities
                        - Agricultural characteristics
                        - Relevant environmental conditions
                        """
                    )

                elif slide_title == "Sampling and Sample Size" or slide_title == "Sampling":

                    st.markdown(
                        """
                        - Target population
                        - Sampling technique
                        - Sample size
                        - Inclusion criteria
                        """
                    )

                elif slide_title == "Data Collection":

                    st.markdown(
                        """
                        - Primary data
                        - Secondary data
                        - Questionnaires
                        - Interviews / focus groups where applicable
                        """
                    )

                elif slide_title == "Data Analysis":

                    st.markdown(
                        """
                        - Descriptive statistics
                        - Econometric analysis where applicable
                        - Hypothesis testing
                        - Statistical software
                        """
                    )

                elif slide_title == "Ethical Considerations":

                    st.markdown(
                        """
                        - Informed consent
                        - Confidentiality
                        - Voluntary participation
                        - Protection of respondents
                        - Permission from relevant authorities
                        """
                    )

                elif slide_title == "Conclusion":

                    st.markdown(
                        """
                        - Summarize the main findings or expected contribution.
                        - Link the conclusion to the objectives.
                        - Highlight the importance of the study.
                        """
                    )

                elif slide_title == "Recommendations":

                    st.markdown(
                        """
                        - Recommendation 1
                        - Recommendation 2
                        - Recommendation 3
                        - Areas for further research
                        """
                    )

                elif slide_title == "References":

                    st.markdown(
                        """
                        - Include all sources cited in the presentation.
                        - Use the required referencing style.
                        - Prioritize recent and credible academic sources.
                        """
                    )

                else:

                    st.markdown(
                        f"""
                        - Key point related to **{slide_title}**
                        - Supporting evidence
                        - Relevant example
                        - Important explanation
                        """
                    )

                st.divider()

            # =================================================
            # ORIGINAL CONTENT
            # =================================================

            st.subheader("📚 Source Content Provided")

            st.info(
                presentation_topic[:5000]
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    ### 🧠 MALUMBO AI
    **Academic • Research • Business • Agriculture**

    Built to help students and researchers work smarter.
    """
)
