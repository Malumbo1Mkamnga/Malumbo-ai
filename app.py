import streamlit as st
import PyPDF2
from docx import Document
from duckduckgo_search import DDGS

# ============================================================
# MALUMBO AI v3.0 - GLOBAL BRAIN
# Global Web Search + Malawi Expertise + File Chat
# ============================================================

st.set_page_config(
    page_title="MALUMBO AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MALUMBO AI")
st.caption("🌍 Global AI Assistant with 🇲🇼 Malawi Expertise")

# ============================================================
# MALAWI KNOWLEDGE BASE
# ============================================================

MALAWI_KNOWLEDGE = {
    "president malawi": "As of 2026, the President of Malawi is **Peter Mutharika**.",
    "vice president malawi": "As of 2026, the Vice President of Malawi is **Jane Ansah**.",
    "capital malawi": "The capital city of Malawi is **Lilongwe**.",
    "currency malawi": "The currency of Malawi is the **Malawian kwacha (MWK)**.",
    "language malawi": "Malawi's official language is **English**, while **Chichewa** is widely spoken.",
}

# ============================================================
# FILE READER
# ============================================================

def read_file(file):
    text = ""

    try:
        if file.name.lower().endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:
                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

        elif file.name.lower().endswith(".docx"):
            doc = Document(file)

            for para in doc.paragraphs:
                if para.text.strip():
                    text += para.text + "\n"

        return text

    except Exception as e:
        return f"Could not read {file.name}: {e}"


# ============================================================
# WEB SEARCH
# ============================================================

def web_search(query, max_results=5):

    context = ""
    links = []

    try:
        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=max_results
            )

            for r in results:

                title = r.get("title", "Untitled source")
                body = r.get("body", "")
                href = r.get("href", "")

                context += (
                    f"Source: {title}\n"
                    f"{body}\n\n"
                )

                if href:
                    links.append(
                        f"- [{title}]({href})"
                    )

    except Exception as e:
        return "", [], str(e)

    return context, links, None


# ============================================================
# SMART AI SEARCH
# ============================================================

def ai_search(query):

    query_lower = query.lower().strip()

    # --------------------------------------------------------
    # 1. CHECK MALAWI KNOWLEDGE BASE
    # --------------------------------------------------------

    if "malawi" in query_lower:

        for key, answer in MALAWI_KNOWLEDGE.items():

            words = key.split()

            if all(word in query_lower for word in words):

                return (
                    f"### 🇲🇼 MALAWI ANSWER\n\n"
                    f"{answer}\n\n"
                    f"*Answered from MALUMBO AI's Malawi knowledge base.*"
                )

    # --------------------------------------------------------
    # 2. GLOBAL SEARCH
    # --------------------------------------------------------

    search_query = query

    # If Malawi is mentioned, boost Malawi without
    # restricting the search to Malawi-only websites.
    if "malawi" in query_lower:
        search_query = f"{query} Malawi"

    context, links, error = web_search(
        search_query,
        max_results=5
    )

    # --------------------------------------------------------
    # 3. SEARCH ERROR
    # --------------------------------------------------------

    if error:

        return (
            "### ⚠️ Web Search Problem\n\n"
            f"I could not complete the web search.\n\n"
            f"**Error:** `{error}`\n\n"
            "Try searching again in a few seconds."
        )

    # --------------------------------------------------------
    # 4. NO RESULTS
    # --------------------------------------------------------

    if not context:

        return (
            f"### 🔎 No Results Found\n\n"
            f"I couldn't find useful web results for:\n\n"
            f"**{query}**\n\n"
            "Try using different keywords."
        )

    # --------------------------------------------------------
    # 5. DISPLAY RESULTS
    # --------------------------------------------------------

    answer = (
        f"### 🌍 Results for: `{query}`\n\n"
        "I found the following information from the web:\n\n"
    )

    answer += context

    # --------------------------------------------------------
    # 6. SOURCES
    # --------------------------------------------------------

    if links:

        answer += "\n### 🔗 Sources\n\n"

        answer += "\n".join(links)

    return answer


# ============================================================
# PAGE TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "1. 🌍 Research & Chat",
        "2. ✍️ Academic Writing",
        "3. 📊 Presentation Generator"
    ]
)


# ============================================================
# TAB 1 - RESEARCH & CHAT
# ============================================================

