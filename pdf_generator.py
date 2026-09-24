import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)


font_yolu = "C:/Windows/Fonts/arial.ttf"
font_bold_yolu = "C:/Windows/Fonts/arialbd.ttf"


if os.path.exists(font_yolu):

    pdfmetrics.registerFont(
        TTFont("Arial", font_yolu)
    )

    if os.path.exists(font_bold_yolu):

        pdfmetrics.registerFont(
            TTFont("Arial-Bold", font_bold_yolu)
        )

    normal_font = "Arial"
    bold_font = "Arial-Bold"

else:

    normal_font = "Helvetica"
    bold_font = "Helvetica-Bold"


def pdf_olustur(sonuc):

    klasor = "raporlar"

    os.makedirs(
        klasor,
        exist_ok=True
    )

    pdf_yolu = os.path.join(
        klasor,
        "website_audit_raporu.pdf"
    )


    document = SimpleDocTemplate(

        pdf_yolu,

        pagesize=A4,

        rightMargin=18 * mm,

        leftMargin=18 * mm,

        topMargin=18 * mm,

        bottomMargin=18 * mm
    )


    styles = getSampleStyleSheet()


    baslik = ParagraphStyle(

        "Baslik",

        parent=styles["Title"],

        fontName=bold_font,

        fontSize=24,

        leading=28,

        alignment=TA_CENTER,

        spaceAfter=10
    )


    alt_baslik = ParagraphStyle(

        "AltBaslik",

        parent=styles["Heading2"],

        fontName=bold_font,

        fontSize=14,

        leading=18,

        spaceBefore=10,

        spaceAfter=8
    )


    normal = ParagraphStyle(

        "Normal",

        parent=styles["BodyText"],

        fontName=normal_font,

        fontSize=10,

        leading=15
    )


    puan_style = ParagraphStyle(

        "Puan",

        parent=styles["Title"],

        fontName=bold_font,

        fontSize=32,

        leading=38,

        alignment=TA_CENTER
    )


    metin_style = ParagraphStyle(

        "Metin",

        parent=normal,

        fontSize=9,

        leading=13
    )


    icerik = []


    # ==========================================
    # BAŞLIK
    # ==========================================

    icerik.append(

        Paragraph(
            "LOCALAI WEBSITE AUDIT",
            baslik
        )
    )


    icerik.append(

        Paragraph(

            "Website ve Dijital Görünürlük Analiz Raporu",

            ParagraphStyle(

                "Alt",

                parent=normal,

                alignment=TA_CENTER,

                fontSize=11
            )
        )
    )


    icerik.append(
        Spacer(1, 15)
    )


    icerik.append(

        HRFlowable(

            width="100%",

            thickness=1,

            color=colors.grey
        )
    )


    icerik.append(
        Spacer(1, 15)
    )


    # ==========================================
    # İŞLETME BİLGİLERİ
    # ==========================================

    icerik.append(

        Paragraph(
            "İşletme Bilgileri",
            alt_baslik
        )
    )


    bilgiler = [

        [
            "İşletme",
            sonuc.get(
                "isletme_adi",
                ""
            )
        ],

        [
            "Sektör",
            sonuc.get(
                "sektor",
                ""
            )
        ],

        [
            "Şehir",
            sonuc.get(
                "sehir",
                ""
            )
        ],

        [
            "Website",
            sonuc.get(
                "url",
                ""
            )
        ]

    ]


    bilgi_tablosu = Table(

        bilgiler,

        colWidths=[

            40 * mm,

            120 * mm
        ]
    )


    bilgi_tablosu.setStyle(

        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.whitesmoke
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
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    icerik.append(
        bilgi_tablosu
    )


    icerik.append(
        Spacer(1, 20)
    )


    # ==========================================
    # PUAN
    # ==========================================

    puan = sonuc.get(
        "puan",
        0
    )


    durum = sonuc.get(
        "durum",
        "Bilinmiyor"
    )


    puan_tablosu = Table(

        [

            [

                Paragraph(

                    f"{puan} / 100",

                    puan_style
                )

            ],

            [

                Paragraph(

                    f"Durum: {durum}",

                    ParagraphStyle(

                        "Durum",

                        parent=normal,

                        fontName=bold_font,

                        alignment=TA_CENTER,

                        fontSize=12
                    )
                )

            ]

        ],

        colWidths=[
            160 * mm
        ]
    )


    puan_tablosu.setStyle(

        TableStyle([

            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.whitesmoke
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                12
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                12
            )

        ])
    )


    icerik.append(
        puan_tablosu
    )


    icerik.append(
        Spacer(1, 20)
    )


    # ==========================================
    # KONTROLLER
    # ==========================================

    icerik.append(

        Paragraph(
            "Kontrol Sonuçları",
            alt_baslik
        )
    )


    kontrol_verisi = [

        [
            "Durum",
            "Kontrol"
        ]

    ]


    for kontrol in sonuc.get(
        "kontroller",
        []
    ):

        if kontrol["durum"] == "ok":

            durum_metni = "OK"

        else:

            durum_metni = "EKSİK"


        kontrol_verisi.append(

            [

                durum_metni,

                kontrol["metin"]

            ]

        )


    kontrol_tablosu = Table(

        kontrol_verisi,

        colWidths=[

            30 * mm,

            130 * mm
        ]
    )


    kontrol_tablosu.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.whitesmoke
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
                "MIDDLE"
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )

        ])
    )


    icerik.append(
        kontrol_tablosu
    )


    icerik.append(
        Spacer(1, 20)
    )


    # ==========================================
    # GELİŞTİRME ÖNERİLERİ
    # ==========================================

    icerik.append(

        Paragraph(
            "Geliştirme Önerileri",
            alt_baslik
        )
    )


    oneriler = sonuc.get(
        "oneriler",
        []
    )


    if oneriler:

        for sira, oneri in enumerate(

            oneriler,

            start=1
        ):

            icerik.append(

                Paragraph(

                    f"{sira}. {oneri}",

                    normal
                )
            )

            icerik.append(
                Spacer(1, 5)
            )

    else:

        icerik.append(

            Paragraph(

                "Temel kontrollerde sorun bulunmadı.",

                normal
            )
        )


    # ==========================================
    # HAZIR SEO METİNLERİ
    # ==========================================

    hazir_metinler = sonuc.get(
        "hazir_metinler",
        {}
    )


    icerik.append(
        Spacer(1, 15)
    )


    icerik.append(

        Paragraph(

            "Hazır SEO Metinleri",

            alt_baslik
        )
    )


    seo_verileri = [

        [
            "TITLE",

            hazir_metinler.get(
                "title",
                ""
            )
        ],

        [
            "H1",

            hazir_metinler.get(
                "h1",
                ""
            )
        ],

        [
            "META DESCRIPTION",

            hazir_metinler.get(
                "meta",
                ""
            )
        ],

        [
            "LOCAL SEO METNİ",

            hazir_metinler.get(
                "local",
                ""
            )
        ],

        [
            "WHATSAPP MESAJI",

            hazir_metinler.get(
                "whatsapp",
                ""
            )
        ]

    ]


    seo_tablosu = Table(

        seo_verileri,

        colWidths=[

            40 * mm,

            120 * mm
        ]
    )


    seo_tablosu.setStyle(

        TableStyle([

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.whitesmoke
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
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    icerik.append(
        seo_tablosu
    )


    icerik.append(
        Spacer(1, 25)
    )


    icerik.append(

        HRFlowable(

            width="100%",

            thickness=0.5,

            color=colors.grey
        )
    )


    icerik.append(
        Spacer(1, 8)
    )


    icerik.append(

        Paragraph(

            "Bu rapor LocalAI Website Audit sistemi tarafından otomatik olarak oluşturulmuştur.",

            ParagraphStyle(

                "AltBilgi",

                parent=normal,

                fontSize=8
            )
        )
    )


    document.build(
        icerik
    )


    return pdf_yolu