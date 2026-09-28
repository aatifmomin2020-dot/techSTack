from fastapi import APIRouter, HTTPException, status
from app.services.github_service import GithubService, GithubServiceError

router = APIRouter(prefix="/api/github", tags=["GitHub Integration"])

@router.get("/{username}")
async def get_github_profile(username: str):
    """
    Fetches real GitHub user profile, repositories, primary languages, topics, and README samples.
    """
    service = GithubService()
    try:
        data = await service.fetch_user_data(username)
        return data
    except GithubServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected GitHub API error: {str(e)}")
