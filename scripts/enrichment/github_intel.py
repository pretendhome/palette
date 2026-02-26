"""GitHub intelligence module — fetches profile, repos, activity, and orgs."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta

import httpx

from .config import GITHUB_API_BASE, GITHUB_REPOS_LIMIT, github_token


@dataclass
class RepoInfo:
    name: str
    description: str | None
    stars: int
    forks: int
    language: str | None
    last_push: str  # ISO date


@dataclass
class GitHubProfile:
    username: str
    bio: str | None = None
    company: str | None = None
    location: str | None = None
    blog: str | None = None
    public_repos: int = 0
    followers: int = 0
    top_repos: list[RepoInfo] = field(default_factory=list)
    recent_commits_30d: int = 0
    organizations: list[str] = field(default_factory=list)
    fetched_at: str = ""
    api_calls: int = 0
    error: str | None = None


def _headers() -> dict[str, str]:
    h: dict[str, str] = {"Accept": "application/vnd.github.v3+json"}
    token = github_token()
    if token and token.startswith(("ghp_", "gho_", "ghu_", "ghs_", "ghr_", "github_pat_")):
        h["Authorization"] = f"Bearer {token}"
    return h


def _get(client: httpx.Client, path: str) -> httpx.Response | None:
    """GET with single retry on network error.  Returns None on 404."""
    url = f"{GITHUB_API_BASE}{path}"
    for attempt in range(2):
        try:
            resp = client.get(url)
            if resp.status_code == 404:
                return None
            if resp.status_code in (401, 403):
                remaining = resp.headers.get("x-ratelimit-remaining", "?")
                raise RuntimeError(
                    f"GitHub API {resp.status_code} (remaining={remaining}). "
                    "Check GITHUB_TOKEN validity or rate limits."
                )
            resp.raise_for_status()
            return resp
        except httpx.HTTPStatusError:
            raise
        except (httpx.ConnectError, httpx.ReadTimeout) as exc:
            if attempt == 0:
                continue
            raise RuntimeError(f"GitHub network error after retry: {exc}") from exc


def fetch_github_profile(username: str) -> GitHubProfile:
    """Fetch GitHub data for a single user.  Returns a GitHubProfile."""
    result = GitHubProfile(
        username=username,
        fetched_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    calls = 0

    with httpx.Client(headers=_headers(), timeout=15.0) as client:
        # 1. User profile
        resp = _get(client, f"/users/{username}")
        calls += 1
        if resp is None:
            result.error = f"User {username} not found (404)"
            result.api_calls = calls
            return result

        user = resp.json()
        result.bio = user.get("bio")
        result.company = user.get("company")
        result.location = user.get("location")
        result.blog = user.get("blog") or None
        result.public_repos = user.get("public_repos", 0)
        result.followers = user.get("followers", 0)

        # 2. Top repos by stars
        resp = _get(
            client,
            f"/users/{username}/repos?type=owner&sort=stars&direction=desc"
            f"&per_page={GITHUB_REPOS_LIMIT}",
        )
        calls += 1
        if resp is not None:
            for repo in resp.json()[:GITHUB_REPOS_LIMIT]:
                result.top_repos.append(
                    RepoInfo(
                        name=repo["name"],
                        description=repo.get("description"),
                        stars=repo.get("stargazers_count", 0),
                        forks=repo.get("forks_count", 0),
                        language=repo.get("language"),
                        last_push=repo.get("pushed_at", ""),
                    )
                )

        # 3. Recent public events → estimate commits in last 30 days
        resp = _get(client, f"/users/{username}/events/public?per_page=100")
        calls += 1
        if resp is not None:
            cutoff = datetime.now(timezone.utc) - timedelta(days=30)
            commits = 0
            for event in resp.json():
                if event.get("type") != "PushEvent":
                    continue
                created = event.get("created_at", "")
                try:
                    ts = datetime.fromisoformat(created.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    continue
                if ts < cutoff:
                    break
                commits += event.get("payload", {}).get("size", 0)
            result.recent_commits_30d = commits

        # 4. Public org memberships
        resp = _get(client, f"/users/{username}/orgs?per_page=20")
        calls += 1
        if resp is not None:
            result.organizations = [
                org.get("login", "") for org in resp.json() if org.get("login")
            ]

    result.api_calls = calls
    return result


def profile_to_yaml_dict(profile: GitHubProfile) -> dict:
    """Convert a GitHubProfile to a dict suitable for embedding in people_library YAML."""
    top_repos = []
    for r in profile.top_repos:
        entry: dict = {"name": r.name, "stars": r.stars}
        if r.description:
            entry["description"] = r.description
        if r.language:
            entry["language"] = r.language
        if r.forks:
            entry["forks"] = r.forks
        if r.last_push:
            entry["last_push"] = r.last_push
        top_repos.append(entry)

    data: dict = {
        "username": profile.username,
        "followers": profile.followers,
        "public_repos": profile.public_repos,
    }
    if profile.bio:
        data["bio"] = profile.bio
    if profile.company:
        data["company"] = profile.company
    if profile.blog:
        data["blog"] = profile.blog
    if top_repos:
        data["top_repos"] = top_repos
    if profile.recent_commits_30d:
        data["recent_commits_30d"] = profile.recent_commits_30d
    if profile.organizations:
        data["organizations"] = profile.organizations
    data["fetched_at"] = profile.fetched_at
    return data
