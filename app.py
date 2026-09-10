import streamlit as st
import PyPDF2
from docx import Document
from duckduckgo_search import DDGS

# ============================================================
# MALUMBO AI
# ============================================================

st.set_page_config(
    page_title="MALUMBO AI",
    page_icon="🇲🇼",
    layout="wide"
)

st.title("🧠 MALUMBO AI - Your Smart Malawi Assistant")
st.write("Ask questions about Malawi or search the web for information.")

# ============================================================
# MALAWI KNOWLEDGE BASE
# ============================================================

MALAWI_KNOWLEDGE = {
    "president": (
        "As of 2026, the President of Malawi is "
        "**Arthur Peter Mutharika**."
    ),

    "capital": (
        "The capital city of Malawi is **Lilongwe**."
    ),

    "currency": (
        "The currency of Malawi is the "
        "**Malawian Kwacha (MWK)**."
    ),

    "official language": (
        "The official language of Malawi is **English**. "
        "Chichewa is widely spoken across the country."
    ),

    "national flag": (
        "The flag of Malawi has three horizontal stripes: "
        "black, red, and green, with a rising red sun on the "
        "upper black stripe."
    ),

    "independence": (
        "Malawi gained independence from British colonial rule "
        "on **6 July 1964**."
    ),

    "largest city": (
        "Lilongwe is the capital city of Malawi, while "
        "Blantyre is one of the country's major commercial cities."
    ),

    "lake malawi": (
        "Lake Malawi is one of Africa's Great Lakes and is "
        "located mainly within Malawi."
    ),

    "malawi population": (
        "Malawi has a population of more than 20 million people. "
        "The exact population depends on the year and data source."
    )
}

# ============================================================
# FILE TEXT EXTRACTION
# ============================================================

def extract_pdf_text(file):
    text = ""

    try:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        text = f"Could not read PDF: {e}"

    return text


def extract_docx_text(file):
    text = ""

    try:
        document = Document(file)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    except Exception as e:
        text = f"Could not read Word document: {e}"

    return text


# ============================================================
# WEB SEARCH
# ============================================================

def web_search(query):
    context = ""
    links = []

    try:
        search_query = query + " Malawi 2026"

        with DDGS() as ddgs:

            results = ddgs.text(
                search_query,
                max_results=5
            )

            for result in results:

                title = result.get("title", "")
                body = result.get("body", "")
                href = result.get("href", "")

                if body:
                    context += body + "\n\n"

                if title and href:
                    links.append(
                        f"[{title}]({href})"
                    )

    except Exception:
        return "", []

    return context, links


# ============================================================
# MALUMBO AI ANSWER ENGINE
# ============================================================

