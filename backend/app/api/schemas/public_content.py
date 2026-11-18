from datetime import date, datetime
from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ContentKind = Literal[
    "ordinance",
    "resolution",
    "memorandum",
    "executive_order",
    "disclosure",
    "bid",
    "form",
    "government_action",
    "news",
    "tourism",
]
ContentStatus = Literal["draft", "published", "archived"]
DOCUMENT_KINDS = {
    "ordinance",
    "resolution",
    "memorandum",
    "executive_order",
    "disclosure",
    "bid",
    "form",
}


def extract_drive_file_id(value: str | None) -> str | None:
    if not value:
        return None
    from urllib.parse import parse_qs, urlparse
    import re

    parsed = urlparse(value.strip())
    if parsed.scheme != "https" or parsed.hostname != "drive.google.com":
        raise ValueError("Use a Google Drive URL over HTTPS")
    match = re.match(r"^/file/d/([^/]+)(?:/|$)", parsed.path)
    file_id = (
        match.group(1)
        if match
        else parse_qs(parsed.query).get("id", [None])[0]
        if parsed.path in {"/open", "/uc"}
        else None
    )
    if not file_id or not re.fullmatch(r"[A-Za-z0-9_-]+", file_id):
        raise ValueError("The Google Drive URL does not contain a valid file ID")
    return file_id


class PublicContentInput(BaseModel):
    slug: str = Field(min_length=1, max_length=180, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    kind: ContentKind
    title: str = Field(min_length=1, max_length=300)
    document_number: str | None = Field(default=None, max_length=120)
    summary: str = Field(default="", max_length=4000)
    body: str | None = None
    category: str | None = Field(default=None, max_length=100)
    image_url: str | None = Field(default=None, max_length=1000)
    featured: bool = False
    record_date: date | None = None
    status: ContentStatus = "draft"
    drive_url: str | None = None

    @field_validator("drive_url")
    @classmethod
    def normalize_drive_url(cls, value: str | None) -> str | None:
        return extract_drive_file_id(value)

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value: str | None) -> str | None:
        if not value:
            return None
        if value.startswith("/") and not value.startswith("//"):
            return value
        parsed = urlparse(value)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username:
            raise ValueError("Use a local asset path or HTTPS image URL")
        return value

    @model_validator(mode="after")
    def require_document_for_publication(self):
        if self.kind not in DOCUMENT_KINDS and not self.summary.strip():
            raise ValueError("A summary is required for this content type")
        if self.featured and self.kind != "news":
            raise ValueError("Only news and events can be featured")
        if (
            self.status == "published"
            and self.kind in DOCUMENT_KINDS
            and not self.drive_url
        ):
            raise ValueError("A public Drive PDF is required to publish this document")
        return self


class PublicContentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    document_number: str | None = Field(default=None, max_length=120)
    summary: str | None = Field(default=None, min_length=1, max_length=4000)
    body: str | None = None
    category: str | None = Field(default=None, max_length=100)
    image_url: str | None = Field(default=None, max_length=1000)
    featured: bool | None = None
    record_date: date | None = None
    status: ContentStatus | None = None
    drive_url: str | None = None

    @field_validator("drive_url")
    @classmethod
    def normalize_drive_url(cls, value: str | None) -> str | None:
        return extract_drive_file_id(value)

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value: str | None) -> str | None:
        if not value:
            return None
        if value.startswith("/") and not value.startswith("//"):
            return value
        parsed = urlparse(value)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username:
            raise ValueError("Use a local asset path or HTTPS image URL")
        return value


class PublicContentOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    slug: str
    kind: str
    title: str
    document_number: str | None
    summary: str
    body: str | None
    category: str | None
    image_url: str | None
    featured: bool
    record_date: date | None
    status: str
    drive_file_id: str | None
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None


class PublicContentArchivePage(BaseModel):
    items: list[PublicContentOutput]
    total: int
    years: list[int]
