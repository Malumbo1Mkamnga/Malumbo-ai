import streamlit as st
import PyPDF2
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from pptx import Presentation
from pptx.util import Inches, Pt
from duckduckgo_search import DDGS
import io
import re


# ============================================================
# MALUMBO AI v5.0
# FULL OUTPUT MODE
# ============================================================

st.set_page_config(
    page_title="MALUMBO AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 MALUMBO AI v5.0")
st.subheader("🌍 Full AI Writer, Research Assistant & Presentation Generator")

st.markdown(
    """
    **MALUMBO AI** helps you research topics, write academic papers,
    read PDF documents, and generate PowerPoint presentations.
    """
)


# ============================================================
# MALAWI BASIC KNOWLEDGE
# ============================================================

MALAWI_KNOWLEDGE = {
    "capital malawi":
        "The capital city of Malawi is Lilongwe.",

    "president malawi":
        "The current President of Malawi should be verified using a current web search before being used in academic or official work.",

    "malawi":
        "Malawi is a landlocked country in southeastern Africa. Its economy is strongly connected to agriculture, with smallholder farming playing an important role."
}


# ============================================================
# WEB SEARCH
# ============================================================

def ai_search(query):

    query_lower = query.lower()

    # Check basic local knowledge
    if "capital" in query_lower and "malawi" in query_lower:
        return "### Answer\n\n" + MALAWI_KNOWLEDGE["capital malawi"]

    sources_text = []
    links = []

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                query + " 2026",
                max_results=5
            )

            for result in results:

                title = result.get("title", "")
                body = result.get("body", "")
                href = result.get("href", "")

                if body:
                    sources_text.append(body)

                if title and href:
                    links.append(
                        f"- [{title}]({href})"
                    )

    except Exception as e:

        return (
            "### Search Error\n\n"
            "The web search service could not be reached right now.\n\n"
            f"Technical information: `{e}`"
        )

    if sources_text:

        answer = "\n\n".join(
            sources_text[:5]
        )

        if len(answer) > 3000:
            answer = answer[:3000] + "..."

        result_text = (
            "### Answer\n\n"
            + answer
        )

        if links:

            result_text += (
                "\n\n### Sources\n\n"
                + "\n".join(links)
            )

        return result_text

    return (
        "### Answer\n\n"
        "I could not find suitable web results for this question."
    )


# ============================================================
# PDF READER
# ============================================================

