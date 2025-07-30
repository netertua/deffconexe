import requests
from bs4 import BeautifulSoup

class InternetScraper:
    def __init__(self, base_url="https://github.com"):
        self.base_url = base_url

    def fetch_repo_readme(self, user, repo):
        url = f"{self.base_url}/{user}/{repo}/blob/main/README.md"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        # Github HTML'den markdown text'i çıkarmak zor,
        # basitçe içerik etiketini döndürelim (Gelişmiş için GitHub API kullanılmalı)
        content = soup.find("article")
        if not content:
            return None
        return content.get_text(separator="\n").strip()

    def search_github_repos(self, query):
        search_url = f"{self.base_url}/search?q={query}"
        response = requests.get(search_url)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for item in soup.select("ul.repo-list li"):
            title = item.find("a", class_="v-align-middle")
            desc = item.find("p", class_="mb-1")
            if title:
                results.append({
                    "name": title.text.strip(),
                    "url": self.base_url + title['href'],
                    "description": desc.text.strip() if desc else ""
                })
        return results

if __name__ == "__main__":
    scraper = InternetScraper()
    repos = scraper.search_github_repos("pyqt")
    for r in repos[:5]:
        print(f"{r['name']}: {r['url']}\n{r['description']}\n")

    readme = scraper.fetch_repo_readme("pyside", "pyside-setup")
    if readme:
        print("\nREADME Content Preview:\n", readme[:500])
    else:
        print("README alınamadı.")
