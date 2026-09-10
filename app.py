import streamlit as st
from duckgo_search import DDGS

# ============================================================
# MALUMBO AI v7.0
# LIGHTWEIGHT / SAFE DEPLOYMENT VERSION
# ============================================================

st.set_page_config(
    page_title="MALUMBO AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MALUMBO AI v7.0")
st.subheader("🌍 Live AI Research Assistant")


# ============================================================
# MALAWI KNOWLEDGE
# ============================================================

MALAWI_KNOWLEDGE = {
    "capital malawi":
        "The capital city of Malawi is **Lilongwe**.",

    "president malawi":
        "The current President of Malawi should be verified with a current web search before being used for official or academic work.",

    "vice president malawi":
        "The current Vice President of Malawi should be verified with a current web search before being used for official or academic work."
}


# ============================================================
# SEARCH FUNCTION
# ============================================================

def ai_search(query):

    query_lower = query.lower()

    # --------------------------------------------------------
    # QUICK MALAWI ANSWERS
    # --------------------------------------------------------

    if "capital" in query_lower and "malawi" in query_lower:

        return (
            "### ✅ Answer\n\n"
            "The capital city of Malawi is **Lilongwe**.\n\n"
            "*From MALUMBO AI Malawi knowledge*"
        )

    # --------------------------------------------------------
    # WHOLE INTERNET SEARCH
    # --------------------------------------------------------

    sources_text = ""
    links = []

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=3
            )

            for result in results:

                body = result.get("body", "")
                title = result.get("title", "")
                href = result.get("href", "")

                if body:

                    sources_text += (
                        body + "\n\n"
                    )

                if title and href:

                    links.append(
                        f"- [{title}]({href})"
                    )

    except Exception as e:

        return (
            "### ❌ Search Error\n\n"
            f"Search failed: `{e}`\n\n"
            "Please try again."
        )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if sources_text:

        answer = sources_text[:2500]

        response = (
            "### ✅ Answer\n\n"
            + answer
        )

        if links:

            response += (
                "\n\n### Sources\n\n"
                + "\n".join(links)
            )

        return response

    return (
        "### ⚠️ No Results\n\n"
        "No suitable search results were found."
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(
    [
        "1. 🌍 Research & Chat",
        "2. ✍️ Academic Writing",
        "3. 📊 Presentation Generator"
    ]
)


# ============================================================
# TAB 1 — RESEARCH
# ============================================================

with tab1:

    st.header(
        "🌍 Research The Whole Internet"
    )

    query = st.text_input(
        "Ask anything",
        placeholder=(
            "News, academic research, Malawi, USA, "
            "agriculture, economics, technology..."
        )
    )

    if st.button(
        "🔍 Search & Answer",
        key="search_button"
    ):

        if query.strip():

            with st.spinner(
                "🔎 Searching the internet..."
            ):

                result = ai_search(
                    query
                )

            st.markdown(result)

        else:

            st.warning(
                "Please enter a question first."
            )


# ============================================================
# TAB 2 — ACADEMIC WRITING
# ============================================================

with tab2:

    st.header(
        "✍️ Academic Writing"
    )

    st.info(
        "🚧 Full .docx academic document generation "
        "will be added after the lightweight version "
        "is confirmed to be running."
    )

    academic_topic = st.text_input(
        "Enter your academic topic",
        placeholder=(
            "Example: Factors Affecting Adoption "
            "of Conservation Agriculture"
        ),
        key="academic_topic"
    )

    if st.button(
        "📝 Generate Academic Paper",
        key="academic_button"
    ):

        if academic_topic.strip():

            st.success(
                "Topic received successfully!"
            )

            st.write(
                "Your topic:"
            )

            st.write(
                academic_topic
            )

        else:

            st.warning(
                "Please enter an academic topic."
            )


# ============================================================
# TAB 3 — PRESENTATION GENERATOR
# ============================================================

with tab3:

    st.header(
        "📊 Presentation Generator"
    )

    st.info(
        "🚧 Full .pptx PowerPoint generation "
        "will be added after the lightweight version "
        "is confirmed to be running."
    )

    presentation_topic = st.text_input(
        "Enter your presentation topic",
        placeholder=(
            "Example: Marketing in Malawi"
        ),
        key="presentation_topic"
    )

    if st.button(
        "🎯 Generate Presentation",
        key="presentation_button"
    ):

        if presentation_topic.strip():

            st.success(
                "Presentation topic received successfully!"
            )

            st.write(
                "Your topic:"
            )

            st.write(
                presentation_topic
            )

        else:

            st.warning(
                "Please enter a presentation topic."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧠 MALUMBO AI v7.0 — Lightweight Deployment"
)

st.caption(
    "🌍 Research • Academic Writing • Presentations"
)