def read_pdf(uploaded_file):

    text = ""

    try:

        reader = PyPDF2.PdfReader(uploaded_file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:

        return f"Could not read PDF: {e}"

    return text


# ============================================================
# CLEAN FILE NAME
# ============================================================

def clean_filename(name):

    name = re.sub(
        r'[\\/*?:"<>|]',
        "",
        name
    )

    name = name.strip()

    if not name:
        name = "Malumbo_AI_Output"

    return name


# ============================================================
# DOCX GENERATOR
# ============================================================

def generate_docx(topic):

    doc = Document()

    # --------------------------------------------------------
    # PAGE SETTINGS
    # --------------------------------------------------------

    section = doc.sections[0]

    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    # --------------------------------------------------------
    # DEFAULT FONT
    # --------------------------------------------------------

    styles = doc.styles

    normal_style = styles["Normal"]

    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title = doc.add_heading(
        topic,
        0
    )

    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for run in title.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(18)
        run.bold = True

    # --------------------------------------------------------
    # AUTHOR
    # --------------------------------------------------------

    author = doc.add_paragraph()

    author.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = author.add_run(
        "Generated by MALUMBO AI"
    )

    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.italic = True

    doc.add_paragraph("")

    # --------------------------------------------------------
    # INTRODUCTION
    # --------------------------------------------------------

    heading = doc.add_heading(
        "1. Introduction",
        level=1
    )

    heading.runs[0].font.name = "Times New Roman"

    intro = doc.add_paragraph()

    intro.add_run(
        f"{topic} is an important subject that has received "
        "considerable attention in academic, economic, social, "
        "environmental and development discussions. Understanding "
        "this topic requires an examination of its background, "
        "major characteristics, challenges and potential solutions."
    )

    intro.add_run(
        " This paper discusses the major issues associated with "
        f"{topic} and considers its broader implications."
    )

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    heading = doc.add_heading(
        "2. Background",
        level=1
    )

    paragraph = doc.add_paragraph()

    paragraph.add_run(
        f"The background of {topic} can be understood by examining "
        "the historical, social, economic and institutional factors "
        "that influence the subject. These factors determine how "
        "the issue develops and how individuals, organizations and "
        "governments respond to it."
    )

    # --------------------------------------------------------
    # MAIN DISCUSSION
    # --------------------------------------------------------

    heading = doc.add_heading(
        "3. Main Discussion",
        level=1
    )

    # Point 1
    sub = doc.add_heading(
        "3.1 Key Issues",
        level=2
    )

    doc.add_paragraph(
        f"One major aspect of {topic} concerns the factors that "
        "influence its development and outcomes. These factors may "
        "include institutional conditions, economic incentives, "
        "access to information, available resources and individual "
        "decision-making."
    )

    # Point 2
    sub = doc.add_heading(
        "3.2 Importance",
        level=2
    )

    doc.add_paragraph(
        f"The importance of {topic} can be observed through its "
        "effects on individuals, households, businesses, institutions "
        "and wider society. A proper understanding of the subject "
        "can support better planning, policy formulation and "
        "decision-making."
    )

    # Point 3
    sub = doc.add_heading(
        "3.3 Challenges",
        level=2
    )

    doc.add_paragraph(
        f"Despite the potential benefits associated with {topic}, "
        "several challenges may limit positive outcomes. These can "
        "include limited financial resources, inadequate information, "
        "institutional constraints, technological barriers and "
        "unequal access to opportunities."
    )

    # Point 4
    sub = doc.add_heading(
        "3.4 Possible Solutions",
        level=2
    )

    doc.add_paragraph(
        f"Addressing challenges related to {topic} requires "
        "coordinated action by relevant stakeholders. Possible "
        "approaches include improving access to information, "
        "strengthening institutions, investing in appropriate "
        "technology, improving education and supporting evidence-"
        "based policy interventions."
    )

    # --------------------------------------------------------
    # MALAWI CONTEXT
    # --------------------------------------------------------

    heading = doc.add_heading(
        "4. Malawi Context",
        level=1
    )

    doc.add_paragraph(
        f"In Malawi, {topic} can be examined within the country's "
        "economic, social and institutional environment. Local "
        "conditions are important because policies and interventions "
        "that work in one country may produce different outcomes "
        "under different circumstances. Therefore, Malawi-specific "
        "evidence should be considered when making conclusions "
        "about the topic."
    )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    heading = doc.add_heading(
        "5. Recommendations",
        level=1
    )

    recommendations = [
        "Improve access to reliable information and knowledge.",
        "Strengthen relevant institutions and stakeholder coordination.",
        "Promote evidence-based planning and decision-making.",
        "Increase investment in appropriate technologies and resources.",
        "Conduct further research using reliable primary and secondary data."
    ]

    for item in recommendations:

        p = doc.add_paragraph(
            style="List Bullet"
        )

        p.add_run(item)

    # --------------------------------------------------------
    # CONCLUSION
    # --------------------------------------------------------

    heading = doc.add_heading(
        "6. Conclusion",
        level=1
    )

    doc.add_paragraph(
        f"In conclusion, {topic} is an important area that requires "
        "careful analysis and continued research. The discussion "
        "shows that outcomes are influenced by several interconnected "
        "factors. Effective responses should therefore consider the "
        "specific economic, social, institutional and environmental "
        "conditions surrounding the issue. Further research can help "
        "generate stronger evidence for policy and practical decision-"
        "making."
    )

    # --------------------------------------------------------
    # REFERENCES
    # --------------------------------------------------------

    heading = doc.add_heading(
        "References",
        level=1
    )

    doc.add_paragraph(
        "Note: MALUMBO AI should verify and replace these references "
        "with real academic sources before the document is submitted "
        "for academic assessment."
    )

    references = [
        "World Bank. World Development Indicators.",
        "Food and Agriculture Organization of the United Nations. FAOSTAT.",
        "Government of Malawi. National development and sector policy documents.",
        "Relevant peer-reviewed academic literature on the selected topic."
    ]

    for ref in references:

        doc.add_paragraph(
            ref,
            style="List Number"
        )

    # --------------------------------------------------------
    # FORMAT ALL PARAGRAPHS
    # --------------------------------------------------------

    for paragraph in doc.paragraphs:

        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        paragraph.paragraph_format.line_spacing = 1.5
        paragraph.paragraph_format.space_after = Pt(6)

        for run in paragraph.runs:

            run.font.name = "Times New Roman"
            run.font.size = Pt(12)

    # Keep title centered
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    author.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --------------------------------------------------------
    # SAVE TO MEMORY
    # --------------------------------------------------------

    buffer = io.BytesIO()

    doc.save(buffer)

    buffer.seek(0)

    return buffer


# ============================================================
# POWERPOINT GENERATOR
# ============================================================

def generate_pptx(topic):

    prs = Presentation()

    # --------------------------------------------------------
    # TITLE SLIDE
    # --------------------------------------------------------

    slide = prs.slides.add_slide(
        prs.slide_layouts[0]
    )

    slide.shapes.title.text = topic

    slide.placeholders[1].text = (
        "Generated by MALUMBO AI"
    )

    # --------------------------------------------------------
    # SLIDE FUNCTION
    # --------------------------------------------------------

    def add_content_slide(title, bullets):

        slide = prs.slides.add_slide(
            prs.slide_layouts[1]
        )

        slide.shapes.title.text = title

        body = slide.placeholders[1]

        body.text = bullets[0]

        for bullet in bullets[1:]:

            paragraph = body.text_frame.add_paragraph()

            paragraph.text = bullet

            paragraph.level = 0

        # Format title
        for shape in slide.shapes:

            if not hasattr(shape, "text_frame"):
                continue

            for paragraph in shape.text_frame.paragraphs:

                for run in paragraph.runs:

                    run.font.name = "Arial"
                    run.font.size = Pt(24)

        return slide

    # --------------------------------------------------------
    # SLIDE 2
    # --------------------------------------------------------

    add_content_slide(
        "1. Introduction",
        [
            f"Overview of {topic}",
            "Background and context",
            "Why the topic is important",
            "Main issues discussed in the presentation"
        ]
    )

    # --------------------------------------------------------
    # SLIDE 3
    # --------------------------------------------------------

    add_content_slide(
        "2. Background",
        [
            f"Historical and contextual background of {topic}",
            "Major developments",
            "Relevant social and economic factors",
            "Current situation"
        ]
    )

    # --------------------------------------------------------
    # SLIDE 4
    # --------------------------------------------------------

    add_content_slide(
        "3. Key Concepts",
        [
            f"Important concepts related to {topic}",
            "Definitions of major terms",
            "Relationship between key concepts",
            "Importance of understanding these concepts"
        ]
    )

    # --------------------------------------------------------
    # SLIDE 5
    # --------------------------------------------------------

    add_content_slide(
        "4. Major Issues",
        [
            f"Major issues associated with {topic}",
            "Factors influencing outcomes",
            "Institutional considerations",
            "Economic and social implications"
        ]
    )

    # --------------------------------------------------------
    # SLIDE 6
    # --------------------------------------------------------

    add_content_slide(
        "5. Importance",
        [
            f"Why {topic} matters",
            "Effects on individuals and households",
            "Effects on organizations and institutions",
            "Broader development implications"
        ]
    )

    # --------------------------------------------------------
    # SLIDE 7
    # --------------------------------------------------------

    add_content_slide(
        "6. Challenges",
        [
            "Limited resources",
            "Information and knowledge gaps",
            "Institutional constraints",
            "Technological and financial barriers"
        ]
    )

    # --------------------------------------------------------
    # SLIDE 8
    # --------------------------------------------------------

    add_content_slide(
        "7. Malawi Context",
        [
            f"Application of {topic} to Malawi",
            "Local economic conditions",
            "Institutional environment",
            "Country-specific challenges and opportunities"
        ]
    )

    # --------------------------------------------------------
    # SLIDE 9
    # --------------------------------------------------------

    add_content_slide(
        "8. Recommendations",
        [
            "Improve access to information",
            "Strengthen institutions",
            "Promote evidence-based decision-making",
            "Invest in appropriate technologies",
            "Support further research"
        ]
    )

    # --------------------------------------------------------
    # SLIDE 10
    # --------------------------------------------------------

    add_content_slide(
        "9. Conclusion",
        [
            f"{topic} requires careful analysis.",
            "Multiple factors influence outcomes.",
            "Effective solutions require stakeholder coordination.",
            "Further research can improve evidence and decision-making."
        ]
    )

    # --------------------------------------------------------
    # REFERENCES SLIDE
    # --------------------------------------------------------

    add_content_slide(
        "10. References",
        [
            "World Bank — World Development Indicators",
            "FAO — FAOSTAT",
            "Government of Malawi publications",
            "Peer-reviewed academic literature",
            "Relevant institutional reports"
        ]
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    buffer = io.BytesIO()

    prs.save(buffer)

    buffer.seek(0)

    return buffer


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🌍 Research & Chat",
        "✍️ Academic Writing",
        "📊 Presentation Generator",
        "📄 PDF Reader"
    ]
)


