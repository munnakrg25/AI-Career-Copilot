import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"


def _github_headers() -> dict:
    """Return headers for GitHub API requests, including auth token if available."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _check_rate_limit(response: httpx.Response) -> None:
    """
    Raise a clear ValueError if the response indicates a GitHub rate limit.
    Handles HTTP 403 (primary rate limit) and HTTP 429 (secondary rate limit).
    """
    if response.status_code in (403, 429):
        try:
            body = response.json()
            message = body.get("message", "")
        except Exception:
            message = ""

        if response.status_code == 429 or "rate limit" in message.lower():
            reset_ts = response.headers.get("X-RateLimit-Reset")
            if reset_ts:
                import datetime
                reset_dt = datetime.datetime.fromtimestamp(
                    int(reset_ts), tz=datetime.timezone.utc
                )
                reset_str = reset_dt.strftime("%H:%M UTC")
                raise ValueError(
                    f"GitHub API rate limit exceeded. Limit resets at {reset_str}. "
                    "Add a GITHUB_TOKEN to your .env to increase the limit."
                )
            raise ValueError(
                "GitHub API rate limit exceeded. "
                "Add a GITHUB_TOKEN to your .env to increase the limit."
            )


async def analyze_github(username: str):
    url = f"{GITHUB_API}/users/{username}/repos"

    async with httpx.AsyncClient(headers=_github_headers()) as client:
        response = await client.get(
            url,
            params={
                "sort": "updated",
                "per_page": 100
            }
        )

    _check_rate_limit(response)

    if response.status_code == 404:
        raise ValueError("GitHub user not found")

    if response.status_code != 200:
        raise ValueError("Unable to fetch GitHub data")

    repositories = response.json()

    total_repositories = len(repositories)

    languages = {}
    total_stars = 0
    total_forks = 0
    projects = []

    for repo in repositories:
        if repo.get("fork"):
            continue

        language = repo.get("language")

        if language:
            languages[language] = languages.get(language, 0) + 1

        total_stars += repo.get("stargazers_count", 0)
        total_forks += repo.get("forks_count", 0)

        projects.append({
            "name": repo.get("name"),
            "language": language,
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "description": repo.get("description")
        })

    project_score = min(total_repositories * 5, 40)
    star_score = min(total_stars * 2, 20)
    language_score = min(len(languages) * 5, 20)

    profile_score = min(
        project_score + star_score + language_score,
        100
    )

    strengths = []
    improvements = []

    if total_repositories >= 5:
        strengths.append("Good number of public repositories")
    else:
        improvements.append("Create more public projects")

    if len(languages) >= 2:
        strengths.append("Good programming language diversity")
    else:
        improvements.append("Work with more technologies")

    if total_stars > 0:
        strengths.append("Has community engagement through repository stars")
    else:
        improvements.append("Improve project visibility and documentation")

    return {
        "username": username,
        "profile_score": profile_score,
        "total_repositories": total_repositories,
        "languages": languages,
        "total_stars": total_stars,
        "total_forks": total_forks,
        "projects": projects,
        "strengths": strengths,
        "improvements": improvements
    }
