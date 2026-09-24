import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re
import ipaddress
import socket


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/140.0 Safari/537.36 "
        "LocalAIWebsiteAudit/1.0"
    )
}


def normalize_url(url):
    url = url.strip()

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url.rstrip("/")


def is_safe_url(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return False

        hostname = parsed.hostname

        if not hostname:
            return False

        blocked_names = {
            "localhost",
            "localhost.localdomain"
        }

        if hostname.lower() in blocked_names:
            return False

        try:
            ip = ipaddress.ip_address(hostname)

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
            ):
                return False

        except ValueError:
            pass

        try:
            resolved = socket.gethostbyname(hostname)
            ip = ipaddress.ip_address(resolved)

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
            ):
                return False

        except Exception:
            pass

        return True

    except Exception:
        return False


def fetch_page(url):
    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
            allow_redirects=True
        )

        return response, None

    except requests.exceptions.Timeout:

        return None, "Web sitesi zaman aşımına uğradı."

    except requests.exceptions.ConnectionError:

        return None, "Web sitesine bağlanılamadı."

    except Exception as hata:

        return None, str(hata)


def text_contains(text, patterns):
    text = text.lower()

    for pattern in patterns:

        if pattern.lower() in text:
            return True

    return False


def calculate_scores(checks):

    seo = 0
    technical = 0
    local = 0
    communication = 0
    content = 0

    if checks["title"]:
        seo += 20

    if checks["meta"]:
        seo += 20

    if checks["h1"]:
        seo += 20

    if checks["canonical"]:
        seo += 15

    if checks["og"]:
        seo += 10

    if checks["schema"]:
        seo += 15

    if checks["https"]:
        technical += 30

    if checks["viewport"]:
        technical += 25

    if checks["robots"]:
        technical += 20

    if checks["sitemap"]:
        technical += 25

    if checks["city"]:
        local += 30

    if checks["sector"]:
        local += 30

    if checks["address"]:
        local += 20

    if checks["phone"]:
        local += 20

    if checks["phone"]:
        communication += 30

    if checks["email"]:
        communication += 25

    if checks["whatsapp"]:
        communication += 25

    if checks["contact_page"]:
        communication += 20

    if checks["word_count"] >= 300:
        content += 35

    elif checks["word_count"] >= 150:
        content += 20

    else:
        content += 5

    if checks["images"] > 0:
        content += 25

    if checks["images_alt_ratio"] >= 0.7:
        content += 20

    if checks["internal_links"] >= 5:
        content += 20

    total = round(
        (
            seo
            + technical
            + local
            + communication
            + content
        ) / 5
    )

    return {
        "seo": min(seo, 100),
        "technical": min(technical, 100),
        "local": min(local, 100),
        "communication": min(communication, 100),
        "content": min(content, 100),
        "total": min(total, 100)
    }


def status_from_score(score):

    if score >= 85:
        return "MÜKEMMEL"

    if score >= 70:
        return "İYİ"

    if score >= 50:
        return "GELİŞTİRİLMELİ"

    return "KRİTİK"


def generate_recommendations(checks):

    recommendations = []

    if not checks["title"]:
        recommendations.append(
            "SEO title eklenmeli."
        )

    elif checks["title_length"] < 30:
        recommendations.append(
            "SEO title daha açıklayıcı hale getirilmeli."
        )

    elif checks["title_length"] > 65:
        recommendations.append(
            "SEO title daha kısa hale getirilmeli."
        )

    if not checks["meta"]:
        recommendations.append(
            "Meta description eklenmeli."
        )

    if not checks["h1"]:
        recommendations.append(
            "Sayfaya bir H1 başlığı eklenmeli."
        )

    if not checks["phone"]:
        recommendations.append(
            "Telefon numarası web sitesinde görünür hale getirilmeli."
        )

    if not checks["email"]:
        recommendations.append(
            "İletişim için e-posta adresi eklenebilir."
        )

    if not checks["whatsapp"]:
        recommendations.append(
            "Müşterilerin hızlı iletişim kurması için WhatsApp bağlantısı eklenebilir."
        )

    if not checks["address"]:
        recommendations.append(
            "İşletme adresi web sitesinde görünür hale getirilmeli."
        )

    if not checks["city"]:
        recommendations.append(
            "Hizmet verilen şehir/bölge metin içerisinde daha net kullanılmalı."
        )

    if not checks["schema"]:
        recommendations.append(
            "LocalBusiness yapılandırılmış verisi eklenmeli."
        )

    if not checks["canonical"]:
        recommendations.append(
            "Canonical URL eklenmeli."
        )

    if not checks["viewport"]:
        recommendations.append(
            "Mobil uyumluluk için viewport etiketi eklenmeli."
        )

    if checks["word_count"] < 300:
        recommendations.append(
            "Ana sayfadaki açıklayıcı içerik artırılmalı."
        )

    if checks["images"] > 0 and checks["images_alt_ratio"] < 0.7:
        recommendations.append(
            "Görsellerin alt açıklamaları tamamlanmalı."
        )

    if not checks["sitemap"]:
        recommendations.append(
            "sitemap.xml oluşturulmalı."
        )

    if not checks["robots"]:
        recommendations.append(
            "robots.txt oluşturulmalı."
        )

    if not recommendations:
        recommendations.append(
            "Temel kontroller başarılı. Daha ileri seviye Local SEO ve içerik optimizasyonu yapılabilir."
        )

    return recommendations