# ============================================================
# TAB 1 — RESEARCH
# ============================================================

with tab1:

    st.header(
        "🌍 Research The Internet"
    )

    query = st.text_input(
        "Ask MALUMBO AI anything",
        placeholder="Example: What are the effects of climate change on agriculture?"
    )

    if st.button(
        "🔍 Search & Answer",
        key="search_button"
    ):

        if query.strip():

            with st.spinner(
                "Researching the web..."
            ):

                answer = ai_search(query)

            st.markdown(answer)

        else:

            st.warning(
                "Please enter a question first."
            )


# ============================================================
# TAB 2 — ACADEMIC WRITING
# ============================================================

with tab2:

    st.header(
        "✍️ Full Academic Writing"
    )

    st.write(
        "Generate a formatted Microsoft Word document."
    )

    topic = st.text_input(
        "Essay / Research Paper Topic",
        placeholder="Example: Effects of Climate Change on Smallholder Farmers in Malawi",
        key="essay_topic"
    )

    if st.button(
        "📝 Generate Full Paper",
        key="generate_paper"
    ):

        if topic.strip():

            with st.spinner(
                "Creating your Word document..."
            ):

                docx_file = generate_docx(
                    topic
                )

            filename = (
                clean_filename(topic)
                + ".docx"
            )

            st.success(
                "✅ Academic paper generated successfully!"
            )

            st.download_button(
                label="📄 Download Full Essay (.docx)",
                data=docx_file,
                file_name=filename,
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),
                key="download_docx"
            )

        else:

            st.warning(
                "Please enter an essay or research topic."
            )


