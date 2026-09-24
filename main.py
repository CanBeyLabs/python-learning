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
        print("İnternet bağlantısında sorun oluştu.")
        return None


def bilgileri_goster(veri):
    print("\n--- GITHUB BİLGİLERİ ---")
    print("Kullanıcı:", veri["login"])
    print("Profil:", veri["html_url"])
    print("Takipçi:", veri["followers"])
    print("Takip edilen:", veri["following"])
    print("Public repo:", veri["public_repos"])


kullanici = input("GitHub kullanıcı adı: ")

veri = github_kullanici_getir(kullanici)

if veri is not None:
    bilgileri_goster(veri)
else:
    print("Kullanıcı bulunamadı.")