def generate_seo_texts(
    business_name,
    sector,
    city
):

    business_name = business_name or "İşletmeniz"
    sector = sector or "hizmet"
    city = city or "bölgenizde"

    title = (
        f"{business_name} | {city} {sector}"
    )

    h1 = (
        f"{city} {sector} | {business_name}"
    )

    meta = (
        f"{business_name}, {city} bölgesinde "
        f"profesyonel {sector} hizmetleri sunmaktadır. "
        f"Hızlı, güvenilir ve kaliteli hizmet için bizimle iletişime geçin."
    )

    local = (
        f"{business_name}, {city} bölgesinde "
        f"{sector} hizmeti sunmaktadır. "
        f"Hizmetlerimiz hakkında bilgi almak ve teklif almak için "
        f"bizimle iletişime geçebilirsiniz."
    )

    whatsapp = (
        f"Merhaba, {city} {sector} hizmetiniz hakkında "
        f"bilgi almak istiyorum."
    )

    return {
        "title": title,
        "h1": h1,
        "meta": meta,
        "local": local,
        "whatsapp": whatsapp
    }


def audit_website(
    website,
    business_name="",
    sector="",
    city=""
):

    website = normalize_url(website)

    if not website:
        return {
            "success": False,
            "error": "Web sitesi adresi boş."
        }

    if not is_safe_url(website):
        return {
            "success": False,
            "error": "Geçerli ve güvenli bir web sitesi adresi girin."
        }

    response, error = fetch_page(website)

    if error:

        return {
            "success": False,
            "error": error
        }

    if response is None:

        return {
            "success": False,
            "error": "Web sitesi analiz edilemedi."
        }

    final_url = response.url

    html = response.text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    page_text = soup.get_text(
        " ",
        strip=True
    )

    page_text_lower = page_text.lower()

    title_tag = soup.find("title")

    title = (
        title_tag.get_text(strip=True)
        if title_tag
        else ""
    )

    meta_tag = soup.find(
        "meta",
        attrs={"name": re.compile(
            "^description$",
            re.I
        )}
    )

    meta_description = (
        meta_tag.get("content", "").strip()
        if meta_tag
        else ""
    )

    h1_tag = soup.find("h1")

    h1 = (
        h1_tag.get_text(strip=True)
        if h1_tag
        else ""
    )

    canonical_tag = soup.find(
        "link",
        attrs={"rel": lambda value:
               value and "canonical" in value}
    )

    canonical = bool(canonical_tag)

    viewport = bool(
        soup.find(
            "meta",
            attrs={
                "name": re.compile(
                    "^viewport$",
                    re.I
                )
            }
        )
    )

    og_title = soup.find(
        "meta",
        attrs={
            "property": "og:title"
        }
    )

    og_description = soup.find(
        "meta",
        attrs={
            "property": "og:description"
        }
    )

    og = bool(
        og_title or og_description
    )

    schema_tags = soup.find_all(
        "script",
        attrs={
            "type": "application/ld+json"
        }
    )

    schema = len(schema_tags) > 0

    images = soup.find_all("img")

    images_with_alt = 0

    for image in images:

        alt = image.get("alt")

        if alt and alt.strip():
            images_with_alt += 1

    if images:
        images_alt_ratio = round(
            images_with_alt / len(images),
            2
        )
    else:
        images_alt_ratio = 1

    links = soup.find_all("a")

    internal_links = 0

    domain = urlparse(
        final_url
    ).netloc

    for link in links:

        href = link.get("href", "")

        if not href:
            continue

        full_url = urljoin(
            final_url,
            href
        )

        link_domain = urlparse(
            full_url
        ).netloc

        if link_domain == domain:
            internal_links += 1

    phone_pattern = re.compile(
        r"(?:\+90|0)?\s*5\d{2}\s*\d{3}\s*\d{2}\s*\d{2}"
    )

    phone = bool(
        phone_pattern.search(
            page_text
        )
    )

    email_pattern = re.compile(
        r"[\w\.-]+@[\w\.-]+\.\w+"
    )

    email = bool(
        email_pattern.search(
            page_text
        )
    )

    whatsapp = (
        "wa.me" in html.lower()
        or "whatsapp.com" in html.lower()
    )

    address_patterns = [
        "adres",
        "mah.",
        "mahallesi",
        "sok.",
        "sokak",
        "cad.",
        "caddesi",
        "istanbul",
        "ankara",
        "izmir"
    ]

    address = any(
        word in page_text_lower
        for word in address_patterns
    )

    city_found = bool(
        city
        and city.lower() in page_text_lower
    )

    sector_found = bool(
        sector
        and sector.lower() in page_text_lower
    )

    contact_page = any(
        word in page_text_lower
        for word in [
            "iletişim",
            "iletisim",
            "contact",
            "bize ulaşın",
            "bize ulasin"
        ]
    )

    robots_url = urljoin(
        final_url,
        "/robots.txt"
    )

    sitemap_url = urljoin(
        final_url,
        "/sitemap.xml"
    )

    try:

        robots_response = requests.get(
            robots_url,
            headers=HEADERS,
            timeout=8
        )

        robots = (
            robots_response.status_code == 200
            and len(robots_response.text) > 10
        )

    except Exception:

        robots = False

    try:

        sitemap_response = requests.get(
            sitemap_url,
            headers=HEADERS,
            timeout=8
        )

        sitemap = (
            sitemap_response.status_code == 200
            and len(sitemap_response.text) > 10
        )

    except Exception:

        sitemap = False

    https = final_url.startswith(
        "https://"
    )

    words = re.findall(
        r"\b\w+\b",
        page_text
    )

    word_count = len(words)

    checks = {

        "title": bool(title),

        "title_length": len(title),

        "meta": bool(meta_description),

        "h1": bool(h1),

        "phone": phone,

        "email": email,

        "whatsapp": whatsapp,

        "https": https,

        "robots": robots,

        "sitemap": sitemap,

        "viewport": viewport,

        "canonical": canonical,

        "og": og,

        "schema": schema,

        "images": len(images),

        "images_alt_ratio": images_alt_ratio,

        "internal_links": internal_links,

        "address": address,

        "city": city_found,

        "sector": sector_found,

        "contact_page": contact_page,

        "word_count": word_count
    }

    scores = calculate_scores(
        checks
    )

    recommendations = generate_recommendations(
        checks
    )

    seo_texts = generate_seo_texts(
        business_name,
        sector,
        city
    )

    controls = []

    def add_control(
        name,
        success,
        detail
    ):

        controls.append({
            "name": name,
            "success": success,
            "detail": detail
        })

    add_control(
        "Title",
        bool(title),
        title if title else "Title bulunamadı."
    )

    add_control(
        "Meta description",
        bool(meta_description),
        meta_description
        if meta_description
        else "Meta description bulunamadı."
    )

    add_control(
        "H1",
        bool(h1),
        h1 if h1 else "H1 başlığı bulunamadı."
    )

    add_control(
        "Telefon",
        phone,
        "Telefon bilgisi bulundu."
        if phone
        else "Telefon bilgisi bulunamadı."
    )

    add_control(
        "E-posta",
        email,
        "E-posta bilgisi bulundu."
        if email
        else "E-posta bilgisi bulunamadı."
    )

    add_control(
        "WhatsApp",
        whatsapp,
        "WhatsApp bağlantısı bulundu."
        if whatsapp
        else "WhatsApp bağlantısı bulunamadı."
    )

    add_control(
        "HTTPS",
        https,
        "HTTPS aktif."
        if https
        else "HTTPS aktif değil."
    )

    add_control(
        "robots.txt",
        robots,
        "robots.txt bulundu."
        if robots
        else "robots.txt bulunamadı."
    )

    add_control(
        "sitemap.xml",
        sitemap,
        "sitemap.xml bulundu."
        if sitemap
        else "sitemap.xml bulunamadı."
    )

    add_control(
        "Mobil viewport",
        viewport,
        "Viewport bulundu."
        if viewport
        else "Viewport bulunamadı."
    )

    add_control(
        "Canonical",
        canonical,
        "Canonical bulundu."
        if canonical
        else "Canonical bulunamadı."
    )

    add_control(
        "Schema",
        schema,
        "Yapılandırılmış veri bulundu."
        if schema
        else "Yapılandırılmış veri bulunamadı."
    )

    add_control(
        "Şehir",
        city_found,
        f"{city} bilgisi bulundu."
        if city_found
        else "Şehir bilgisi bulunamadı."
    )

    add_control(
        "Sektör",
        sector_found,
        f"{sector} bilgisi bulundu."
        if sector_found
        else "Sektör bilgisi bulunamadı."
    )

    add_control(
        "Adres",
        address,
        "Adres sinyali bulundu."
        if address
        else "Adres bilgisi bulunamadı."
    )

    add_control(
        "İçerik",
        word_count >= 300,
        f"{word_count} kelime analiz edildi."
    )

    score = scores["total"]

    return {

        "success": True,

        "business_name": business_name,

        "sector": sector,

        "city": city,

        "website": website,

        "final_url": final_url,

        "status_code": response.status_code,

        "page_size": len(html),

        "title": title,

        "h1": h1,

        "meta_description": meta_description,

        "scores": scores,

        "score": score,

        "status": status_from_score(
            score
        ),

        "checks": checks,

        "controls": controls,

        "recommendations": recommendations,

        "seo_texts": seo_texts,

        "report_date": datetime.now().strftime(
            "%d.%m.%Y %H:%M"
        )
    }