# ============================================================
# TAB 3 — PRESENTATION
# ============================================================

with tab3:

    st.header(
        "📊 Full PowerPoint Presentation"
    )

    st.write(
        "Generate a 10-slide PowerPoint presentation."
    )

    pres_topic = st.text_input(
        "Presentation Topic",
        placeholder="Example: Marketing in Malawi",
        key="presentation_topic"
    )

    if st.button(
        "🎯 Generate Full Presentation",
        key="generate_presentation"
    ):

        if pres_topic.strip():

            with st.spinner(
                "Creating your PowerPoint presentation..."
            ):

                pptx_file = generate_pptx(
                    pres_topic
                )

            filename = (
                clean_filename(pres_topic)
                + ".pptx"
            )

            st.success(
                "✅ PowerPoint presentation generated successfully!"
            )

            st.download_button(
                label="📊 Download Full Presentation (.pptx)",
                data=pptx_file,
                file_name=filename,
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "presentationml.presentation"
                ),
                key="download_pptx"
            )

        else:

            st.warning(
                "Please enter a presentation topic."
            )


# ============================================================
# TAB 4 — PDF READER
# ============================================================

with tab4:

    st.header(
        "📄 PDF Reader"
    )

    st.write(
        "Upload a PDF and MALUMBO AI will extract its text."
    )

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_pdf:

        with st.spinner(
            "Reading PDF..."
        ):

            pdf_text = read_pdf(
                uploaded_pdf
            )

        if pdf_text.strip():

            st.success(
                "✅ PDF successfully read."
            )

            st.text_area(
                "Extracted PDF Text",
                pdf_text,
                height=500
            )

        else:

            st.warning(
                "No readable text was found in this PDF."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧠 MALUMBO AI v5.0 — Full Output Mode"
)

st.caption(
    "Always verify AI-generated academic information, "
    "statistics and references before submission."
)
