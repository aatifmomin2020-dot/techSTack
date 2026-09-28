import base64
import logging
from typing import Dict, Any, List, Optional
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

class GithubServiceError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class GithubService:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.GITHUB_TOKEN
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Developer-Tech-Stack-Predictor/1.0"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    async def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """
        Fetches GitHub user profile, repositories, topics, and README files.
        """
        clean_username = username.strip()
        if not clean_username:
            raise GithubServiceError("GitHub username cannot be empty", status_code=400)

        async with httpx.AsyncClient(headers=self.headers, timeout=12.0) as client:
            # 1. Fetch user profile
            user_url = f"{self.BASE_URL}/users/{clean_username}"
            user_resp = await client.get(user_url)

            if user_resp.status_code == 404:
                raise GithubServiceError(f"GitHub user '{clean_username}' not found", status_code=404)
            elif user_resp.status_code == 403 and "rate limit" in user_resp.text.lower():
                raise GithubServiceError("GitHub API rate limit exceeded. Please try manual profile entry or configure a GITHUB_TOKEN.", status_code=429)
            elif user_resp.status_code != 200:
                raise GithubServiceError(f"GitHub API error ({user_resp.status_code}): {user_resp.text}", status_code=user_resp.status_code)

            profile_data = user_resp.json()

            # 2. Fetch public repositories (up to 30 most recently updated)
            repos_url = f"{self.BASE_URL}/users/{clean_username}/repos?sort=updated&per_page=30"
            repos_resp = await client.get(repos_url)

            repositories = []
            languages_aggregated: Dict[str, int] = {}
            topics_aggregated: List[str] = []

            if repos_resp.status_code == 200:
                raw_repos = repos_resp.json()
                for r in raw_repos:
                    if r.get("fork"):
                        continue  # Focus on original repositories

                    repo_name = r.get("name")
                    primary_lang = r.get("language")
                    stars = r.get("stargazers_count", 0)
                    forks = r.get("forks_count", 0)
                    desc = r.get("description") or ""
                    topics = r.get("topics", [])
                    created_at = r.get("created_at")
                    updated_at = r.get("updated_at")
                    repo_url = r.get("html_url")

                    if primary_lang:
                        languages_aggregated[primary_lang] = languages_aggregated.get(primary_lang, 0) + 1

                    for t in topics:
                        if t not in topics_aggregated:
                            topics_aggregated.append(t)

                    # Fetch README for top repositories (first 5 to avoid excessive requests)
                    readme_content = ""
                    if len(repositories) < 5:
                        readme_content = await self._fetch_repo_readme(client, clean_username, repo_name)

                    repositories.append({
                        "name": repo_name,
                        "description": desc,
                        "primary_language": primary_lang,
                        "stars": stars,
                        "forks": forks,
                        "topics": topics,
                        "readme_content": readme_content,
                        "created_at": created_at,
                        "updated_at": updated_at,
                        "repo_url": repo_url
                    })

            return {
                "username": profile_data.get("login"),
                "name": profile_data.get("name") or profile_data.get("login"),
                "bio": profile_data.get("bio") or "",
                "location": profile_data.get("location") or "",
                "public_repos": profile_data.get("public_repos", 0),
                "followers": profile_data.get("followers", 0),
                "avatar_url": profile_data.get("avatar_url"),
                "repositories": repositories,
                "languages_summary": languages_aggregated,
                "topics_summary": topics_aggregated
            }

    async def _fetch_repo_readme(self, client: httpx.AsyncClient, username: str, repo_name: str) -> str:
        try:
            readme_url = f"{self.BASE_URL}/repos/{username}/{repo_name}/readme"
            resp = await client.get(readme_url)
            if resp.status_code == 200:
                content_b64 = resp.json().get("content", "")
                if content_b64:
                    decoded = base64.b64decode(content_b64).decode("utf-8", errors="ignore")
                    # Limit length to 3000 chars for processing
                    return decoded[:3000]
        except Exception as e:
            logger.debug(f"Could not fetch README for {username}/{repo_name}: {e}")
        return ""
