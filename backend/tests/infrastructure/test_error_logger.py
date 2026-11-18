import uuid

import pytest

from app.application.services.integrations.error_logger import (
    _build_error_log_instance,
)
from app.meta.registry import MetaRegistry


@pytest.mark.asyncio
async def test_error_log_fallback_id_fits_database_column(monkeypatch):
    monkeypatch.setattr(MetaRegistry, "get", lambda _name: None)

    entry = await _build_error_log_instance(None, 500, "DatabaseError", "test")

    assert str(uuid.UUID(entry.id)) == entry.id