def ai_search(query):

    query_lower = query.lower().strip()

    # --------------------------------------------------------
    # STEP 1: CHECK MALAWI KNOWLEDGE BASE
    # --------------------------------------------------------

    for key, answer in MALAWI_KNOWLEDGE.items():

        if key in query_lower:

            return (
                answer
                + "\n\n"
                + "*Answered from MALUMBO AI's Malawi knowledge base.*"
            )

    # --------------------------------------------------------
    # SPECIAL PRESIDENT QUESTIONS
    # --------------------------------------------------------

    president_words = [
        "who is the president",
        "president of malawi",
        "malawi president",
        "current president",
        "president malawi"
    ]

    if any(word in query_lower for word in president_words):

        return (
            "**The President of Malawi is "
            "Arthur Peter Mutharika.** 🇲🇼\n\n"
            "*MALUMBO AI Malawi knowledge base*"
        )

    # --------------------------------------------------------
    # SPECIAL CAPITAL QUESTIONS
    # --------------------------------------------------------

    capital_words = [
        "capital of malawi",
        "malawi capital",
        "what is the capital"
    ]

    if any(word in query_lower for word in capital_words):

        return (
            "**The capital city of Malawi is Lilongwe.** 🇲🇼\n\n"
            "*MALUMBO AI Malawi knowledge base*"
        )

    # --------------------------------------------------------
    # SPECIAL CURRENCY QUESTIONS
    # --------------------------------------------------------

    currency_words = [
        "currency of malawi",
        "malawi currency",
        "money used in malawi",
        "malawi money"
    ]

    if any(word in query_lower for word in currency_words):

        return (
            "**The currency of Malawi is the Malawian Kwacha (MWK).** 💰\n\n"
            "*MALUMBO AI Malawi knowledge base*"
        )

    # --------------------------------------------------------
    # STEP 2: TRY WEB SEARCH
    # --------------------------------------------------------

    context, links = web_search(query)

    # --------------------------------------------------------
    # STEP 3: IF WEB SEARCH WORKS
    # --------------------------------------------------------

    if context:

        answer = "**Answer:**\n\n"

        # Limit the amount of returned search text
        answer += context[:5000]

        if links:

            answer += "\n\n**Sources:**\n\n"

            for link in links:
                answer += "- " + link + "\n"

        return answer

    # --------------------------------------------------------
    # STEP 4: FALLBACK ANSWER
    # --------------------------------------------------------

    return (
        f"I couldn't find live web results for **'{query}'**.\n\n"
        "However, MALUMBO AI is still working. 🇲🇼\n\n"
        "Try asking me things such as:\n"
        "- Who is the president of Malawi?\n"
        "- What is the capital of Malawi?\n"
        "- What is the currency of Malawi?\n"
        "- When did Malawi gain independence?\n"
        "- Tell me about Lake Malawi."
    )


# ============================================================
# FILE UPLOAD SECTION
# ============================================================

st.sidebar.header("📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or Word documents",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

document_text = ""

if uploaded_files:

    st.sidebar.success(
        f"{len(uploaded_files)} file(s) uploaded."
    )

    for uploaded_file in uploaded_files:

        if uploaded_file.name.lower().endswith(".pdf"):

            document_text += (
                extract_pdf_text(uploaded_file)
                + "\n"
            )

        elif uploaded_file.name.lower().endswith(".docx"):

            document_text += (
                extract_docx_text(uploaded_file)
                + "\n"
            )

    # Limit document context
    document_text = document_text[:15000]


# ============================================================
# MAIN QUESTION AREA
# ============================================================

query = st.text_input(
    "Ask MALUMBO AI anything:",
    placeholder="Example: Who is the president of Malawi?"
)


# ============================================================
# SEARCH BUTTON
# ============================================================

if st.button("🔍 Search & Answer"):

    if query.strip():

        with st.spinner("🧠 MALUMBO AI is thinking..."):

            # ------------------------------------------------
            # If documents are uploaded, search document first
            # ------------------------------------------------

            if document_text:

                query_words = query.lower().split()

                matching_lines = []

                for line in document_text.split("\n"):

                    line_lower = line.lower()

                    if any(
                        word in line_lower
                        for word in query_words
                        if len(word) > 3
                    ):

                        matching_lines.append(line)

                if matching_lines:

                    st.subheader("📄 Answer from your documents")

                    document_answer = "\n".join(
                        matching_lines[:20]
                    )

                    st.write(document_answer)

                    st.divider()

                    st.caption(
                        "Answer found in your uploaded document(s)."
                    )

                else:

                    st.subheader("🌐 MALUMBO AI Answer")

                    st.write(
                        ai_search(query)
                    )

            else:

                st.subheader("🌐 MALUMBO AI Answer")

                st.write(
                    ai_search(query)
                )

    else:

        st.warning(
            "Please type a question first."
        )


# ============================================================
# SIDEBAR INFORMATION
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("✨ MALUMBO AI Features")

st.sidebar.write(
    """
    ✅ Malawi knowledge base

    ✅ Web search

    ✅ PDF upload

    ✅ Word document upload

    ✅ Document question answering

    ✅ Multiple file support

    ✅ Search fallback system
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🇲🇼 MALUMBO AI — Smart AI Assistant for Malawi"
)
