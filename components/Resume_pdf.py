# from reportlab.lib.pagesizes import LETTER
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
# from reportlab.lib.colors import HexColor, black
# from reportlab.platypus import (
#     SimpleDocTemplate,
#     Paragraph,
#     Spacer,
#     HRFlowable,
#     Table,
#     TableStyle,
#     KeepTogether
# )
# from reportlab.lib.units import inch

# class ResumePDFBuilder:

#     def __init__(self, resume, output_file="Resume.pdf"):
#         self.resume = resume
#         self.output_file = output_file
#         self._create_styles()

#     # =====================================================
#     # STYLES (Keeping standard font setup)
#     # =====================================================

#     def _create_styles(self):
#         font_regular = "Times-Roman"
#         font_bold = "Times-Bold"
#         font_italic = "Times-Italic"

#         # Candidate Name Header
#         self.name_style = ParagraphStyle(
#             "Name",
#             fontName=font_bold,
#             fontSize=22,
#             alignment=TA_CENTER,
#             leading=24,
#             textColor=HexColor("#000000")
#         )

#         # Contact Details Sub-header
#         self.contact_style = ParagraphStyle(
#             "Contact",
#             fontName=font_regular,
#             fontSize=9.5,
#             alignment=TA_CENTER,
#             leading=13,
#             textColor=HexColor("#1A1A1A")
#         )

#         # Section Titles
#         self.section_style = ParagraphStyle(
#             "Section",
#             fontName=font_bold,
#             fontSize=11.5,
#             spaceBefore=6,
#             spaceAfter=2,
#             leading=13,
#             textColor=HexColor("#000000"),
#             leftIndent=0
#         )

#         # Main Body Text (Flush Left)
#         self.body_style = ParagraphStyle(
#             "BodyLeft",
#             fontName=font_regular,
#             fontSize=10,
#             leading=12.5,
#             alignment=TA_LEFT,
#             textColor=HexColor("#000000"),
#             leftIndent=0,
#             firstLineIndent=0
#         )

#         # Main Body Text (Right-Aligned for Dates & Locations)
#         self.body_right_style = ParagraphStyle(
#             "BodyRight",
#             fontName=font_regular,
#             fontSize=10,
#             leading=12.5,
#             alignment=TA_RIGHT,
#             textColor=HexColor("#000000"),
#             rightIndent=0
#         )

#         # Indented Bullet List Items
#         self.bullet_style = ParagraphStyle(
#             "IndentedBullet",
#             fontName=font_regular,
#             fontSize=9.5,
#             leading=12,
#             alignment=TA_LEFT,
#             textColor=HexColor("#000000"),
#             leftIndent=18,
#             firstLineIndent=-10
#         )

#         # Indented Links Line
#         self.links_style = ParagraphStyle(
#             "IndentedLinks",
#             fontName=font_regular,
#             fontSize=9.5,
#             leading=12,
#             alignment=TA_LEFT,
#             textColor=HexColor("#003366"),
#             leftIndent=18,
#             firstLineIndent=-10
#         )

#     # =====================================================
#     # HELPER METHODS
#     # =====================================================

#     def _ensure_url(self, url):
#         if not url:
#             return ""
#         url = url.strip()
#         if not (url.startswith("http://") or url.startswith("https://") or url.startswith("mailto:")):
#             return "https://" + url
#         return url

#     def _section(self, title, story):
#         story.append(
#             Paragraph(
#                 title,
#                 self.section_style
#             )
#         )
#         story.append(
#             HRFlowable(
#                 width="100%",
#                 thickness=0.6,
#                 color=black,
#                 spaceAfter=4,
#                 spaceBefore=1,
#                 hAlign="LEFT"
#             )
#         )

#     # =====================================================
#     # BUILD PDF
#     # =====================================================

#     def create(self):
#         pdf_buffer = io.BytesIO()
        
#         left_margin = 0.5 * inch
#         right_margin = 0.5 * inch
        
