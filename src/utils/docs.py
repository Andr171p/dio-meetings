import io

from markdown_pdf import MarkdownPdf, Section


def md_text_to_pdf(md_text: str) -> bytes:
    """Формирует PDF файл по Markdown тексту"""

    pdf = MarkdownPdf()
    pdf.add_section(Section(md_text))
    buffer = io.BytesIO()
    pdf.save_bytes(buffer)
    return buffer.getvalue()
