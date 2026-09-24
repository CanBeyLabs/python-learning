import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)


# ==========================================
# DOSYA AYARLARI
# ==========================================

TXT_DOSYASI = "website_raporu.txt"
PDF_DOSYASI = "website_audit_raporu.pdf"


# ==========================================
# RAPORU OKU
# ==========================================

with open(
    TXT_DOSYASI,
    "r",
    encoding="utf-8"
) as dosya:

    rapor = dosya.read()


# ==========================================
# BILGILERI BUL
# ==========================================

website = "Bilinmiyor"
puan = 0
durum = "Bilinmiyor"

website_eslesme = re.search(
    r"Website:\s*(.+)",
    rapor
)

if website_eslesme:

    website = website_eslesme.group(1).strip()


puan_eslesme = re.search(
    r"Puan:\s*(\d+)\s*/\s*100",
    rapor
)

if puan_eslesme:

    puan = int(puan_eslesme.group(1))


durum_eslesme = re.search(
    r"Durum:\s*(.+)",
    rapor
)

if durum_eslesme:

    durum = durum_eslesme.group(1).strip()


# ==========================================
# PDF AYARLARI
# ==========================================

document = SimpleDocTemplate(
    PDF_DOSYASI,
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
    fontSize=24,
    leading=28,
    alignment=TA_CENTER,
    spaceAfter=8
)


alt_baslik = ParagraphStyle(
    "AltBaslik",
    parent=styles["Heading2"],
    fontSize=14,
    leading=18,
    spaceBefore=10,
    spaceAfter=8
)


normal = ParagraphStyle(
    "Normal",
    parent=styles["BodyText"],
    fontSize=10,
    leading=15
)


buyuk_puan = ParagraphStyle(
    "BuyukPuan",
    parent=styles["Title"],
    fontSize=32,
    leading=36,
    alignment=TA_CENTER,
    spaceAfter=5
)


kucuk = ParagraphStyle(
    "Kucuk",
    parent=styles["BodyText"],
    fontSize=9,
    leading=12
)


# ==========================================
# PDF ICERIGI
# ==========================================

icerik = []


# BASLIK

icerik.append(
    Paragraph(
        "LOCALAI WEBSITE AUDIT",
        baslik
    )
)


icerik.append(
    Paragraph(
        "Dijital Gorunurluk ve Website Analiz Raporu",
        ParagraphStyle(
            "Alt",
            parent=normal,
            alignment=TA_CENTER,
            fontSize=11
        )
    )
)


icerik.append(
    Spacer(1, 12)
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


# WEBSITE BILGISI

icerik.append(
    Paragraph(
        "Website",
        alt_baslik
    )
)


icerik.append(
    Paragraph(
        website,
        normal
    )
)


icerik.append(
    Spacer(1, 12)
)


# ==========================================
# PUAN KUTUSU
# ==========================================

puan_tablosu = Table(
    [
        [
            Paragraph(
                f"{puan} / 100",
                buyuk_puan
            )
        ],
        [
            Paragraph(
                f"Durum: {durum}",
                ParagraphStyle(
                    "Durum",
                    parent=normal,
                    alignment=TA_CENTER,
                    fontSize=12
                )
            )
        ]
    ],
    colWidths=[160 * mm]
)


puan_tablosu.setStyle(
    TableStyle(
        [
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
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
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
        ]
    )
)


icerik.append(puan_tablosu)


icerik.append(
    Spacer(1, 18)
)


# ==========================================
# KONTROLLER
# ==========================================

icerik.append(
    Paragraph(
        "Kontrol Sonuclari",
        alt_baslik
    )
)


kontrol_satirlari = []


kontrol_basladi = False


for satir in rapor.split("\n"):

    satir = satir.strip()


    if satir == "KONTROLLER":

        kontrol_basladi = True
        continue


    if satir == "GELISTIRME ONERILERI":

        kontrol_basladi = False
        continue


    if kontrol_basladi and satir:

        if satir.startswith("[OK]"):

            kontrol_satirlari.append(
                [
                    "OK",
                    satir.replace("[OK]", "").strip()
                ]
            )

        elif satir.startswith("[X]"):

            kontrol_satirlari.append(
                [
                    "EKSIK",
                    satir.replace("[X]", "").strip()
                ]
            )


if kontrol_satirlari:

    tablo_verisi = [
        ["Durum", "Kontrol"]
    ]

    tablo_verisi.extend(kontrol_satirlari)


    kontrol_tablosu = Table(
        tablo_verisi,
        colWidths=[
            30 * mm,
            130 * mm
        ]
    )


    kontrol_tablosu.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
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
            ]
        )
    )


    icerik.append(kontrol_tablosu)


icerik.append(
    Spacer(1, 18)
)


# ==========================================
# ONERILER
# ==========================================

icerik.append(
    Paragraph(
        "Gelisitirme Onerileri",
        alt_baslik
    )
)


oneri_basladi = False


oneri_listesi = []


for satir in rapor.split("\n"):

    satir = satir.strip()


    if satir == "GELISTIRME ONERILERI":

        oneri_basladi = True
        continue


    if oneri_basladi and satir:

        if satir.startswith("->"):

            oneri_listesi.append(
                satir.replace("->", "").strip()
            )


if oneri_listesi:

    for sira, oneri in enumerate(
        oneri_listesi,
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
            "Temel kontrollerde sorun bulunmadi.",
            normal
        )
    )


# ==========================================
# ALT BILGI
# ==========================================

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
        "Bu rapor otomatik website analiz sistemi tarafindan olusturulmustur.",
        kucuk
    )
)


# ==========================================
# PDF OLUSTUR
# ==========================================

document.build(icerik)


print("\n================================")
print("       PROFESYONEL PDF")
print("================================")

print("PDF olusturuldu:")
print(PDF_DOSYASI)