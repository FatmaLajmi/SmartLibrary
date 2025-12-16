# Simple export helpers at app root (make sure openpyxl and reportlab are installed)
import io
from datetime import datetime
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from datetime import datetime

def truncate(text, max_len=25):
    """Truncate long text to fit cell nicely."""
    if not text:
        return ""
    return text if len(text) <= max_len else text[:max_len - 3] + "..."

def header_footer(canvas, doc):
    """Draw header (title + date) and footer (page number)."""

    canvas.saveState()

    # Header title
    canvas.setFont("Helvetica-Bold", 11)
    canvas.setFillColor(colors.HexColor("#1A4B84"))
    canvas.drawString(30, 770, "SmartLibrary – Stock Report")

    # Date
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(580, 770, datetime.now().strftime("%Y-%m-%d"))

    # Footer page number
    page_num = canvas.getPageNumber()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(580, 20, f"Page {page_num}")

    canvas.restoreState()

def export_stocks_to_excel(queryset, output_stream):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stock export"

    # Header
    headers = ['Book title', 'Genre', 'Author', 'Quantity', 'Min quantity', 'Max quantity', 'Status']
    ws.append(headers)

    for s in queryset.select_related('book'):
        title = (
            getattr(s.book, 'title', None)
            or getattr(s.book, 'titre', None)
            or str(getattr(s, 'book', '') or '')
        )
        row = [
            title,
            getattr(s.book, 'genre', ''),
            getattr(s.book, 'author', ''),
            s.quantity,
            s.min_quantity,
            s.max_quantity,
            s.status
        ]
        ws.append(row)

    # Optional: set column widths (approx)
    cols = ['A','B','C','D','E','F','G']
    widths = [40, 20, 25, 12, 12, 12, 14]  # excel column width units
    for col, w in zip(cols, widths):
        ws.column_dimensions[col].width = w

    wb.save(output_stream)

def export_stocks_to_pdf(queryset, output_stream):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=25,
        rightMargin=25,
        topMargin=60,      # extra for header
        bottomMargin=40    # extra for footer
    )

    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.textColor = colors.HexColor("#1A4B84")

    elements.append(Paragraph("📚 Stock Report", title_style))
    elements.append(Spacer(1, 12))

    # Table data
    data = [['Book Title', 'Genre', 'Author', 'Quantity', 'Min', 'Max', 'Status']]

    for s in queryset.select_related('book'):
        data.append([
            truncate(getattr(s.book, 'title', ''), 30),
            truncate(getattr(s.book, 'genre', ''), 18),
            truncate(getattr(s.book, 'author', ''), 25),
            str(s.quantity),
            str(s.min_quantity),
            str(s.max_quantity),
            str(s.status)
        ])

    table = Table(
        data,
        repeatRows=1,
        colWidths=[
            5 * cm, 3.2 * cm, 3.4 * cm,
            2 * cm, 1.5 * cm, 1.5 * cm, 2.5 * cm
        ]
    )

    # Colors
    header_color = colors.HexColor("#1A4B84")
    row_color_1 = colors.HexColor("#E8F1FA")
    row_color_2 = colors.white
    grid_color = colors.HexColor("#A3B3C2")

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_color),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

        ("GRID", (0, 0), (-1, -1), 0.3, grid_color),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),

        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ])

    # Alternating row colors
    for i in range(1, len(data)):
        style.add(
            "BACKGROUND",
            (0, i), (-1, i),
            row_color_1 if i % 2 == 1 else row_color_2
        )

    table.setStyle(style)

    elements.append(table)
    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph("<font size='9' color='#666'>Generated automatically by SmartLibrary Admin</font>",
                  styles["Normal"])
    )

    # Build PDF with header/footer functions
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

    output_stream.write(buffer.getvalue())
    buffer.close()