with tab1:

    st.header("🌍 Research The Whole Internet")

    st.write(
        "Ask MALUMBO AI about Malawi, USA, UK, science, "
        "technology, agriculture, economics, politics, news, "
        "academic research and much more."
    )

    uploaded_files = st.file_uploader(
        "📎 Upload PDF or DOCX",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    file_context = ""

    if uploaded_files:

        st.success(
            f"📚 {len(uploaded_files)} file(s) uploaded."
        )

        for file in uploaded_files:

            with st.spinner(f"Reading {file.name}..."):

                extracted_text = read_file(file)

                file_context += (
                    f"\n\n===== FILE: {file.name} =====\n"
                    f"{extracted_text}\n"
                )

        with st.expander("📄 View uploaded file information"):

            for file in uploaded_files:
                st.write(
                    f"• **{file.name}**"
                )

    query = st.text_input(
        "Ask anything",
        placeholder=(
            "Example: latest AI research 2026, "
            "president of USA, climate change effects..."
        )
    )

    if st.button(
        "🔍 Search & Answer",
        use_container_width=True
    ):

        if not query:

            st.warning(
                "Please enter a question first."
            )

        else:

            with st.spinner(
                "🌍 Searching the global web..."
            ):

                # If files were uploaded, include their
                # content in the search context.
                if file_context:

                    st.markdown(
                        "### 📚 Uploaded Document Context"
                    )

                    # Limit displayed document text
                    # to prevent extremely large output.
                    display_context = file_context[:12000]

                    st.text_area(
                        "Document content",
                        display_context,
                        height=250
                    )

                st.markdown(
                    ai_search(query)
                )


# ============================================================
# TAB 2 - ACADEMIC WRITING
# ============================================================

with tab2:

    st.header("✍️ Academic Writing Assistant")

    st.write(
        "Create a basic academic structure for essays, "
        "assignments and research papers."
    )

    topic = st.text_input(
        "Essay / Research Paper Topic",
        key="academic_topic",
        placeholder="Enter your topic..."
    )

    level = st.selectbox(
        "Academic Level",
        [
            "High School",
            "University",
            "Masters"
        ]
    )

    academic_type = st.selectbox(
        "Type of Work",
        [
            "Essay",
            "Research Paper",
            "Assignment",
            "Research Proposal",
            "Literature Review"
        ]
    )

    if st.button(
        "📝 Generate Outline + Sources",
        use_container_width=True
    ):

        if not topic:

            st.warning(
                "Please enter an academic topic first."
            )

        else:

            st.markdown(
                f"""
### 📚 Academic Work

**Topic:** {topic}

**Level:** {level}

**Type:** {academic_type}

---

### Suggested Structure

**1. Introduction**

- Background of the study
- Problem statement
- Purpose of the study
- Objectives
- Research questions

**2. Literature Review**

- Key concepts
- Theoretical literature
- Empirical literature
- Research gap

**3. Methodology**

- Research design
- Study area
- Target population
- Sampling procedure
- Sample size
- Data collection
- Data analysis

**4. Results / Discussion**

- Presentation of findings
- Interpretation
- Comparison with previous studies

**5. Conclusion**

- Summary of findings
- Conclusions
- Recommendations

**6. References**

- Use appropriate academic sources
- Apply APA referencing where required
                """
            )

            st.info(
                "💡 Tip: Use the Research & Chat tab to "
                "search for current academic sources before "
                "writing your literature review."
            )


# ============================================================
# TAB 3 - PRESENTATION GENERATOR
# ============================================================

with tab3:

    st.header("📊 Presentation Generator")

    st.write(
        "Generate a simple presentation structure "
        "for academic or professional presentations."
    )

    pres_topic = st.text_input(
        "Presentation Topic",
        key="presentation_topic",
        placeholder="Example: Conservation Agriculture"
    )

    slides = st.slider(
        "Number of Slides",
        min_value=3,
        max_value=15,
        value=7
    )

    if st.button(
        "📊 Generate Slide Structure",
        use_container_width=True
    ):

        if not pres_topic:

            st.warning(
                "Please enter a presentation topic first."
            )

        else:

            st.markdown(
                f"## 📊 Presentation: {pres_topic}"
            )

            st.write(
                f"**Number of slides:** {slides}"
            )

            slide_titles = [
                "Title",
                "Introduction",
                "Background",
                "Problem Statement",
                "Objectives",
                "Literature Review",
                "Methodology",
                "Results",
                "Discussion",
                "Conclusion",
                "Recommendations",
                "References",
                "Questions & Answers",
                "Thank You"
            ]

            for i in range(slides):

                if i < len(slide_titles):

                    title = slide_titles[i]

                else:

                    title = f"Section {i + 1}"

                st.markdown(
                    f"""
### Slide {i + 1}: {title}

- Key point 1
- Key point 2
- Key point 3
                    """
                )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧠 MALUMBO AI")

st.sidebar.success(
    """
✅ Global Web Search

✅ Malawi Expert Mode

✅ Academic Research

✅ PDF/DOCX Upload

✅ Academic Writing

✅ Presentation Generator
"""
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
🌍 **MALUMBO AI v3.0**

A global AI research assistant
with special knowledge of Malawi.

🇲🇼 Malawi + 🌍 Global
"""
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Built with Streamlit • MALUMBO AI"
)
