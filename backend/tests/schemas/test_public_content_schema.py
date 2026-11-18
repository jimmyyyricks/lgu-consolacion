import pytest
from pydantic import ValidationError

from app.api.schemas.public_content import PublicContentInput, extract_drive_file_id


def test_extract_drive_file_id_from_share_link():
    assert (
        extract_drive_file_id(
            "https://drive.google.com/file/d/Abc_123/view?usp=sharing"
        )
        == "Abc_123"
    )


@pytest.mark.parametrize(
    "url",
    [
        "http://drive.google.com/file/d/file-id/view",
        "https://example.com/file/d/file-id/view",
        "https://drive.google.com/file/d/invalid%20id/view",
    ],
)
def test_extract_drive_file_id_rejects_unsafe_or_invalid_links(url):
    with pytest.raises(ValueError):
        extract_drive_file_id(url)


def test_published_document_requires_drive_file():
    with pytest.raises(ValidationError):
        PublicContentInput(
            slug="council-ordinance",
            kind="ordinance",
            title="Council ordinance",
            summary="Approved description",
            status="published",
        )


def test_document_input_stores_drive_file_id():
    content = PublicContentInput(
        slug="council-ordinance",
        kind="ordinance",
        title="Council ordinance",
        summary="Approved description",
        status="published",
        drive_url="https://drive.google.com/file/d/Abc_123/view",
    )
    assert content.drive_url == "Abc_123"


def test_non_drive_url_is_not_accepted_as_document():
    with pytest.raises(ValidationError):
        PublicContentInput(
            slug="council-ordinance",
            kind="ordinance",
            title="Council ordinance",
            summary="Approved description",
            status="published",
            drive_url="https://example.com/ordinance.pdf",
        )


def test_featured_news_accepts_local_image_path():
    content = PublicContentInput(
        slug="community-cleanup-demo",
        kind="news",
        title="Community clean-up",
        summary="Fictional demo content.",
        image_url="/images/consolacion-cover-photo.jpg",
        featured=True,
    )

    assert content.featured is True
    assert content.image_url == "/images/consolacion-cover-photo.jpg"


def test_non_news_cannot_be_featured():
    with pytest.raises(ValidationError):
        PublicContentInput(
            slug="featured-ordinance",
            kind="ordinance",
            title="Featured ordinance",
            summary="Not a news or event item.",
            featured=True,
        )


@pytest.mark.parametrize("image_url", ["javascript:alert(1)", "//example.com/image.jpg"])
def test_image_url_rejects_unsafe_urls(image_url):
    with pytest.raises(ValidationError):
        PublicContentInput(
            slug="community-cleanup-demo",
            kind="news",
            title="Community clean-up",
            summary="Fictional demo content.",
            image_url=image_url,
        )