#         doc = SimpleDocTemplate(
#             pdf_buffer,
#             pagesize=LETTER,
#             leftMargin=left_margin,
#             rightMargin=right_margin,
#             topMargin=0.45 * inch,
#             bottomMargin=0.45 * inch
#         )

#         printable_width = LETTER[0] - (left_margin + right_margin)
#         col_right_width = 1.85 * inch
#         col_left_width = printable_width - col_right_width

#         story = []

#         # ---------------- HEADER ----------------

#         if self.resume.get("name"):
#             name_text = self.resume.get("name")
#             story.append(Paragraph(name_text, self.name_style))

#         story.append(Spacer(1, 3))

#         location = self.resume.get("location", "")
#         email = self.resume.get("email", "")
#         email_url = f"mailto:{email}" if email else ""
#         phone = self.resume.get("phone", "")

#         linkedin_url = self._ensure_url(self.resume.get("linkedin", ""))
#         github_url = self._ensure_url(self.resume.get("github", ""))
#         portfolio_url = self._ensure_url(self.resume.get("portfolio", ""))

#         # Line 1 Structure: Location | Phone | Email
#         contact_line1 = []
#         if location:
#             contact_line1.append(location)
#         if phone:
#             contact_line1.append(phone)
#         if email:
#             contact_line1.append(f'<a href="{email_url}">{email}</a>')

#         # Line 2 Structure: Portfolio | LinkedIn | GitHub
#         contact_line2 = []
#         if portfolio_url:
#             contact_line2.append(f'<a href="{portfolio_url}">Portfolio</a>')
#         if linkedin_url:
#             contact_line2.append(f'<a href="{linkedin_url}">LinkedIn</a>')
#         if github_url:
#             github_label = self.resume.get("github", "github").replace("https://", "").replace("http://", "")
#             contact_line2.append(f'<a href="{github_url}">{github_label}</a>')

#         if contact_line1:
#             story.append(Paragraph(" | ".join(contact_line1), self.contact_style))
#             story.append(Spacer(1, 1.5))

#         if contact_line2:
#             story.append(Paragraph(" | ".join(contact_line2), self.contact_style))

#         story.append(Spacer(1, 6))
        
        

#         # ---------------- EDUCATION ----------------

#         if self.resume.get("education"):
#             self._section("Education", story)

#             for edu in self.resume["education"]:
#                 data = [
#                     [
#                         Paragraph(f"<b>{edu.get('college', '')}</b>", self.body_style),
#                         Paragraph(f"<b>{edu.get('year', '')}</b>", self.body_right_style)
#                     ],
#                     [
#                         Paragraph(f"<i>{edu.get('degree', '')}</i>", self.body_style),
#                         Paragraph(f"<i>{edu.get('location', '')}</i>", self.body_right_style)
#                     ]
#                 ]

#                 table = Table(data, colWidths=[col_left_width, col_right_width], hAlign='LEFT')
#                 table.setStyle(
#                     TableStyle([
#                         ("VALIGN", (0, 0), (-1, -1), "TOP"),
#                         ("LEFTPADDING", (0, 0), (-1, -1), 0),
#                         ("RIGHTPADDING", (0, 0), (-1, -1), 0),
#                         ("TOPPADDING", (0, 0), (-1, -1), 0),
#                         ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
#                     ])
#                 )
#                 story.append(table)
#                 story.append(Spacer(1, 3))

#         # ---------------- SKILLS ----------------

#         if self.resume.get("skills"):
#             self._section("Technical Skills", story)

#             for item in self.resume["skills"]:
#                 if isinstance(item, (tuple, list)) and len(item) >= 2:
#                     category, skill_list = item[0], item[1]
#                     story.append(Paragraph(f"• &nbsp;<b>{category}:</b> {skill_list}", self.bullet_style))
#                 elif isinstance(item, str):
#                     story.append(Paragraph(f"• &nbsp;{item}", self.bullet_style))
            
#             story.append(Spacer(1, 4))

#         # ---------------- PROJECTS ----------------

