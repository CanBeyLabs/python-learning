import requests


username = input("GitHub kullanıcı adı: ")

user_url = f"https://api.github.com/users/{username}"
response = requests.get(user_url)


if response.status_code == 200:

    data = response.json()

    print("\n===== GITHUB RAPORU =====")
    print("Kullanıcı:", data["login"])
    print("Takipçi:", data["followers"])
    print("Takip edilen:", data["following"])
    print("Public repo:", data["public_repos"])
    print("Profil:", data["html_url"])

    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos_response = requests.get(repos_url)

    if repos_response.status_code == 200:

        repos = repos_response.json()

        print("\n===== REPOLAR =====")

        toplam_yildiz = 0
        toplam_fork = 0

        for repo in repos:

            print(
                "-",
                repo["name"],
                "| ⭐",
                repo["stargazers_count"],
                "| Fork:",
                repo["forks_count"]
            )

            toplam_yildiz += repo["stargazers_count"]
            toplam_fork += repo["forks_count"]

        print("\n===== TOPLAM =====")
        print("Toplam yıldız:", toplam_yildiz)
        print("Toplam fork:", toplam_fork)

    else:
        print("Repolar alınamadı.")

else:
    print("Kullanıcı bulunamadı.")