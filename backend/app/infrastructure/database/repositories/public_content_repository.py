from datetime import datetime

from sqlalchemy import extract, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.framework.models.public_content import PublicContent


class PublicContentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _archive_conditions(
        self,
        *,
        kind: str,
        search: str | None,
        year: int | None,
        records_only: bool,
    ):
        conditions = [PublicContent.status == "published", PublicContent.kind == kind]
        if records_only:
            conditions.append(PublicContent.kind.not_in(("news", "tourism")))
        if search and (term := search.strip()):
            pattern = f"%{term}%"
            conditions.append(
                or_(
                    PublicContent.title.ilike(pattern),
                    PublicContent.document_number.ilike(pattern),
                    PublicContent.summary.ilike(pattern),
                    PublicContent.category.ilike(pattern),
                )
            )
        if year:
            conditions.extend(
                (
                    PublicContent.published_at >= datetime(year, 1, 1),
                    PublicContent.published_at < datetime(year + 1, 1, 1),
                )
            )
        return conditions

    async def list_archive_page(
        self,
        *,
        kind: str,
        search: str | None,
        year: int | None,
        records_only: bool,
        limit: int,
        offset: int,
    ) -> list[PublicContent]:
        conditions = self._archive_conditions(
            kind=kind,
            search=search,
            year=year,
            records_only=records_only,
        )
        ordering = (
            func.coalesce(
                PublicContent.published_at,
                PublicContent.created_at,
            ).desc(),
            PublicContent.created_at.desc(),
        )
        result = await self.db.execute(
            select(PublicContent)
            .where(*conditions)
            .order_by(*ordering)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def count_archive_records(
        self,
        *,
        kind: str,
        search: str | None,
        year: int | None,
        records_only: bool,
    ) -> int:
        conditions = self._archive_conditions(
            kind=kind,
            search=search,
            year=year,
            records_only=records_only,
        )
        result = await self.db.execute(
            select(func.count()).select_from(PublicContent).where(*conditions)
        )
        return result.scalar_one()

    async def archive_publication_years(
        self,
        *,
        kind: str,
        records_only: bool,
    ) -> list[int]:
        conditions = self._archive_conditions(
            kind=kind,
            search=None,
            year=None,
            records_only=records_only,
        )
        year = extract("year", PublicContent.published_at)
        result = await self.db.execute(
            select(year)
            .where(*conditions, PublicContent.published_at.is_not(None))
            .distinct()
            .order_by(year.desc())
        )
        return [int(value) for value in result.scalars().all()]

    async def list(
        self,
        *,
        kind: str | None = None,
        search: str | None = None,
        year: int | None = None,
        records_only: bool = False,
        include_drafts: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[PublicContent]:
        query = select(PublicContent)
        if not include_drafts:
            query = query.where(PublicContent.status == "published")
        if kind:
            query = query.where(PublicContent.kind == kind)
        if records_only:
            query = query.where(PublicContent.kind.not_in(("news", "tourism")))
        if search:
            term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    PublicContent.title.ilike(term),
                    PublicContent.document_number.ilike(term),
                    PublicContent.summary.ilike(term),
                    PublicContent.category.ilike(term),
                )
            )
        if year:
            query = query.where(
                PublicContent.record_date >= datetime(year, 1, 1).date(),
                PublicContent.record_date < datetime(year + 1, 1, 1).date(),
            )
        ordering = (
            (
                func.coalesce(
                    PublicContent.published_at,
                    PublicContent.created_at,
                ).desc(),
                PublicContent.created_at.desc(),
            )
            if records_only
            else (
                PublicContent.featured.desc(),
                PublicContent.published_at.desc(),
                PublicContent.record_date.desc(),
                PublicContent.created_at.desc(),
            )
        )
        return list(
            (
                await self.db.execute(
                    query.order_by(*ordering)
                    .limit(limit)
                    .offset(offset)
                )
            )
            .scalars()
            .all()
        )

    async def get_by_slug(
        self, slug: str, *, include_drafts: bool = False
    ) -> PublicContent | None:
        query = select(PublicContent).where(PublicContent.slug == slug)
        if not include_drafts:
            query = query.where(PublicContent.status == "published")
        return (await self.db.execute(query)).scalar_one_or_none()

    async def save(self, content: PublicContent) -> PublicContent:
        self.db.add(content)
        await self.db.commit()
        await self.db.refresh(content)
        return content
