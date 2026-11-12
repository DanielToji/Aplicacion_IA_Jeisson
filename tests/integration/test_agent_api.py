import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


async def _client() -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    )


@pytest.mark.asyncio
async def test_estimate_ok() -> None:
    async with await _client() as client:
        r = await client.post(
            "/api/v1/agent/estimate-learning-effort",
            json={
                "activity": "Curso de FastAPI",
                "difficulty": "media",
                "topics_count": 10,
                "weekly_hours_available": 10.0,
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["total_hours"] == 22.5
    assert body["estimated_days"] == 16
    assert body["difficulty"] == "media"


@pytest.mark.asyncio
async def test_estimate_rejects_zero_topics() -> None:
    async with await _client() as client:
        r = await client.post(
            "/api/v1/agent/estimate-learning-effort",
            json={
                "activity": "Curso",
                "difficulty": "media",
                "topics_count": 0,
                "weekly_hours_available": 10.0,
            },
        )
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_estimate_rejects_unknown_difficulty() -> None:
    async with await _client() as client:
        r = await client.post(
            "/api/v1/agent/estimate-learning-effort",
            json={
                "activity": "Curso",
                "difficulty": "extrema",
                "topics_count": 5,
                "weekly_hours_available": 10.0,
            },
        )
    assert r.status_code == 422