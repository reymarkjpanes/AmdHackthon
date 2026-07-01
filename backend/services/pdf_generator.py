import io
import logging
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from models.response import AnalysisResult

logger = logging.getLogger(__name__)

# AMD brand color
AMD_RED = colors.HexColor("#ED1C24")
AMD_DARK = colors.HexColor("#1a1a2e")
AMD_LIGHT_GRAY = colors.HexColor("#f5f5f5")
AMD_MED_GRAY = colors.HexColor("#e0e0e0")
WHITE = colors.white
BLACK = colors.black

def _color_to_hex(color) -> str:
    """Convert a ReportLab color to a 6-digit hex string (no #)."""
    r = int(color.red * 255)
    g = int(color.green * 255)
    b = int(color.blue * 255)
    return f"{r:02x}{g:02x}{b:02x}"


class PDFGenerator:
    """
    Generates AMD-branded PDF reports from AnalysisResult data using ReportLab.
    """

    AMD_RED = "#ED1C24"  # spec: AMD_RED = "#ED1C24"

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._build_custom_styles()

    def _build_custom_styles(self):
        """Define custom paragraph styles for the report."""
        self.title_style = ParagraphStyle(
            "DFTitle",
            parent=self.styles["Title"],
            fontSize=28,
            textColor=WHITE,
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName="Helvetica-Bold",
        )
        self.subtitle_style = ParagraphStyle(
            "DFSubtitle",
            parent=self.styles["Normal"],
            fontSize=14,
            textColor=AMD_RED,
            alignment=TA_CENTER,
            spaceAfter=8,
            fontName="Helvetica-Bold",
        )
        self.section_header_style = ParagraphStyle(
            "DFSection",
            parent=self.styles["Heading1"],
            fontSize=14,
            textColor=AMD_RED,
            fontName="Helvetica-Bold",
            spaceBefore=16,
            spaceAfter=8,
            borderPad=4,
        )
        self.body_style = ParagraphStyle(
            "DFBody",
            parent=self.styles["Normal"],
            fontSize=10,
            textColor=BLACK,
            fontName="Helvetica",
            spaceAfter=6,
            leading=14,
        )
        self.label_style = ParagraphStyle(
            "DFLabel",
            parent=self.styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#666666"),
            fontName="Helvetica",
        )
        self.footer_style = ParagraphStyle(
            "DFFooter",
            parent=self.styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#999999"),
            alignment=TA_CENTER,
            fontName="Helvetica",
        )

    def generate_report(self, analysis: AnalysisResult, session_id: str) -> bytes:
        """
        Generate a complete PDF report from an AnalysisResult.

        Args:
            analysis: Completed AnalysisResult with all analysis data
            session_id: Session identifier (used in footer)

        Returns:
            PDF file as bytes

        Raises:
            Exception: If PDF generation fails
        """
        buffer = io.BytesIO()
        today = datetime.utcnow().strftime("%Y-%m-%d")

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            title="Clausify AI — Document Intelligence Report",
            author="Clausify AI",
        )

        story = []

        # === TITLE PAGE ===
        story.extend(self._build_title_page(today, session_id))
        story.append(PageBreak())

        # === EXECUTIVE SUMMARY ===
        story.extend(self._build_executive_summary(analysis))

        # === RISK ANALYSIS TABLE ===
        story.extend(self._build_risk_table(analysis))

        # === COMPARISON MATRIX ===
        story.extend(self._build_comparison_matrix(analysis))

        # === DETECTED CONFLICTS ===
        story.extend(self._build_conflicts_section(analysis))

        # === RECOMMENDATION ===
        story.extend(self._build_recommendation_section(analysis))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()

        logger.info(
            f"PDF report generated for session {session_id} ({len(pdf_bytes)} bytes)"
        )
        return pdf_bytes

    def _build_title_page(self, today: str, session_id: str) -> list:
        """Build the title page elements."""
        elements = []

        # Dark header background effect using a colored table
        title_data = [
            [Paragraph("Clausify AI", self.title_style)],
            [Paragraph("Document Intelligence Report", self.subtitle_style)],
        ]
        title_table = Table(title_data, colWidths=[16 * cm])
        title_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), AMD_DARK),
                ("TOPPADDING", (0, 0), (-1, -1), 24),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 24),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ])
        )
        elements.append(Spacer(1, 3 * cm))
        elements.append(title_table)
        elements.append(Spacer(1, 1 * cm))

        # AMD badge
        amd_data = [
            [Paragraph("⚡ Powered by AMD MI300X", ParagraphStyle(
                "AMDBadge",
                parent=self.styles["Normal"],
                fontSize=12,
                textColor=AMD_RED,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            ))]
        ]
        amd_table = Table(amd_data, colWidths=[16 * cm])
        amd_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff0f0")),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("BOX", (0, 0), (-1, -1), 1.5, AMD_RED),
            ])
        )
        elements.append(amd_table)
        elements.append(Spacer(1, 2 * cm))

        # Report metadata
        meta_info = [
            ["Generated:", today],
            ["Session ID:", session_id[:8] + "..." if len(session_id) > 8 else session_id],
            ["Platform:", "Clausify AI v1.0.0"],
        ]
        meta_table = Table(meta_info, colWidths=[4 * cm, 12 * cm])
        meta_table.setStyle(
            TableStyle([
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#666666")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ])
        )
        elements.append(meta_table)
        elements.append(Spacer(1, 1 * cm))
        elements.append(HRFlowable(width="100%", thickness=2, color=AMD_RED))

        return elements

    def _build_executive_summary(self, analysis: AnalysisResult) -> list:
        """Build the executive summary section."""
        elements = []
        elements.append(Paragraph("Executive Summary", self.section_header_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=AMD_MED_GRAY))
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(Paragraph(analysis.executiveSummary, self.body_style))
        elements.append(Spacer(1, 0.5 * cm))
        return elements

    def _build_risk_table(self, analysis: AnalysisResult) -> list:
        """Build the risk analysis table section."""
        elements = []
        elements.append(Paragraph("Risk Analysis", self.section_header_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=AMD_MED_GRAY))
        elements.append(Spacer(1, 0.3 * cm))

        if not analysis.risks:
            elements.append(Paragraph("No risks identified.", self.body_style))
            return elements

        # Table headers
        table_data = [
            [
                Paragraph("<b>Level</b>", self.body_style),
                Paragraph("<b>Category</b>", self.body_style),
                Paragraph("<b>Description</b>", self.body_style),
                Paragraph("<b>Source Document</b>", self.body_style),
            ]
        ]

        level_colors = {
            "HIGH": colors.HexColor("#fff0f0"),
            "MEDIUM": colors.HexColor("#fff8e1"),
            "LOW": colors.HexColor("#f0fff4"),
        }
        level_text_colors = {
            "HIGH": AMD_RED,
            "MEDIUM": colors.HexColor("#e65100"),
            "LOW": colors.HexColor("#2e7d32"),
        }

        row_styles = []
        for i, risk in enumerate(analysis.risks, start=1):
            level_color = level_text_colors.get(risk.level, BLACK)
            table_data.append([
                Paragraph(f"<b>{risk.level}</b>", ParagraphStyle(
                    f"Level{i}",
                    parent=self.body_style,
                    textColor=level_text_colors.get(risk.level, BLACK),
                    fontName="Helvetica-Bold",
                )),
                Paragraph(risk.category, self.body_style),
                Paragraph(risk.description, self.body_style),
                Paragraph(risk.sourceDocument, self.label_style),
            ])
            bg = level_colors.get(risk.level, WHITE)
            row_styles.append(("BACKGROUND", (0, i), (-1, i), bg))

        col_widths = [2 * cm, 2.5 * cm, 7.5 * cm, 4 * cm]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), AMD_DARK),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, AMD_MED_GRAY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ])
        for style_cmd in row_styles:
            table_style.add(*style_cmd)
        table.setStyle(table_style)

        elements.append(table)
        elements.append(Spacer(1, 0.5 * cm))
        return elements

    def _build_comparison_matrix(self, analysis: AnalysisResult) -> list:
        """Build the supplier comparison matrix table."""
        elements = []
        elements.append(Paragraph("Supplier Comparison Matrix", self.section_header_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=AMD_MED_GRAY))
        elements.append(Spacer(1, 0.3 * cm))

        if not analysis.comparisonMatrix:
            elements.append(Paragraph("No comparison data available.", self.body_style))
            return elements

        # Collect all supplier names dynamically
        all_suppliers: list[str] = []
        for row in analysis.comparisonMatrix:
            for supplier in row.values.keys():
                if supplier not in all_suppliers:
                    all_suppliers.append(supplier)

        # Build header row
        header = [Paragraph("<b>Criteria</b>", self.body_style)]
        for supplier in all_suppliers:
            header.append(Paragraph(f"<b>{supplier}</b>", self.body_style))
        header.append(Paragraph("<b>Winner</b>", self.body_style))

        table_data = [header]

        for i, row in enumerate(analysis.comparisonMatrix):
            data_row = [Paragraph(row.field, self.body_style)]
            for supplier in all_suppliers:
                val = row.values.get(supplier, "—")
                is_winner = row.winner == supplier
                style = ParagraphStyle(
                    f"CellWinner{i}{supplier}",
                    parent=self.body_style,
                    textColor=colors.HexColor("#2e7d32") if is_winner else BLACK,
                    fontName="Helvetica-Bold" if is_winner else "Helvetica",
                )
                data_row.append(Paragraph(f"{'✓ ' if is_winner else ''}{val}", style))
            data_row.append(
                Paragraph(
                    row.winner or "—",
                    ParagraphStyle(
                        f"Winner{i}",
                        parent=self.body_style,
                        textColor=colors.HexColor("#2e7d32"),
                        fontName="Helvetica-Bold",
                    ),
                )
            )
            table_data.append(data_row)

        num_cols = len(all_suppliers) + 2
        col_width = 16 * cm / num_cols
        col_widths = [col_width] * num_cols

        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), AMD_DARK),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, AMD_MED_GRAY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, AMD_LIGHT_GRAY]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ])
        )

        elements.append(table)
        elements.append(Spacer(1, 0.5 * cm))
        return elements

    def _build_conflicts_section(self, analysis: AnalysisResult) -> list:
        """Build the detected conflicts section."""
        elements = []
        elements.append(Paragraph("Detected Conflicts", self.section_header_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=AMD_MED_GRAY))
        elements.append(Spacer(1, 0.3 * cm))

        if not analysis.conflicts:
            elements.append(
                Paragraph("No conflicts detected between documents.", self.body_style)
            )
            return elements

        severity_colors = {
            "HIGH": AMD_RED,
            "MEDIUM": colors.HexColor("#e65100"),
            "LOW": colors.HexColor("#2e7d32"),
        }

        for i, conflict in enumerate(analysis.conflicts):
            sev_color = severity_colors.get(conflict.severity, BLACK)

            conflict_block = [
                Paragraph(
                    f"<b>{conflict.type}</b> — <font color='#{_color_to_hex(sev_color)}'><b>{conflict.severity}</b></font>",
                    self.body_style,
                ),
                Spacer(1, 0.2 * cm),
            ]

            # Documents comparison table
            doc_data = [
                [
                    Paragraph(f"<b>{conflict.documentA.name}</b>", self.label_style),
                    Paragraph(f"<b>{conflict.documentB.name}</b>", self.label_style),
                ],
                [
                    Paragraph(
                        f'"{conflict.documentA.excerpt}"',
                        self.body_style,
                    ),
                    Paragraph(
                        f'"{conflict.documentB.excerpt}"',
                        self.body_style,
                    ),
                ],
            ]
            doc_table = Table(doc_data, colWidths=[8 * cm, 8 * cm])
            doc_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), AMD_LIGHT_GRAY),
                    ("GRID", (0, 0), (-1, -1), 0.5, AMD_MED_GRAY),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ])
            )
            conflict_block.append(doc_table)
            conflict_block.append(Spacer(1, 0.2 * cm))
            conflict_block.append(
                Paragraph(f"<b>Explanation:</b> {conflict.explanation}", self.body_style)
            )
            conflict_block.append(
                Paragraph(
                    f"<b>Recommended Action:</b> {conflict.recommendedAction}",
                    ParagraphStyle(
                        f"Rec{i}",
                        parent=self.body_style,
                        textColor=colors.HexColor("#1a237e"),
                    ),
                )
            )
            conflict_block.append(Spacer(1, 0.4 * cm))
            conflict_block.append(HRFlowable(width="100%", thickness=0.5, color=AMD_MED_GRAY))

            elements.append(KeepTogether(conflict_block))
            elements.append(Spacer(1, 0.3 * cm))

        return elements

    def _build_recommendation_section(self, analysis: AnalysisResult) -> list:
        """Build the final recommendation section."""
        elements = []
        rec = analysis.recommendation

        elements.append(Paragraph("Recommendation", self.section_header_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=AMD_MED_GRAY))
        elements.append(Spacer(1, 0.3 * cm))

        # Title box
        title_data = [[Paragraph(f"<b>{rec.title}</b>", ParagraphStyle(
            "RecTitle",
            parent=self.body_style,
            fontSize=13,
            textColor=WHITE,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        ))]]
        title_table = Table(title_data, colWidths=[16 * cm])
        title_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), AMD_DARK),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ])
        )
        elements.append(title_table)
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(Paragraph(rec.summary, self.body_style))
        elements.append(Spacer(1, 0.3 * cm))

        # Next steps
        elements.append(Paragraph("<b>Next Steps:</b>", self.body_style))
        for i, step in enumerate(rec.nextSteps, 1):
            elements.append(
                Paragraph(f"&nbsp;&nbsp;{i}. {step}", self.body_style)
            )

        elements.append(Spacer(1, 0.4 * cm))

        # Confidence score
        confidence_pct = int(rec.confidence * 100)
        confidence_color = (
            colors.HexColor("#2e7d32") if rec.confidence >= 0.7
            else colors.HexColor("#e65100") if rec.confidence >= 0.4
            else AMD_RED
        )
        elements.append(
            Paragraph(
                f"<b>Confidence Score:</b> <font color='#{_color_to_hex(confidence_color)}'><b>{confidence_pct}%</b></font>",
                self.body_style,
            )
        )
        elements.append(Spacer(1, 1 * cm))
        elements.append(HRFlowable(width="100%", thickness=2, color=AMD_RED))
        elements.append(Spacer(1, 0.3 * cm))
        elements.append(
            Paragraph(
                "Generated by Clausify AI — Powered by AMD MI300X | clausify.app",
                self.footer_style,
            )
        )

        return elements
