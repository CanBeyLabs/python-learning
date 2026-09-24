import requests
from bs4 import BeautifulSoup


# ==========================================
# ISLETME BILGILERI
# ==========================================

print("================================")
print("      LOCALAI WEBSITE AUDIT")
print("================================")

isletme_adi = input("Isletme adi: ")
sektor = input("Sektor: ")
sehir = input("Sehir: ")
url = input("Web sitesi: ")


if not url.startswith("http"):
    url = "https://" + url


# ==========================================
# WEBSITE ISTEGI
# ==========================================

try:

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

except requests.exceptions.RequestException as hata:

    print("\nWebsiteye baglanilamadi.")
    print("Hata:", hata)
    exit()


# ==========================================
# WEBSITE KONTROLU
# ==========================================

print("\n================================")
print("       WEBSITE ANALIZI")
print("================================")

print("Isletme:", isletme_adi)
print("Sektor:", sektor)
print("Sehir:", sehir)
print("URL:", url)
print("Durum kodu:", response.status_code)


if response.status_code != 200:

    print("Website aktif degil veya kontrol edilemiyor.")
    exit()


print("Website: AKTIF")


# ==========================================
# HTML
# ==========================================

soup = BeautifulSoup(
    response.text,
    "html.parser"
)


page_text = soup.get_text(
    " ",
    strip=True
)


sayfa_kucuk = response.text.lower()


# ==========================================
# PUAN
# ==========================================

toplam_puan = 0

kontroller = []

oneriler = []


print("\n===== KONTROLLER =====")


# ==========================================
# 1 TITLE
# ==========================================

title = soup.find("title")


if title and title.text.strip():

    print("[OK] Title")

    toplam_puan += 10

    kontroller.append(
        "[OK] Title bulundu"
    )

else:

    print("[X] Title")

    kontroller.append(
        "[X] Title bulunamadi"
    )

    oneriler.append(
        "Title etiketi eklenmeli."
    )


# ==========================================
# 2 META DESCRIPTION
# ==========================================

description = soup.find(
    "meta",
    attrs={
        "name": "description"
    }
)


if description and description.get("content"):

    print("[OK] Meta description")

    toplam_puan += 10

    kontroller.append(
        "[OK] Meta description bulundu"
    )

else:

    print("[X] Meta description")

    kontroller.append(
        "[X] Meta description bulunamadi"
    )

    oneriler.append(
        "Meta description eklenmeli."
    )


# ==========================================
# 3 H1
# ==========================================

h1 = soup.find("h1")


if h1 and h1.text.strip():

    print("[OK] H1")

    toplam_puan += 10

    kontroller.append(
        "[OK] H1 bulundu"
    )

else:

    print("[X] H1")

    kontroller.append(
        "[X] H1 bulunamadi"
    )

    oneriler.append(
        "H1 basligi eklenmeli."
    )


# ==========================================
# 4 HTTPS
# ==========================================

if url.startswith("https://"):

    print("[OK] HTTPS")

    toplam_puan += 10

    kontroller.append(
        "[OK] HTTPS aktif"
    )

else:

    print("[X] HTTPS")

    kontroller.append(
        "[X] HTTPS aktif degil"
    )

    oneriler.append(
        "HTTPS kullanilmali."
    )


# ==========================================
# 5 TELEFON
# ==========================================

telefon_baslangiclari = [
    "050",
    "051",
    "052",
    "053",
    "054",
    "055",
    "056",
    "057",
    "058",
    "059",
    "0212",
    "0216"
]


telefon_bulundu = any(
    numara in page_text
    for numara in telefon_baslangiclari
)


if telefon_bulundu:

    print("[OK] Telefon")

    toplam_puan += 10

    kontroller.append(
        "[OK] Telefon bilgisi bulundu"
    )

else:

    print("[X] Telefon")

    kontroller.append(
        "[X] Telefon bilgisi bulunamadi"
    )

    oneriler.append(
        "Telefon bilgisi gorunur hale getirilmeli."
    )


# ==========================================
# 6 E-POSTA
# ==========================================

if "@" in page_text:

    print("[OK] E-posta")

    toplam_puan += 10

    kontroller.append(
        "[OK] E-posta bilgisi bulundu"
    )

else:

    print("[X] E-posta")

    kontroller.append(
        "[X] E-posta bilgisi bulunamadi"
    )

    oneriler.append(
        "E-posta adresi eklenmeli."
    )


# ==========================================
# 7 WHATSAPP
# ==========================================

whatsapp_bulundu = (
    "wa.me" in sayfa_kucuk
    or "whatsapp" in sayfa_kucuk
)


if whatsapp_bulundu:

    print("[OK] WhatsApp")

    toplam_puan += 10

    kontroller.append(
        "[OK] WhatsApp baglantisi bulundu"
    )

