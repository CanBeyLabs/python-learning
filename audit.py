import requests
from bs4 import BeautifulSoup


def website_analiz_et(url):

    if not url.startswith("http"):
        url = "https://" + url

    sonuc = {
        "url": url,
        "aktif": False,
        "puan": 0,
        "durum": "",
        "kontroller": [],
        "oneriler": []
    }

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

    except requests.exceptions.RequestException as hata:

        sonuc["durum"] = "Websiteye baglanilamadi."
        sonuc["hata"] = str(hata)

        return sonuc


    if response.status_code != 200:

        sonuc["durum"] = "Website aktif degil."

        return sonuc


    sonuc["aktif"] = True


    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    page_text = soup.get_text(
        " ",
        strip=True
    )


    sayfa_kucuk = response.text.lower()


    toplam_puan = 0


    # TITLE

    title = soup.find("title")

    if title and title.text.strip():

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "Title bulundu"
            }
        )

    else:

        sonuc["kontroller"].append(
            {
                "durum": "eksik",
                "metin": "Title bulunamadi"
            }
        )

        sonuc["oneriler"].append(
            "Title etiketi eklenmeli."
        )


    # META DESCRIPTION

    description = soup.find(
        "meta",
        attrs={
            "name": "description"
        }
    )


    if description and description.get("content"):

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "Meta description bulundu"
            }
        )

    else:

        sonuc["kontroller"].append(
            {
                "durum": "eksik",
                "metin": "Meta description bulunamadi"
            }
        )

        sonuc["oneriler"].append(
            "Meta description eklenmeli."
        )


    # H1

    h1 = soup.find("h1")


    if h1 and h1.text.strip():

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "H1 bulundu"
            }
        )

    else:

        sonuc["kontroller"].append(
            {
                "durum": "eksik",
                "metin": "H1 bulunamadi"
            }
        )

        sonuc["oneriler"].append(
            "H1 basligi eklenmeli."
        )


    # HTTPS

    if url.startswith("https://"):

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "HTTPS aktif"
            }
        )

    else:

        sonuc["kontroller"].append(
            {
                "durum": "eksik",
                "metin": "HTTPS aktif degil"
            }
        )

        sonuc["oneriler"].append(
            "HTTPS kullanilmali."
        )


    # TELEFON

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

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "Telefon bilgisi bulundu"
            }
        )

    else:

        sonuc["kontroller"].append(
            {
                "durum": "eksik",
                "metin": "Telefon bilgisi bulunamadi"
            }
        )

        sonuc["oneriler"].append(
            "Telefon bilgisi gorunur hale getirilmeli."
        )


    # E-POSTA

    if "@" in page_text:

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "E-posta bilgisi bulundu"
            }
        )

    else:

        sonuc["kontroller"].append(
            {
                "durum": "eksik",
                "metin": "E-posta bilgisi bulunamadi"
            }
        )

        sonuc["oneriler"].append(
            "E-posta adresi eklenmeli."
        )


    # WHATSAPP

    whatsapp_bulundu = (
        "wa.me" in sayfa_kucuk
        or "whatsapp" in sayfa_kucuk
    )


    if whatsapp_bulundu:

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "WhatsApp baglantisi bulundu"
            }
        )

    else:

        sonuc["kontroller"].append(
            {
                "durum": "eksik",
                "metin": "WhatsApp baglantisi bulunamadi"
            }
        )

        sonuc["oneriler"].append(
            "WhatsApp iletisim baglantisi eklenebilir."
        )


    # ROBOTS.TXT

    robots_url = url.rstrip("/") + "/robots.txt"


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

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "robots.txt bulundu"
            }
        )

    else:

        sonuc["kontroller"].append(
            {
                "durum": "eksik",
                "metin": "robots.txt bulunamadi"
            }
        )

        sonuc["oneriler"].append(
            "robots.txt eklenmeli."
        )


    # SITEMAP

    sitemap_url = url.rstrip("/") + "/sitemap.xml"


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

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "sitemap.xml bulundu"
            }
        )

    else:

        sonuc["kontroller"].append(
            {
                "durum": "eksik",
                "metin": "sitemap.xml bulunamadi"
            }
        )

        sonuc["oneriler"].append(
            "sitemap.xml eklenmeli."
        )


    # GORSELLER

    images = soup.find_all("img")


    if len(images) == 0:

        toplam_puan += 10

        sonuc["kontroller"].append(
            {
                "durum": "ok",
                "metin": "Sayfada gorsel bulunmuyor"
            }
        )

    else:

        alt_eksik = 0


        for image in images:

            if not image.get("alt"):

                alt_eksik += 1


        if alt_eksik == 0:

            toplam_puan += 10

            sonuc["kontroller"].append(
                {
                    "durum": "ok",
                    "metin": "Tum gorsellerde ALT var"
                }
            )

        else:

            sonuc["kontroller"].append(
                {
                    "durum": "eksik",
                    "metin": f"{alt_eksik} gorselde ALT eksik"
                }
            )

            sonuc["oneriler"].append(
                "Gorsellerin ALT etiketleri tamamlanmali."
            )


    # DURUM

    if toplam_puan >= 80:

        durum = "IYI"

    elif toplam_puan >= 50:

        durum = "GELISTIRILMELI"

    else:

        durum = "ZAYIF"


    sonuc["puan"] = toplam_puan
    sonuc["durum"] = durum


    return sonuc