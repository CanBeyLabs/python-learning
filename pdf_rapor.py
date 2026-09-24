from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import os


REPORT_DIR = "raporlar"

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


def create_pdf(result):

    file_path = os.path.join(
        REPORT_DIR,
        "website_audit_raporu.pdf"
    )

    font_path = (
        "C:/Windows/Fonts/arial.ttf"
    )

    bold_font_path = (
        "C:/Windows/Fonts/arialbd.ttf"
    )

    if os.path.exists(font_path):

        pdfmetrics.registerFont(
            TTFont(
                "Arial",
                font_path
            )
        )

        if os.path.exists(
            bold_font_path
        ):

            pdfmetrics.registerFont(
                TTFont(
                    "ArialBold",
                    bold_font_path
                )
            )

            normal_font = "Arial"
            bold_font = "ArialBold"

        else:

            normal_font = "Arial"
            bold_font = "Arial"

    else:

        normal_font = "Helvetica"
        bold_font = "Helvetica-Bold"


    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    title_style.fontName = bold_font
    title_style.alignment = TA_CENTER
    title_style.fontSize = 22

    heading_style = styles["Heading2"]
    heading_style.fontName = bold_font

    body_style = styles["BodyText"]
    body_style.fontName = normal_font
    body_style.fontSize = 10
    body_style.leading = 14


    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )


    story = []


    story.append(
        Paragraph(
            "LocalAI Website Audit",
            title_style
        )
    )

    story.append(
        Spacer(1, 15)
    )


    story.append(
        Paragraph(
            "Profesyonel Web Sitesi Analiz Raporu",
            heading_style
        )
    )

    story.append(
        Spacer(1, 10)
    )


    business = result.get(
        "business_name",
        "İşletme"
    )

    sector = result.get(
        "sector",
        ""
    )

    city = result.get(
        "city",
        ""
    )

    website = result.get(
        "website",
        ""
    )

    score = result.get(
        "score",
        0
    )

    status = result.get(
        "status",
        ""
    )


    info_data = [

        ["İşletme", business],

        ["Sektör", sector],

        ["Şehir", city],

        ["Web Sitesi", website],

        ["Genel Puan", f"{score}/100"],

        ["Durum", status]

    ]


    info_table = Table(
        info_data,
        colWidths=[120, 350]
    )


    info_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor(
                    "#eeeeee"
                )
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                normal_font
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                bold_font
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                7
            )

        ])
    )


    story.append(
        info_table
    )

    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            "Kategori Puanları",
            heading_style
        )
    )

    story.append(
        Spacer(1, 10)
    )


    scores = result.get(
        "scores",
        {}
    )


    score_data = [

        ["Kategori", "Puan"],

        ["SEO", f"{scores.get('seo', 0)}/100"],

        [
            "Teknik SEO",
            f"{scores.get('technical', 0)}/100"
        ],

        [
            "Local SEO",
            f"{scores.get('local', 0)}/100"
        ],

        [
            "İletişim",
            f"{scores.get('communication', 0)}/100"
        ],

        [
            "İçerik",
            f"{scores.get('content', 0)}/100"
        ]

    ]


    score_table = Table(
        score_data,
        colWidths=[300, 170]
    )


    score_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#222222"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                bold_font
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                normal_font
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    story.append(
        score_table
    )


    story.append(
        PageBreak()
    )


    story.append(
        Paragraph(
            "Kontrol Sonuçları",
            heading_style
        )
    )

    story.append(
        Spacer(1, 10)
    )


    controls = result.get(
        "controls",
        []
    )


    control_data = [
        ["Kontrol", "Sonuç"]
    ]


    for control in controls:

        symbol = (
            "✓"
            if control["success"]
            else "X"
        )

        control_data.append(
            [
                control["name"],
                f"{symbol} {control['detail']}"
            ]
        )


    control_table = Table(
        control_data,
        colWidths=[140, 330]
    )


    control_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#222222"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                bold_font
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                normal_font
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                7
            )

        ])
    )


    story.append(
        control_table
    )


    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            "Geliştirme Önerileri",
            heading_style
        )
    )

    story.append(
        Spacer(1, 10)
    )


    recommendations = result.get(
        "recommendations",
        []
    )


    for recommendation in recommendations:

        story.append(
            Paragraph(
                "• " + recommendation,
                body_style
            )
        )

        story.append(
            Spacer(1, 5)
        )


    story.append(
        PageBreak()
    )


    story.append(
        Paragraph(
            "Hazır SEO Metinleri",
            heading_style
        )
    )

    story.append(
        Spacer(1, 10)
    )


    seo_texts = result.get(
        "seo_texts",
        {}
    )


    seo_data = [

        [
            "TITLE",
            seo_texts.get(
                "title",
                ""
            )
        ],

        [
            "H1",
            seo_texts.get(
                "h1",
                ""
            )
        ],

        [
            "META DESCRIPTION",
            seo_texts.get(
                "meta",
                ""
            )
        ],

        [
            "LOCAL SEO",
            seo_texts.get(
                "local",
                ""
            )
        ],

        [
            "WHATSAPP",
            seo_texts.get(
                "whatsapp",
                ""
            )
        ]

    ]


    seo_table = Table(
        seo_data,
        colWidths=[130, 340]
    )


    seo_table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor(
                    "#eeeeee"
                )
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                bold_font
            ),

            (
                "FONTNAME",
                (1, 0),
                (1, -1),
                normal_font
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    story.append(
        seo_table
    )


    story.append(
        Spacer(1, 25)
    )


    story.append(
        Paragraph(
            "Bu rapor LocalAI Website Audit "
            "tarafından otomatik olarak oluşturulmuştur.",
            body_style
        )
    )


    doc.build(
        story
    )


    return file_path