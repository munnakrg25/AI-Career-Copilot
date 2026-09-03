import httpx
from services.github_analyzer import _github_headers, _check_rate_limit


GITHUB_API = "https://api.github.com"


async def get_repository_analysis(username: str, repo_name: str):
    async with httpx.AsyncClient(headers=_github_headers()) as client:

        repo_response = await client.get(
            f"{GITHUB_API}/repos/{username}/{repo_name}"
        )

        _check_rate_limit(repo_response)

        if repo_response.status_code == 404:
            raise ValueError("Repository not found")

        if repo_response.status_code != 200:
            raise ValueError("Unable to fetch repository")

        repo = repo_response.json()

        contents_response = await client.get(
            f"{GITHUB_API}/repos/{username}/{repo_name}/contents"
        )

        _check_rate_limit(contents_response)

        if contents_response.status_code != 200:
            raise ValueError("Unable to fetch repository files")

        contents = contents_response.json()

    files = []

    if isinstance(contents, list):
        files = [
            item["name"]
            for item in contents
            if item.get("type") == "file"
        ]

    file_names = {file.lower() for file in files}

    has_readme = any(
        file.startswith("readme")
        for file in file_names
    )

    has_requirements = (
        "requirements.txt" in file_names
        or "pyproject.toml" in file_names
    )

    has_package_json = "package.json" in file_names

    has_docker = any(
        file in file_names
        for file in [
            "dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml"
        ]
    )

    has_tests = any(
        "test" in file
        for file in file_names
    )

    quality_score = 0

    if has_readme:
        quality_score += 20

    if has_requirements or has_package_json:
        quality_score += 20

    if has_tests:
        quality_score += 20

    if has_docker:
        quality_score += 20

    if repo.get("description"):
        quality_score += 10

    if repo.get("stargazers_count", 0) > 0:
        quality_score += 10

    recommendations = []

    if not has_readme:
        recommendations.append(
            "Add a detailed README"
        )

    if not has_requirements and not has_package_json:
        recommendations.append(
            "Add dependency management files"
        )

    if not has_tests:
        recommendations.append(
            "Add unit or integration tests"
        )

    if not has_docker:
        recommendations.append(
            "Add Docker support"
        )

    if not repo.get("description"):
        recommendations.append(
            "Add a repository description"
        )

    return {
        "repository": repo_name,
        "full_name": repo.get("full_name"),
        "description": repo.get("description"),
        "language": repo.get("language"),
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "has_readme": has_readme,
        "has_requirements": has_requirements,
        "has_package_json": has_package_json,
        "has_tests": has_tests,
        "has_docker": has_docker,
        "quality_score": quality_score,
        "files": files,
        "recommendations": recommendations
    }
