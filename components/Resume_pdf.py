from reportlab.lib.pagesizes import A4
import streamlit as st
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
    KeepTogether
)
from reportlab.lib.units import inch


class ResumePDFBuilder:

    def __init__(self, resume, output_file="Resume.pdf"):
        self.resume = resume
        self.output_file = output_file
        self._create_styles()

    # =====================================================
    # STYLES
    # =====================================================

    def _create_styles(self):

        self.name_style = ParagraphStyle(
            "Name",
            fontName="Helvetica-Bold",
            fontSize=20,
            alignment=TA_CENTER,
            leading=24,
            textColor=HexColor("#1A1A1A")
        )

        self.contact_style = ParagraphStyle(
            "Contact",
            fontName="Helvetica",
            fontSize=9,
            alignment=TA_CENTER,
            leading=13,
            textColor=HexColor("#333333")
        )

        self.section_style = ParagraphStyle(
            "Section",
            fontName="Helvetica-Bold",
            fontSize=11,
            spaceBefore=8,
            spaceAfter=2,
            leading=13,
            textColor=HexColor("#000000"),
            leftIndent=0
        )

        self.body_style = ParagraphStyle(
            "BodyLeft",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            textColor=HexColor("#222222"),
            leftIndent=0,
            firstLineIndent=0
        )

        self.body_right_style = ParagraphStyle(
            "BodyRight",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_RIGHT,
            textColor=HexColor("#222222"),
            rightIndent=0
        )

        self.small_style = ParagraphStyle(
            "Small",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            alignment=TA_LEFT,
            textColor=HexColor("#1A0DAB"),
            leftIndent=0
        )

    # =====================================================
    # HELPERS
    # =====================================================

    def _ensure_url(self, url):
        if not url:
            return ""
        url = url.strip()
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("mailto:")):
            return "https://" + url
        return url

    def _section(self, title, story):
        story.append(
            Paragraph(
                title.upper(),
                self.section_style
            )
        )
        story.append(
            HRFlowable(
                width="100%",
                thickness=0.8,
                color=black,
                spaceAfter=5,
                spaceBefore=2,
                hAlign="LEFT"
            )
        )

    def _bullet(self, text):
        return Paragraph(
            f"• {text}",
            self.body_style
        )

    # =====================================================
    # BUILD PDF
    # =====================================================

    def create(self):

        doc = SimpleDocTemplate(
            self.output_file,
            pagesize=A4,
            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
            topMargin=0.45 * inch,
            bottomMargin=0.45 * inch
        )

        # Printable area: 8.5" - (0.5" left + 0.5" right) = 7.5"
        col_left_width = 5.75 * inch
        col_right_width = 1.75 * inch

        story = []

        # ---------------- HEADER ----------------

        if self.resume.get("name"):
            story.append(
                Paragraph(
                    self.resume.get("name"),
                    self.name_style
                )
            )

        story.append(Spacer(1, 4))

        email = self.resume.get("email", "")
        email_url = f"mailto:{email}" if email else ""
        phone = self.resume.get("phone", "")
        location = self.resume.get("location", "")

        linkedin_url = self._ensure_url(self.resume.get("linkedin", ""))
        github_url = self._ensure_url(self.resume.get("github", ""))
        portfolio_url = self._ensure_url(self.resume.get("portfolio", ""))

        header_parts_line1 = []
        if location:
            header_parts_line1.append(location)
        if phone:
            header_parts_line1.append(phone)
        if email:
            header_parts_line1.append(f'<a href="{email_url}">{email}</a>')

        header_parts_line2 = []
        if portfolio_url:
            header_parts_line2.append(f'<a href="{portfolio_url}">Portfolio</a>')
        if linkedin_url:
            header_parts_line2.append(f'<a href="{linkedin_url}">LinkedIn</a>')
        if github_url:
            github_label = self.resume.get("github", "GitHub").replace("https://", "").replace("http://", "")
            header_parts_line2.append(f'<a href="{github_url}">{github_label}</a>')

        contact_text = f"{' | '.join(header_parts_line1)}<br/>{' | '.join(header_parts_line2)}"

        story.append(
            Paragraph(
                contact_text,
                self.contact_style
            )
        )

        story.append(Spacer(1, 6))

        # ---------------- SUMMARY ----------------

        if self.resume.get("summary"):
            self._section("Summary", story)
            story.append(
                Paragraph(
                    self.resume["summary"],
                    self.body_style
                )
            )

        # ---------------- EDUCATION ----------------

        if "education" in self.resume and self.resume["education"]:
            self._section("Education", story)

            for edu in self.resume["education"]:
                data = [
                    [
                        Paragraph(f"<b>{edu.get('college', '')}</b>", self.body_style),
                        Paragraph(f"<b>{edu.get('year', '')}</b>", self.body_right_style)
                    ],
                    [
                        Paragraph(f"{edu.get('degree', '')}", self.body_style),
                        Paragraph(f"{edu.get('location', '')}", self.body_right_style)
                    ]
                ]

                table = Table(data, colWidths=[col_left_width, col_right_width], hAlign='LEFT')
                table.setStyle(
                    TableStyle([
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ])
                )
                story.append(table)
                story.append(Spacer(1, 4))

        # ---------------- SKILLS ----------------

        if "skills" in self.resume and self.resume["skills"]:
            self._section("Technical Skills", story)

            for item in self.resume["skills"]:
                if isinstance(item, (tuple, list)) and len(item) >= 2:
                    category, skill_list = item[0], item[1]
                    story.append(self._bullet(f"<b>{category}:</b> {skill_list}"))
                elif isinstance(item, str):
                    story.append(self._bullet(item))

        # ---------------- PROJECTS ----------------

        if "projects" in self.resume and self.resume["projects"]:
            self._section("Projects", story)

            for project in self.resume["projects"]:
                block = []

                title_text = f"<b>{project.get('title', '')}</b>"
                if project.get("tech"):
                    title_text += f" | <i>{project.get('tech')}</i>"

                data = [
                    [
                        Paragraph(title_text, self.body_style),
                        Paragraph(f"<b>{project.get('year', '')}</b>", self.body_right_style)
                    ]
                ]

                table = Table(data, colWidths=[col_left_width, col_right_width], hAlign='LEFT')
                table.setStyle(
                    TableStyle([
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ])
                )
                block.append(table)

                # Process Links
                project_links = []

                if project.get("frontend_code_url"):
                    url = self._ensure_url(project["frontend_code_url"])
                    project_links.append(f'<a href="{url}">GitHub Frontend</a>')

                if project.get("backend_code_url"):
                    url = self._ensure_url(project["backend_code_url"])
                    project_links.append(f'<a href="{url}">GitHub Backend</a>')

                if project.get("live_url"):
                    url = self._ensure_url(project["live_url"])
                    project_links.append(f'<a href="{url}">Live</a>')

                if project_links:
                    block.append(
                        Paragraph(
                            f"• <b>Links:</b> {' | '.join(project_links)}",
                            self.small_style
                        )
                    )

                # Bullet points
                for point in project.get("points", []):
                    if point:
                        block.append(self._bullet(point))

                block.append(Spacer(1, 5))
                story.append(KeepTogether(block))

        # ---------------- CERTIFICATIONS ----------------

        if "certifications" in self.resume and self.resume["certifications"]:
            self._section("Certifications", story)

            for cert in self.resume["certifications"]:
                if cert:
                    story.append(self._bullet(cert))

        doc.build(story)
