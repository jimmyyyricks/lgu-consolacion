from datetime import datetime

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.database import get_db
from app.core.framework.models.auth import User
from app.core.framework.models.public_content import PublicContent
from app.core.security import CurrentUser, get_current_user_from_token
from app.main import fastapi_app


@pytest_asyncio.fixture
async def content_client():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(User.__table__.create)
        await connection.run_sync(PublicContent.__table__.create)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        session.add(
            User(
                id="editor-1",
                username="editor",
                email="editor@example.com",
                full_name="Content Editor",
                hashed_password="not-used",
                is_active=True,
            )
        )
        await session.commit()

    async def override_get_db():
        async with session_factory() as session:
            yield session

    previous_overrides = fastapi_app.dependency_overrides.copy()
    fastapi_app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
    fastapi_app.dependency_overrides.clear()
    fastapi_app.dependency_overrides.update(previous_overrides)
    await engine.dispose()


@pytest.mark.asyncio
async def test_public_content_requires_staff_authentication(content_client):
    response = await content_client.post(
        "/api/content",
        json={
            "slug": "test-ordinance",
            "kind": "ordinance",
            "title": "Test ordinance",
            "summary": "Test summary",
            "status": "draft",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_public_content_denies_non_editor_users(content_client):
    async def viewer_user():
        return CurrentUser(id="viewer-1", username="viewer", roles=["Viewer"])

    fastapi_app.dependency_overrides[get_current_user_from_token] = viewer_user
    response = await content_client.post(
        "/api/content",
        json={
            "slug": "viewer-ordinance",
            "kind": "ordinance",
            "title": "Viewer ordinance",
            "summary": "This user cannot publish.",
        },
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_public_content_hides_drafts_and_lists_published(content_client):
    async def editor_user():
        return CurrentUser(
            id="editor-1",
            username="editor",
            roles=["Content Editor"],
        )

    fastapi_app.dependency_overrides[get_current_user_from_token] = editor_user
    shared_fields = {
        "kind": "ordinance",
        "title": "Approved test ordinance",
    }
    published = await content_client.post(
        "/api/content",
        json={
            **shared_fields,
            "slug": "published-ordinance",
            "status": "published",
            "drive_url": "https://drive.google.com/file/d/PublicFile_123/view",
        },
    )
    draft = await content_client.post(
        "/api/content",
        json={**shared_fields, "slug": "draft-ordinance", "status": "draft"},
    )

    assert published.status_code == 201
    assert published.json()["summary"] == ""
    assert draft.status_code == 201
    assert published.json()["drive_file_id"] == "PublicFile_123"
    assert "drive_url" not in published.json()

    fastapi_app.dependency_overrides.pop(get_current_user_from_token)
    visible = await content_client.get(
        "/api/content", params={"kind": "ordinance"}
    )
    hidden = await content_client.get("/api/content/draft-ordinance")
    visible_slugs = {record["slug"] for record in visible.json()}

    assert visible.status_code == 200
    assert "published-ordinance" in visible_slugs
    assert "draft-ordinance" not in visible_slugs
    assert hidden.status_code == 404


@pytest.mark.asyncio
async def test_non_document_content_requires_a_summary(content_client):
    async def editor_user():
        return CurrentUser(
            id="editor-1",
            username="editor",
            roles=["Content Editor"],
        )

    fastapi_app.dependency_overrides[get_current_user_from_token] = editor_user
    response = await content_client.post(
        "/api/content",
        json={
            "slug": "news-without-summary",
            "kind": "news",
            "title": "News without summary",
            "status": "draft",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_public_content_saves_featured_news_and_image(content_client):
    async def editor_user():
        return CurrentUser(
            id="editor-1",
            username="editor",
            roles=["Content Editor"],
        )

    fastapi_app.dependency_overrides[get_current_user_from_token] = editor_user
    response = await content_client.post(
        "/api/content",
        json={
            "slug": "featured-news",
            "kind": "news",
            "title": "Featured news",
            "summary": "A test sample.",
            "image_url": "/images/featured-news.jpg",
            "featured": True,
            "status": "published",
        },
    )

    assert response.status_code == 201
    assert response.json()["featured"] is True
    assert response.json()["image_url"] == "/images/featured-news.jpg"


@pytest.mark.asyncio
async def test_public_content_can_list_public_records_without_news_or_tourism(
    content_client,
):
    async def editor_user():
        return CurrentUser(
            id="editor-1",
            username="editor",
            roles=["Content Editor"],
        )

    fastapi_app.dependency_overrides[get_current_user_from_token] = editor_user
    for kind, slug in (
        ("ordinance", "records-only-ordinance"),
        ("government_action", "records-only-notice"),
        ("news", "records-only-news"),
        ("tourism", "records-only-tourism"),
    ):
        response = await content_client.post(
            "/api/content",
            json={
                "slug": slug,
                "kind": kind,
                "title": slug,
                "summary": "Published content for the records filter.",
                "status": "published",
                **(
                    {"drive_url": "https://drive.google.com/file/d/PublicFile_123/view"}
                    if kind == "ordinance"
                    else {}
                ),
            },
        )
        assert response.status_code == 201

    fastapi_app.dependency_overrides.pop(get_current_user_from_token)
    response = await content_client.get(
        "/api/content", params={"records_only": True}
    )

    assert response.status_code == 200
    records = response.json()
    assert {item["kind"] for item in records} == {
        "ordinance",
        "government_action",
    }
    assert [item["slug"] for item in records] == [
        "records-only-notice",
        "records-only-ordinance",
    ]


@pytest.mark.asyncio
async def test_public_content_archive_filters_and_paginates_by_publication_year(
    content_client,
):
    async def editor_user():
        return CurrentUser(
            id="editor-1",
            username="editor",
            roles=["Content Editor"],
        )

    fastapi_app.dependency_overrides[get_current_user_from_token] = editor_user
    for slug, title, record_date in (
        ("archive-needle-one", "Needle archive one", "2020-01-02"),
        ("archive-needle-two", "Needle archive two", "2021-02-03"),
        ("archive-other", "Other archive record", "2022-03-04"),
    ):
        response = await content_client.post(
            "/api/content",
            json={
                "slug": slug,
                "kind": "government_action",
                "title": title,
                "summary": "Published archive test record.",
                "record_date": record_date,
                "status": "published",
            },
        )
        assert response.status_code == 201

    fastapi_app.dependency_overrides.pop(get_current_user_from_token)
    current_year = datetime.utcnow().year
    first_page = await content_client.get(
        "/api/content/archive",
        params={
            "kind": "government_action",
            "records_only": True,
            "year": current_year,
            "limit": 1,
        },
    )
    second_page = await content_client.get(
        "/api/content/archive",
        params={
            "kind": "government_action",
            "records_only": True,
            "year": current_year,
            "limit": 1,
            "offset": 1,
        },
    )
    searched = await content_client.get(
        "/api/content/archive",
        params={
            "kind": "government_action",
            "search": "Needle",
            "year": current_year,
            "records_only": True,
        },
    )
    record_date_year = await content_client.get(
        "/api/content/archive",
        params={
            "kind": "government_action",
            "year": 2020,
            "records_only": True,
        },
    )

    assert first_page.status_code == 200
    assert first_page.json()["total"] == 3
    assert len(first_page.json()["items"]) == 1
    assert first_page.json()["years"] == [current_year]
    assert second_page.status_code == 200
    assert second_page.json()["items"][0]["id"] != first_page.json()["items"][0]["id"]
    assert searched.json()["total"] == 2
    assert {item["slug"] for item in searched.json()["items"]} == {
        "archive-needle-one",
        "archive-needle-two",
    }
    assert record_date_year.json()["total"] == 0