#         if self.resume.get("projects"):
#             self._section("Projects", story)

#             for project in self.resume["projects"]:
#                 block = []

#                 title_text = f"<b>{project.get('title', '')}</b>"
#                 if project.get("tech"):
#                     title_text += f" | <i>{project.get('tech')}</i>"

#                 data = [
#                     [
#                         Paragraph(title_text, self.body_style),
#                         Paragraph(f"<b>{project.get('year', '')}</b>", self.body_right_style)
#                     ]
#                 ]

#                 table = Table(data, colWidths=[col_left_width, col_right_width], hAlign='LEFT')
#                 table.setStyle(
#                     TableStyle([
#                         ("VALIGN", (0, 0), (-1, -1), "TOP"),
#                         ("LEFTPADDING", (0, 0), (-1, -1), 0),
#                         ("RIGHTPADDING", (0, 0), (-1, -1), 0),
#                         ("TOPPADDING", (0, 0), (-1, -1), 0),
#                         ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
#                     ])
#                 )
#                 block.append(table)

#                 # Process Links
#                 project_links = []
#                 if project.get("frontend_code_url"):
#                     url = self._ensure_url(project["frontend_code_url"])
#                     project_links.append(f'<a href="{url}">GitHub Frontend</a>')

#                 if project.get("backend_code_url"):
#                     url = self._ensure_url(project["backend_code_url"])
#                     project_links.append(f'<a href="{url}">GitHub Backend</a>')

#                 if project.get("live_url"):
#                     url = self._ensure_url(project["live_url"])
#                     project_links.append(f'<a href="{url}">Live</a>')

#                 if project_links:
#                     block.append(
#                         Paragraph(
#                             f"• &nbsp;<b>Links:</b> {' | '.join(project_links)}",
#                             self.links_style
#                         )
#                     )

#                 # Bullet points
#                 for point in project.get("points", []):
#                     if point:
#                         block.append(Paragraph(f"• &nbsp;{point}", self.bullet_style))

#                 block.append(Spacer(1, 5))
#                 story.append(KeepTogether(block))

#         # ---------------- CERTIFICATIONS ----------------

#         if self.resume.get("certifications"):
#             self._section("Certifications", story)

#             for cert in self.resume["certifications"]:
#                 if isinstance(cert, (tuple, list)) and len(cert) >= 2:
#                     title, inst = cert[0], cert[1]
#                     data = [
#                         [
#                             Paragraph(f"• &nbsp;<b>{title}</b>", self.bullet_style),
#                             Paragraph(f"<i>{inst}</i>", self.body_right_style)
#                         ]
#                     ]
#                     table = Table(data, colWidths=[col_left_width, col_right_width], hAlign='LEFT')
#                     table.setStyle(
#                         TableStyle([
#                             ("VALIGN", (0, 0), (-1, -1), "TOP"),
#                             ("LEFTPADDING", (0, 0), (-1, -1), 0),
#                             ("RIGHTPADDING", (0, 0), (-1, -1), 0),
#                             ("TOPPADDING", (0, 0), (-1, -1), 0),
#                             ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
#                         ])
#                     )
#                     story.append(table)
#                 elif cert:
#                     story.append(Paragraph(f"• &nbsp;{cert}", self.bullet_style))

#             story.append(Spacer(1, 4))

#         # ---------------- ACHIEVEMENTS ----------------

#         if self.resume.get("achievements"):
#             self._section("Achievements", story)

#             for ach in self.resume["achievements"]:
#                 if ach:
#                     story.append(Paragraph(f"• &nbsp;{ach}", self.bullet_style))

#         # Build and Return Bytes
#         doc.build(story)
#         pdf_bytes = pdf_buffer.getvalue()
#         pdf_buffer.close()
#         return pdf_bytes