else:

    print("[X] WhatsApp")

    kontroller.append(
        "[X] WhatsApp baglantisi bulunamadi"
    )

    oneriler.append(
        "WhatsApp iletisim baglantisi eklenebilir."
    )


# ==========================================
# 8 ROBOTS.TXT
# ==========================================

robots_url = (
    url.rstrip("/")
    + "/robots.txt"
)


try:

    robots_response = requests.get(
        robots_url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

except requests.exceptions.RequestException:

    robots_response = None


if (
    robots_response
    and robots_response.status_code == 200
):

    print("[OK] robots.txt")

    toplam_puan += 10

    kontroller.append(
        "[OK] robots.txt bulundu"
    )

else:

    print("[X] robots.txt")

    kontroller.append(
        "[X] robots.txt bulunamadi"
    )

    oneriler.append(
        "robots.txt eklenmeli."
    )


# ==========================================
# 9 SITEMAP
# ==========================================

sitemap_url = (
    url.rstrip("/")
    + "/sitemap.xml"
)


try:

    sitemap_response = requests.get(
        sitemap_url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

except requests.exceptions.RequestException:

    sitemap_response = None


if (
    sitemap_response
    and sitemap_response.status_code == 200
):

    print("[OK] sitemap.xml")

    toplam_puan += 10

    kontroller.append(
        "[OK] sitemap.xml bulundu"
    )

else:

    print("[X] sitemap.xml")

    kontroller.append(
        "[X] sitemap.xml bulunamadi"
    )

    oneriler.append(
        "sitemap.xml eklenmeli."
    )


# ==========================================
# 10 GORSELLER
# ==========================================

images = soup.find_all("img")


if len(images) == 0:

    print("[OK] Gorsel kontrolu")

    toplam_puan += 10

    kontroller.append(
        "[OK] Sayfada gorsel bulunmuyor"
    )

else:

    alt_eksik = 0


    for image in images:

        if not image.get("alt"):

            alt_eksik += 1


    if alt_eksik == 0:

        print("[OK] Gorsel ALT etiketleri")

        toplam_puan += 10

        kontroller.append(
            "[OK] Tum gorsellerde ALT var"
        )

    else:

        print(
            "[X] Eksik ALT:",
            alt_eksik
        )

        kontroller.append(
            f"[X] {alt_eksik} gorselde ALT eksik"
        )

        oneriler.append(
            "Gorsellerin ALT etiketleri tamamlanmali."
        )


# ==========================================
# DURUM
# ==========================================

if toplam_puan >= 80:

    durum = "IYI"

elif toplam_puan >= 50:

    durum = "GELISTIRILMELI"

else:

    durum = "ZAYIF"


# ==========================================
# TERMINAL SONUCU
# ==========================================

print("\n================================")
print("          SEO PUANI")
print("================================")

print(
    "PUAN:",
    toplam_puan,
    "/ 100"
)

print(
    "DURUM:",
    durum
)


# ==========================================
# ONERILER
# ==========================================

print("\n===== GELISTIRME ONERILERI =====")


if len(oneriler) == 0:

    print(
        "Temel kontrollerde sorun bulunmadi."
    )

else:

    for oneri in oneriler:

        print(
            "->",
            oneri
        )


# ==========================================
# TXT RAPOR
# ==========================================

rapor = ""

rapor += "================================\n"
rapor += "       LOCALAI WEBSITE AUDIT\n"
rapor += "================================\n\n"

rapor += f"Isletme: {isletme_adi}\n"
rapor += f"Sektor: {sektor}\n"
rapor += f"Sehir: {sehir}\n"
rapor += f"Website: {url}\n"
rapor += f"Durum kodu: {response.status_code}\n"
rapor += f"Sayfa uzunlugu: {len(response.text)}\n\n"


rapor += "SEO PUANI\n"
rapor += "---------\n"

rapor += f"Puan: {toplam_puan} / 100\n"
rapor += f"Durum: {durum}\n\n"


rapor += "KONTROLLER\n"
rapor += "----------\n"


for kontrol in kontroller:

    rapor += kontrol + "\n"


rapor += "\nGELISTIRME ONERILERI\n"
rapor += "--------------------\n"


if len(oneriler) == 0:

    rapor += (
        "Temel kontrollerde sorun bulunmadi.\n"
    )

else:

    for oneri in oneriler:

        rapor += (
            "-> "
            + oneri
            + "\n"
        )


# ==========================================
# DOSYAYA KAYDET
# ==========================================

with open(
    "website_raporu.txt",
    "w",
    encoding="utf-8"
) as dosya:

    dosya.write(rapor)


print("\n================================")
print("       RAPOR OLUSTURULDU")
print("================================")

print(
    "Dosya: website_raporu.txt"
)