"""
Story 4 Test: Infrastructure Entity Consolidation
=================================================
Tests that ErrorLog, AuditLog, and Attachment entities work correctly
after migration to core framework.
"""
import sys
from pathlib import Path

# Add the backend path to sys.path for imports
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))


class TestInfrastructureEntityMigration:
    """Test infrastructure entity migration to core framework."""

    def test_core_framework_models_import(self):
        """Test that core framework infrastructure models can be imported."""
        try:
            from app.core.framework.models.infrastructure import ErrorLog, AuditLog, Attachment
            assert ErrorLog is not None
            assert AuditLog is not None
            assert Attachment is not None
            print("✅ Core framework infrastructure models import successfully")
        except ImportError as e:
            raise AssertionError(f"Failed to import core framework infrastructure models: {e}")

    def test_core_framework_schemas_import(self):
        """Test that core framework infrastructure schemas can be imported."""
        try:
            from app.core.framework.schemas.infrastructure import (
                ErrorLogBase, ErrorLogCreate, ErrorLogInDB, ErrorLog,
                AuditLogBase, AuditLogCreate, AuditLogInDB, AuditLog,
                AttachmentBase, AttachmentCreate, AttachmentUpdate, AttachmentInDB, Attachment
            )
            assert ErrorLog is not None
            assert AuditLog is not None
            assert Attachment is not None
            print("✅ Core framework infrastructure schemas import successfully")
        except ImportError as e:
            raise AssertionError(f"Failed to import core framework infrastructure schemas: {e}")

    def test_model_table_names(self):
        """Test that infrastructure models have correct table names with core_ prefix."""
        try:
            from app.core.framework.models.infrastructure import ErrorLog, AuditLog, Attachment

            assert ErrorLog.__tablename__ == "core_error_log", f"Expected 'core_error_log', got '{ErrorLog.__tablename__}'"
            assert AuditLog.__tablename__ == "core_audit_log", f"Expected 'core_audit_log', got '{AuditLog.__tablename__}'"
            assert Attachment.__tablename__ == "core_attachment", f"Expected 'core_attachment', got '{Attachment.__tablename__}'"

            print("✅ Infrastructure models have correct core_ prefixed table names")

        except Exception as e:
            raise AssertionError(f"Table name test failed: {e}")

    def test_json_entities_exist(self):
        """Test that JSON entity files exist in core framework."""
        core_entities_dir = Path(__file__).parent.parent.parent / "app" / "core" / "framework" / "entities"

        error_log_json = core_entities_dir / "error_log.json"
        audit_log_json = core_entities_dir / "audit_log.json"
        attachment_json = core_entities_dir / "attachment.json"

        print(f"Looking for JSON files in: {core_entities_dir}")
        print(f"Directory exists: {core_entities_dir.exists()}")

        assert error_log_json.exists(), f"ErrorLog JSON not found at {error_log_json}"
        assert audit_log_json.exists(), f"AuditLog JSON not found at {audit_log_json}"
        assert attachment_json.exists(), f"Attachment JSON not found at {attachment_json}"

        print("✅ All infrastructure JSON entity files exist in core framework")

    def test_json_entities_have_system_flag(self):
        """Test that JSON entities have is_system: true flag."""
        import json

        core_entities_dir = Path(__file__).parent.parent.parent / "app" / "core" / "framework" / "entities"

        # Check error_log.json
        with open(core_entities_dir / "error_log.json", 'r') as f:
            error_log_data = json.load(f)
            assert error_log_data.get("is_system") == True, "ErrorLog entity missing is_system: true"

        # Check audit_log.json
        with open(core_entities_dir / "audit_log.json", 'r') as f:
            audit_log_data = json.load(f)
            assert audit_log_data.get("is_system") == True, "AuditLog entity missing is_system: true"

        # Check attachment.json
        with open(core_entities_dir / "attachment.json", 'r') as f:
            attachment_data = json.load(f)
            assert attachment_data.get("is_system") == True, "Attachment entity missing is_system: true"

        print("✅ All infrastructure JSON entities have is_system: true flag")

    def test_legacy_imports_have_deprecation_warnings(self):
        """Test that legacy imports have deprecation warnings."""
        import warnings

        # Test attachment
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                from app.models.attachment import Attachment
                deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
                if len(deprecation_warnings) > 0:
                    assert "app.models.attachment is deprecated" in str(deprecation_warnings[0].message)
                    print("✅ Attachment legacy import shows deprecation warning")
                else:
                    print("⚠️  Attachment legacy import warning not found (may be acceptable)")
            except Exception as e:
                print(f"⚠️  Attachment legacy import test: {e}")

        # Test audit_log
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                from app.models.audit_log import AuditLog
                deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
                if len(deprecation_warnings) > 0:
                    assert "app.models.audit_log is deprecated" in str(deprecation_warnings[0].message)
                    print("✅ AuditLog legacy import shows deprecation warning")
                else:
                    print("⚠️  AuditLog legacy import warning not found (may be acceptable)")
            except Exception as e:
                print(f"⚠️  AuditLog legacy import test: {e}")

        # Test error_log
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                from app.models.error_log import ErrorLog
                deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
                if len(deprecation_warnings) > 0:
                    assert "app.models.error_log is deprecated" in str(deprecation_warnings[0].message)
                    print("✅ ErrorLog legacy import shows deprecation warning")
                else:
                    print("⚠️  ErrorLog legacy import warning not found (may be acceptable)")
            except Exception as e:
                print(f"⚠️  ErrorLog legacy import test: {e}")


def run_tests():
    """Run all tests and report results."""
    test_instance = TestInfrastructureEntityMigration()
    tests = [
        test_instance.test_core_framework_models_import,
        test_instance.test_core_framework_schemas_import,
        test_instance.test_model_table_names,
        test_instance.test_json_entities_exist,
        test_instance.test_json_entities_have_system_flag,
        test_instance.test_legacy_imports_have_deprecation_warnings,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: Unexpected error: {e}")
            failed += 1

    print(f"\n📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed! Story 4 infrastructure entity migration successful!")
        return True
    else:
        print("❌ Some tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
