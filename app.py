import streamlit as st
from duckduckgo_search import DDGS

# ============================================================
# MALUMBO AI v6.1 - SAFE MODE
# ============================================================

st.set_page_config(
    page_title="MALUMBO AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MALUMBO AI v6.1")
st.subheader("🌍 AI Research Assistant - Safe Mode")


# ============================================================
# MALAWI BASIC KNOWLEDGE
# ============================================================

MALAWI_KNOWLEDGE = {
    "capital malawi":
        "The capital city of Malawi is **Lilongwe**.",

    "malawi":
        "Malawi is a landlocked country in southeastern Africa."
}


# ============================================================
# WEB SEARCH FUNCTION
# ============================================================

def ai_search(query):

    query_lower = query.lower()

    # Basic Malawi answers
    if "capital" in query_lower and "malawi" in query_lower:
        return (
            "### Answer\n\n"
            "The capital city of Malawi is **Lilongwe**."
        )

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
                    sources_text += body + "\n\n"

                if title and href:
                    links.append(
                        f"- [{title}]({href})"
                    )

    except Exception as e:

        return (
            "### Search Error\n\n"
            f"`{e}`\n\n"
            "Please try again later."
        )

    if sources_text:

        answer = sources_text[:2500]

        response = (
            "### Answer\n\n"
            + answer
        )

        if links:

            response += (
                "\n\n### Sources\n\n"
                + "\n".join(links)
            )

        return response

    return (
        "### Answer\n\n"
        "No suitable web results were found."
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
# TAB 1 - RESEARCH
# ============================================================

with tab1:

    st.header(
        "🌍 Research The Internet"
    )

    query = st.text_input(
        "Ask anything",
        placeholder="Example: What are the effects of climate change on agriculture?"
    )

    if st.button(
        "🔍 Search & Answer",
        key="search"
    ):

        if query.strip():

            with st.spinner(
                "Searching the web..."
            ):

                answer = ai_search(query)

            st.markdown(answer)

        else:

            st.warning(
                "Please type a question first."
            )


# ============================================================
# TAB 2 - ACADEMIC WRITING
# ============================================================

with tab2:

    st.header(
        "✍️ Academic Writing"
    )

    st.info(
        "DOCX generation will be added after the safe version "
        "is confirmed to be running."
    )

    topic = st.text_input(
        "Essay / Research Topic",
        placeholder="Example: Conservation Agriculture in Malawi",
        key="academic_topic"
    )

    if st.button(
        "📝 Generate Paper",
        key="academic_button"
    ):

        if topic.strip():

            st.success(
                "Topic received: " + topic
            )

        else:

            st.warning(
                "Please enter a topic."
            )


# ============================================================
# TAB 3 - PRESENTATION
# ============================================================

with tab3:

    st.header(
        "📊 Presentation Generator"
    )

    st.info(
        "PPTX generation will be added after the safe version "
        "is confirmed to be running."
    )

    presentation_topic = st.text_input(
        "Presentation Topic",
        placeholder="Example: Marketing in Malawi",
        key="presentation_topic"
    )

    if st.button(
        "🎯 Generate Presentation",
        key="presentation_button"
    ):

        if presentation_topic.strip():

            st.success(
                "Topic received: " + presentation_topic
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
    "🧠 MALUMBO AI v6.1 — Safe Mode"
)