import io
import os
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
        font_regular = "Times-Roman"
        font_bold = "Times-Bold"
        font_italic = "Times-Italic"

        # Candidate Name Header
        self.name_style = ParagraphStyle(
            "Name",
            fontName=font_bold,
            fontSize=22,
            alignment=TA_CENTER,
            leading=24,
            textColor=HexColor("#000000")
        )

        # Contact Details Sub-header
        self.contact_style = ParagraphStyle(
            "Contact",
            fontName=font_regular,
            fontSize=9.5,
            alignment=TA_CENTER,
            leading=13,
            textColor=HexColor("#1A1A1A")
        )

        # Section Titles
        self.section_style = ParagraphStyle(
            "Section",
            fontName=font_bold,
            fontSize=11.5,
            spaceBefore=6,
            spaceAfter=2,
            leading=13,
            textColor=HexColor("#000000"),
            leftIndent=0
        )

        # Main Body Text (Flush Left)
        self.body_style = ParagraphStyle(
            "BodyLeft",
            fontName=font_regular,
            fontSize=10,
            leading=12.5,
            alignment=TA_LEFT,
            textColor=HexColor("#000000"),
            leftIndent=0,
            firstLineIndent=0
        )

        # Summary Paragraph Style (Flush Left, Clean Spacing)
        self.summary_style = ParagraphStyle(
            "SummaryBody",
            fontName=font_regular,
            fontSize=9.5,
            leading=12.5,
            alignment=TA_LEFT,
            textColor=HexColor("#000000"),
            leftIndent=0,
            firstLineIndent=0
        )

        # Main Body Text (Right-Aligned for Dates & Locations)
        self.body_right_style = ParagraphStyle(
            "BodyRight",
            fontName=font_regular,
            fontSize=10,
            leading=12.5,
            alignment=TA_RIGHT,
            textColor=HexColor("#000000"),
            rightIndent=0
        )

        # Indented Bullet List Items
        self.bullet_style = ParagraphStyle(
            "IndentedBullet",
            fontName=font_regular,
            fontSize=9.5,
            leading=12,
            alignment=TA_LEFT,
            textColor=HexColor("#000000"),
            leftIndent=18,
            firstLineIndent=-10
        )

        # Indented Links Line
        self.links_style = ParagraphStyle(
            "IndentedLinks",
            fontName=font_regular,
            fontSize=9.5,
            leading=12,
            alignment=TA_LEFT,
            textColor=HexColor("#003366"),
            leftIndent=18,
            firstLineIndent=-10
        )

    # =====================================================
    # HELPER METHODS
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
                title,
                self.section_style
            )
        )
        story.append(
            HRFlowable(
                width="100%",
                thickness=0.6,
                color=black,
                spaceAfter=4,
                spaceBefore=1,
                hAlign="LEFT"
            )
        )

    # =====================================================
    # BUILD PDF
    # =====================================================

    def create(self):
        pdf_buffer = io.BytesIO()
        
        left_margin = 0.5 * inch
        right_margin = 0.5 * inch
        
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=LETTER,
            leftMargin=left_margin,
            rightMargin=right_margin,
            topMargin=0.45 * inch,
            bottomMargin=0.45 * inch
        )

        printable_width = LETTER[0] - (left_margin + right_margin)
        col_right_width = 1.85 * inch
        col_left_width = printable_width - col_right_width

        story = []

        # ---------------- HEADER ----------------

        if self.resume.get("name"):
            name_text = self.resume.get("name")
            story.append(Paragraph(name_text, self.name_style))

        story.append(Spacer(1, 3))

        location = self.resume.get("location", "")
        email = self.resume.get("email", "")
        email_url = f"mailto:{email}" if email else ""
        phone = self.resume.get("phone", "")

        linkedin_url = self._ensure_url(self.resume.get("linkedin", ""))
        github_url = self._ensure_url(self.resume.get("github", ""))
        portfolio_url = self._ensure_url(self.resume.get("portfolio", ""))

        # Line 1 Structure: Location | Phone | Email
        contact_line1 = []
        if location:
            contact_line1.append(location)
        if phone:
            contact_line1.append(phone)
        if email:
            contact_line1.append(f'<a href="{email_url}">{email}</a>')

        # Line 2 Structure: Portfolio | LinkedIn | GitHub
        contact_line2 = []
        if portfolio_url:
            contact_line2.append(f'<a href="{portfolio_url}">Portfolio</a>')
        if linkedin_url:
            contact_line2.append(f'<a href="{linkedin_url}">LinkedIn</a>')
        if github_url:
            github_label = self.resume.get("github", "github").replace("https://", "").replace("http://", "")
            contact_line2.append(f'<a href="{github_url}">{github_label}</a>')

        if contact_line1:
            story.append(Paragraph(" | ".join(contact_line1), self.contact_style))
            story.append(Spacer(1, 1.5))

        if contact_line2:
            story.append(Paragraph(" | ".join(contact_line2), self.contact_style))

        story.append(Spacer(1, 6))

        # ---------------- SUMMARY ----------------

        if self.resume.get("summary"):
            self._section("Summary", story)
            story.append(
                Paragraph(
                    self.resume["summary"],
                    self.summary_style
                )
            )
            story.append(Spacer(1, 4))

        # ---------------- EDUCATION ----------------

        if self.resume.get("education"):
            self._section("Education", story)

            for edu in self.resume["education"]:
                data = [
                    [
                        Paragraph(f"<b>{edu.get('college', '')}</b>", self.body_style),
                        Paragraph(f"<b>{edu.get('year', '')}</b>", self.body_right_style)
                    ],
                    [
                        Paragraph(f"<i>{edu.get('degree', '')}</i>", self.body_style),
                        Paragraph(f"<i>{edu.get('location', '')}</i>", self.body_right_style)
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
                story.append(Spacer(1, 3))

        # ---------------- SKILLS ----------------

        if self.resume.get("skills"):
            self._section("Technical Skills", story)

            for item in self.resume["skills"]:
                if isinstance(item, (tuple, list)) and len(item) >= 2:
                    category, skill_list = item[0], item[1]
                    story.append(Paragraph(f"• &nbsp;<b>{category}:</b> {skill_list}", self.bullet_style))
                elif isinstance(item, str):
                    story.append(Paragraph(f"• &nbsp;{item}", self.bullet_style))
            
            story.append(Spacer(1, 4))

        # ---------------- PROJECTS ----------------

        if self.resume.get("projects"):
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
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
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
                            f"• &nbsp;<b>Links:</b> {' | '.join(project_links)}",
                            self.links_style
                        )
                    )

                # Bullet points
                for point in project.get("points", []):
                    if point:
                        block.append(Paragraph(f"• &nbsp;{point}", self.bullet_style))

                block.append(Spacer(1, 5))
                story.append(KeepTogether(block))

        # ---------------- CERTIFICATIONS ----------------

        if self.resume.get("certifications"):
            self._section("Certifications", story)

            for cert in self.resume["certifications"]:
                if isinstance(cert, (tuple, list)) and len(cert) >= 2:
                    title, inst = cert[0], cert[1]
                    data = [
                        [
                            Paragraph(f"• &nbsp;<b>{title}</b>", self.bullet_style),
                            Paragraph(f"<i>{inst}</i>", self.body_right_style)
                        ]
                    ]
                    table = Table(data, colWidths=[col_left_width, col_right_width], hAlign='LEFT')
                    table.setStyle(
                        TableStyle([
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                            ("TOPPADDING", (0, 0), (-1, -1), 0),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                        ])
                    )
                    story.append(table)
                elif cert:
                    story.append(Paragraph(f"• &nbsp;{cert}", self.bullet_style))

            story.append(Spacer(1, 4))

        # ---------------- ACHIEVEMENTS ----------------

        if self.resume.get("achievements"):
            self._section("Achievements", story)

            for ach in self.resume["achievements"]:
                if ach:
                    story.append(Paragraph(f"• &nbsp;{ach}", self.bullet_style))

        # Build and Return Bytes
        doc.build(story)
        pdf_bytes = pdf_buffer.getvalue()
        pdf_buffer.close()
        return pdf_bytes