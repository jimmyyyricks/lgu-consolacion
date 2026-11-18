from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.public_content import (
    ContentKind,
    DOCUMENT_KINDS,
    PublicContentArchivePage,
    PublicContentInput,
    PublicContentOutput,
    PublicContentUpdate,
)
from app.core.database import get_db
from app.core.security import CurrentUser, get_current_user_from_token
from app.core.framework.models.public_content import PublicContent
from app.infrastructure.database.repositories.public_content_repository import (
    PublicContentRepository,
)

router = APIRouter(prefix="/content", tags=["Public Content"])
EDITOR_ROLES = {"admin", "administrator", "content_editor", "editor"}


def get_content_repository(
    db: AsyncSession = Depends(get_db),
) -> PublicContentRepository:
    return PublicContentRepository(db)


async def require_content_editor(
    user: CurrentUser = Depends(get_current_user_from_token),
) -> CurrentUser:
    if user.id == "anonymous":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    normalized_roles = {
        role.casefold().replace(" ", "_") for role in user.roles
    }
    if not user.is_superuser and not EDITOR_ROLES.intersection(normalized_roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user


def output(content: PublicContent) -> PublicContentOutput:
    result = PublicContentOutput.model_validate(content)
    return result.model_copy(
        update={
            "drive_file_id": content.drive_file_id,
        }
    )


@router.get("", response_model=list[PublicContentOutput])
async def list_public_content(
    repository: Annotated[PublicContentRepository, Depends(get_content_repository)],
    kind: ContentKind | None = None,
    search: str | None = Query(default=None, max_length=200),
    year: int | None = Query(default=None, ge=1900, le=2200),
    records_only: bool = False,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items = await repository.list(
        kind=kind,
        search=search,
        year=year,
        records_only=records_only,
        limit=limit,
        offset=offset,
    )
    return [output(item) for item in items]


@router.get("/archive", response_model=PublicContentArchivePage)
async def list_public_content_archive(
    repository: Annotated[PublicContentRepository, Depends(get_content_repository)],
    kind: ContentKind,
    search: str | None = Query(default=None, max_length=200),
    year: int | None = Query(default=None, ge=1900, le=2200),
    records_only: bool = False,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items = await repository.list_archive_page(
        kind=kind,
        search=search,
        year=year,
        records_only=records_only,
        limit=limit,
        offset=offset,
    )
    total = await repository.count_archive_records(
        kind=kind,
        search=search,
        year=year,
        records_only=records_only,
    )
    years = await repository.archive_publication_years(
        kind=kind,
        records_only=records_only,
    )
    return {
        "items": [output(item) for item in items],
        "total": total,
        "years": years,
    }


@router.get("/{slug}", response_model=PublicContentOutput)
async def get_public_content(
    slug: str,
    repository: Annotated[PublicContentRepository, Depends(get_content_repository)],
):
    content = await repository.get_by_slug(slug)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return output(content)


@router.get("/admin/all", response_model=list[PublicContentOutput])
async def list_all_content(
    repository: Annotated[PublicContentRepository, Depends(get_content_repository)],
    _user: Annotated[CurrentUser, Depends(require_content_editor)],
    kind: ContentKind | None = None,
    limit: int = Query(default=100, ge=1, le=200),
):
    items = await repository.list(kind=kind, include_drafts=True, limit=limit)
    return [output(item) for item in items]


@router.post("", response_model=PublicContentOutput, status_code=status.HTTP_201_CREATED)
async def create_content(
    payload: PublicContentInput,
    repository: Annotated[PublicContentRepository, Depends(get_content_repository)],
    user: Annotated[CurrentUser, Depends(require_content_editor)],
):
    content = PublicContent(
        **payload.model_dump(exclude={"drive_url"}),
        drive_file_id=payload.drive_url,
        created_by_id=user.id,
        published_at=datetime.utcnow() if payload.status == "published" else None,
    )
    try:
        return output(await repository.save(content))
    except IntegrityError as exc:
        await repository.db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A content item with this slug already exists",
        ) from exc


@router.patch("/{slug}", response_model=PublicContentOutput)
async def update_content(
    slug: str,
    payload: PublicContentUpdate,
    repository: Annotated[PublicContentRepository, Depends(get_content_repository)],
    _user: Annotated[CurrentUser, Depends(require_content_editor)],
):
    content = await repository.get_by_slug(slug, include_drafts=True)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("featured") and content.kind != "news":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only news and events can be featured",
        )
    if "drive_url" in changes:
        content.drive_file_id = changes.pop("drive_url")
    for field, value in changes.items():
        setattr(content, field, value)
    if content.status == "published":
        if content.kind in DOCUMENT_KINDS and not content.drive_file_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A public Drive PDF is required to publish this document",
            )
        content.published_at = content.published_at or datetime.utcnow()
    elif content.status == "draft":
        content.published_at = None
    try:
        return output(await repository.save(content))
    except IntegrityError as exc:
        await repository.db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Content could not be saved",
        ) from exc
