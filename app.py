import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document
from duckduckgo_search import DDGS
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="MALUMBO AI ASSISTANT",
    layout="wide"
)

st.title("🤖 MALUMBO AI ASSISTANT")
st.markdown("### Your Academic, Research & Business Copilot - Forever Online")

client = InferenceClient(
    "microsoft/Phi-3-mini-4k-instruct"
)


def generate_response(prompt, max_tokens=1500):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = client.chat_completion(
        messages,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content


def read_file(file):

    if file.name.endswith(".pdf"):

        reader = PyPDF2.PdfReader(file)

        text = ""

        for page in reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

        return text

    elif file.name.endswith(".docx"):

        doc = Document(file)

        return "\n".join(
            [p.text for p in doc.paragraphs]
        )

    elif file.name.endswith(".csv"):

        return pd.read_csv(file).to_string()

    else:

        return "Unsupported file type"


def web_search_sources(query, num_results=3):

    sources = []

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                f"{query} site:mdpi.com OR site:researchgate.net",
                max_results=num_results
            )

            for r in results:

                sources.append(
                    {
                        "title": r["title"],
                        "link": r["href"],
                        "snippet": r["body"]
                    }
                )

    except Exception as e:

        st.warning(f"Web search unavailable: {e}")

    return sources


tab1, tab2 = st.tabs(
    [
        "1. Multi-File Chat",
        "2. Academic Writing"
    ]
)


# ==========================================
# TAB 1 - MULTI FILE CHAT
# ==========================================

with tab1:

    st.header("📚 Multi-File Chat")

    files = st.file_uploader(
        "Upload Files: PDF, DOCX, CSV",
        type=["pdf", "docx", "csv"],
        accept_multiple_files=True
    )

    question = st.text_input(
        "Ask a question about your files"
    )

    if st.button("Ask AI"):

        if not files:

            st.warning("Please upload at least one file.")

        elif not question:

            st.warning("Please enter a question.")

        else:

            with st.spinner("Reading files and thinking..."):

                context = ""

                for file in files:

                    context += (
                        f"\n--- FILE: {file.name} ---\n"
                    )

                    context += read_file(file)

                prompt = f"""
You are MALUMBO AI ASSISTANT.

Use ONLY the information contained
in the uploaded files to answer the question.

If the answer is not contained in the files,
clearly say that the information is not available
in the uploaded documents.

UPLOADED FILES:

{context}

QUESTION:

{question}

ANSWER:
"""

                try:

                    answer = generate_response(
                        prompt,
                        1024
                    )

                    st.write(answer)

                except Exception as e:

                    st.error(
                        f"AI error: {e}"
                    )


# ==========================================
# TAB 2 - ACADEMIC WRITING
# ==========================================

with tab2:

    st.header("✍️ Academic Writing Assistant")

    task_type = st.selectbox(
        "Task Type",
        [
            "Assignment Questions",
            "Essay",
            "Report"
        ]
    )

    assignment_text = st.text_area(
        "Paste Assignment Instructions Here",
        height=250
    )

    doc_length = st.slider(
        "Total Word Count",
        500,
        2000,
        750
    )

    if st.button("Generate Full Assignment"):

        if not assignment_text:

            st.warning(
                "Please paste your assignment instructions."
            )

        else:

            # ==================================
            # STEP 1 - WEB SEARCH
            # ==================================

            with st.spinner(
                "Step 1/3: Searching for academic sources..."
            ):

                sources = web_search_sources(
                    assignment_text[:200],
                    num_results=3
                )

                source_text = ""

                for i, source in enumerate(
                    sources,
                    start=1
                ):

                    source_text += (
                        f"[{i}] {source['title']}\n"
                        f"{source['snippet']}\n"
                        f"Source: {source['link']}\n\n"
                    )

            # ==================================
            # STEP 2 - WRITING
            # ==================================

            with st.spinner(
                "Step 2/3: Writing assignment..."
            ):

                prompt = f"""
You are a university academic writing assistant.

Write a high-quality {doc_length}-word
{task_type} based on the assignment instructions.

Use APA 7th Edition style.

ASSIGNMENT INSTRUCTIONS:

{assignment_text}

ACADEMIC SOURCES:

{source_text}

REQUIREMENTS:

1. Answer all assignment questions.
2. Use clear academic language.
3. Use appropriate headings and subheadings.
4. Include an introduction.
5. Include the main discussion.
6. Include a conclusion.
7. Use APA-style in-text citations.
8. Include a References section.
9. Do not invent sources.
10. Use the supplied sources where relevant.
11. Make the writing suitable for a university student.
12. Keep the response close to the requested word count.

Now write the complete assignment.
"""

                try:

                    answer = generate_response(
                        prompt,
                        2500
                    )

                    st.markdown(answer)

                except Exception as e:

                    st.error(
                        f"AI writing error: {e}"
                    )

            st.success(
                "✅ Assignment Complete!"
            )
