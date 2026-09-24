import requests


def github_kullanici_getir(kullanici):
    url = f"https://api.github.com/users/{kullanici}"

    try:
        cevap = requests.get(url, timeout=10)

        if cevap.status_code == 200:
            return cevap.json()

        elif cevap.status_code == 404:
            return None

        else:
            print("API hata kodu:", cevap.status_code)
            return None

    except requests.exceptions.RequestException:
        print("Bağlantı hatası.")
        return None