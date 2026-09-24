import requests

username = input("GitHub kullanıcı adı: ")

url = f"https://api.github.com/users/{username}"
response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    print("\n===== GITHUB RAPORU =====")
    print("Kullanıcı:", data["login"])
    print("Takipçi:", data["followers"])
    print("Takip edilen:", data["following"])
    print("Public repo:", data["public_repos"])
    print("Profil:", data["html_url"])

    repos_url = f"https://api.github.com/users/{username}/repos"
    repos_response = requests.get(repos_url)

    if repos_response.status_code == 200:

        repos = repos_response.json()

        print("\n===== REPOLAR =====")

        for repo in repos:
            print(
                "-", repo["name"],
                "| ⭐", repo["stargazers_count"],
                "| Fork:", repo["forks_count"]
            )

else:
    print("Kullanıcı bulunamadı.")