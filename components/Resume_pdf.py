
import streamlit as st
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import black
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
            fontSize=22,
            alignment=TA_CENTER,
            leading=26
        )


        self.contact_style = ParagraphStyle(
            "Contact",
            fontSize=9,
            alignment=TA_CENTER,
            leading=12
        )


        self.section_style = ParagraphStyle(
            "Section",
            fontName="Helvetica-Bold",
            fontSize=12,
            spaceBefore=12,
            spaceAfter=5,
            leading=14
        )


        self.body_style = ParagraphStyle(
            "Body",
            fontSize=9.5,
            leading=12,
            alignment=TA_LEFT
        )


        self.small_style = ParagraphStyle(
            "Small",
            fontSize=8.8,
            leading=11
        )


    # =====================================================
    # HELPERS
    # =====================================================

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
                color=black
            )
        )


    def _bullet(self, text):

        return Paragraph(
            "• " + text,
            self.body_style
        )


    # =====================================================
    # BUILD PDF
    # =====================================================

    def create(self):

        doc = SimpleDocTemplate(

            self.output_file,

            pagesize=LETTER,

            leftMargin=0.5*inch,

            rightMargin=0.5*inch,

            topMargin=0.45*inch,

            bottomMargin=0.45*inch
        )


        story = []


        # ---------------- HEADER ----------------
        
        # st.write("=================================================")
        
        # st.write(self.resume)
        
        # st.write("=================================================")
        story.append(
            Paragraph(
                self.resume["name"],
                self.name_style
            )
        )


        story.append(
            Spacer(1, 4)
        )


        contact = f"""
        {self.resume['location']} |
        {self.resume['phone']} |
        <link href="mailto:{self.resume['email']}">
        {self.resume['email']}
        </link>
        <br/>
        <link href="{self.resume['portfolio']}">
        {self.resume['portfolio']}
        </link>
        <br/>
        <link href="{self.resume['linkedin']}">
        LinkedIn
        </link>
        |
        <link href="{self.resume['github']}">
        GitHub
        </link>
        """


        story.append(
            Paragraph(
                contact,
                self.contact_style
            )
        )


        story.append(
            Spacer(1, 10)
        )


        # ---------------- SUMMARY ----------------

        self._section(
            "Summary",
            story
        )


        story.append(
            Paragraph(
                self.resume["summary"],
                self.body_style
            )
        )


        # ---------------- EDUCATION ----------------

        self._section(
            "Education",
            story
        )


        for edu in self.resume["education"]:

            data = [

                [

                    Paragraph(
                        f"""
                        <b>{edu['college']}</b><br/>
                        {edu['degree']}
                        """,
                        self.body_style
                    ),


                    Paragraph(
                        f"""
                        {edu['location']}<br/>
                        <b>{edu['year']}</b>
                        """,
                        self.body_style
                    )

                ]

            ]


            table = Table(
                data,
                colWidths=[4.5*inch, 1.5*inch]
            )


            table.setStyle(
                TableStyle(
                    [
                        (
                            "VALIGN",
                            (0,0),
                            (-1,-1),
                            "TOP"
                        ),

                        (
                            "ALIGN",
                            (1,0),
                            (1,0),
                            "RIGHT"
                        )
                    ]
                )
            )


            story.append(table)



        # ---------------- SKILLS ----------------

        self._section(
            "Technical Skills",
            story
        )


        for skill, value in self.resume["skills"]:

            story.append(
                Paragraph(
                    f"<b>{skill}:</b> {value}",
                    self.body_style
                )
            )



        # ---------------- PROJECTS ----------------

        self._section(
            "Projects",
            story
        )


        for project in self.resume["projects"]:

            block = []


            block.append(

                Paragraph(
                    f"""
                    <b>{project['title']}</b>
                    |
                    {project['tech']}
                    <br/>
                    <b>{project['year']}</b>
                    """,
                    self.body_style
                )

            )


            block.append(

                Paragraph(
                    f"""
                    <link href="{project['url']}">
                    {project['links']}
                    </link>
                    """,
                    self.small_style
                )

            )


            for point in project["points"]:

                block.append(
                    self._bullet(point)
                )


            block.append(
                Spacer(1, 6)
            )


            story.append(
                KeepTogether(block)
            )



        # ---------------- CERTIFICATIONS ----------------

        self._section(
            "Certifications",
            story
        )


        for cert in self.resume["certifications"]:

            story.append(
                self._bullet(cert)
            )


        doc.build(story)