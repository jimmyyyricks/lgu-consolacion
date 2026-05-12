"""
Story 7: Module Initialization with Core Framework Integration Tests
====================================================================
Tests that verify modules can access core framework entities during initialization.

This test file validates:
1. Core framework initializes before modules load
2. Modules can import and use core entities in their models/hooks
3. No circular dependencies between modules and core framework
"""
import pytest
import sys
import os
from pathlib import Path

# Ensure backend app is importable
BACKEND_ROOT = str(Path(__file__).resolve().parents[2])
sys.path.insert(0, BACKEND_ROOT)


class TestModuleLoaderCoreFrameworkIntegration:
    """Test that module loader properly initializes core framework first."""

    def test_core_framework_initializes_before_modules(self):
        """
        Verify that when load_modules() is called, core framework is initialized first.
        This ensures core entities are available for modules to reference.
        """
        from app.core.framework import is_initialized
        from app.core.loader import load_modules
        
        # Reset framework state to test initialization order
        import app.core.framework as framework_module
        framework_module._framework_initialized = False
        
        # Load modules (should initialize core framework first)
        load_modules()
        
        # Verify core framework is initialized
        assert is_initialized(), "Core framework should be initialized after load_modules()"

    def test_modules_can_import_core_entities(self):
        """
        Verify that all modules can import core entities without errors.
        This simulates what happens when modules reference core entities.
        """
        # Test importing core entities from module-like context
        from app.core.framework import (
            User, Role, EntityPermission,
            ErrorLog, AuditLog, Attachment, EmailLog, 
            NotificationSubscription, ScheduledJobLog,
            ModuleOrder, EntityOrder,
            WorkflowState, WorkflowAction, Workflow,
            WorkflowStateLink, WorkflowTransition,
            generate_slug,
        )
        
        # All entities should be importable and have correct table names
        assert User.__tablename__ == "core_users"
        assert Role.__tablename__ == "core_roles"
        assert EntityPermission.__tablename__ == "core_entity_permissions"
        assert ErrorLog.__tablename__ == "core_error_log"
        assert AuditLog.__tablename__ == "core_audit_log"
        assert Attachment.__tablename__ == "core_attachment"
        assert EmailLog.__tablename__ == "core_email_log"
        assert NotificationSubscription.__tablename__ == "core_notification_subscription"
        assert ScheduledJobLog.__tablename__ == "core_scheduled_job_log"
        assert ModuleOrder.__tablename__ == "core_module_orders"
        assert EntityOrder.__tablename__ == "core_entity_orders"
        assert WorkflowState.__tablename__ == "core_workflow_states"
        assert WorkflowAction.__tablename__ == "core_workflow_actions"
        assert Workflow.__tablename__ == "core_workflows"
        assert WorkflowStateLink.__tablename__ == "core_workflow_state_links"
        assert WorkflowTransition.__tablename__ == "core_workflow_transitions"

    def test_module_hooks_can_access_core_entities(self):
        """
        Verify that module hooks can import and use core entities.
        This validates the integration between module hooks and core framework.
        """
        # Simulate what a module hook would do
        from app.core.framework import User, Role, WorkflowState
        
        # Verify these are actual SQLAlchemy models that can be used
        from sqlalchemy.inspection import inspect
        
        assert inspect(User).mapper is not None
        assert inspect(Role).mapper is not None
        assert inspect(WorkflowState).mapper is not None

    def test_no_circular_imports_between_modules_and_core(self):
        """
        Verify that importing modules doesn't cause circular imports with core framework.
        """
        # Re-import core framework
        from app.core.framework import initialize_core_framework
        initialize_core_framework()
        
        # Now try to load a module that uses core entities
        from app.modules.core_eam import hooks as core_eam_hooks
        
        # If we get here without circular import error, test passes
        assert core_eam_hooks is not None

    def test_core_entity_access_function_works_in_module_context(self):
        """
        Verify that get_core_entity() works correctly in a module-like context.
        Note: This requires register_core_models() to be called first (as in main.py).
        """
        from app.core.framework import list_core_entities
        from app.infrastructure.database.repositories.entity_repository import register_core_models
        
        # Register core models with entity repository (happens in main.py lifespan)
        register_core_models()
        
        # Test that all core entities can be retrieved by name
        expected_entities = [
            'user', 'role', 'entity_permission',
            'error_log', 'audit_log', 'attachment',
            'email_log', 'notification_subscription', 'scheduled_job_log',
            'module_order', 'entity_order',
            'workflow_state', 'workflow_action', 'workflow',
            'workflow_state_link', 'workflow_transition',
        ]
        
        available = list_core_entities()
        for entity_name in expected_entities:
            assert entity_name in available, f"Entity '{entity_name}' should be available"
        
        # Now test get_core_entity after registration
        from app.core.framework import get_core_entity
        for entity_name in expected_entities:
            entity_class = get_core_entity(entity_name)
            assert entity_class is not None

    def test_framework_metadata_uses_single_root(self):
        """Verify all core metadata is consolidated under app/core/framework/entities only."""
        framework_entities_dir = Path(BACKEND_ROOT) / "app" / "core" / "framework" / "entities"
        legacy_entities_dir = Path(BACKEND_ROOT) / "app" / "core" / "entities"

        expected_framework_entities = {
            'user', 'role', 'entity_permission',
            'error_log', 'audit_log', 'attachment',
            'email_log', 'notification_subscription', 'scheduled_job_log',
            'module_order', 'entity_order',
            'workflow_state', 'workflow_action', 'workflow',
            'workflow_state_link', 'workflow_transition',
        }

        actual_framework_entities = {
            path.stem for path in framework_entities_dir.glob('*.json')
        }
        legacy_entities = {
            path.stem for path in legacy_entities_dir.glob('*.json')
        }

        assert actual_framework_entities == expected_framework_entities
        assert legacy_entities == set()


class TestModuleCoreEntityReferences:
    """Test that modules correctly reference core entities in their code."""

    def test_core_eam_module_uses_core_entities(self):
        """
        Verify that core_eam module can import and use core entities.
        """
        # This tests the actual integration between a module and core framework
        from app.modules.core_eam.hooks import register_hooks
        
        # The hook registration should work without errors
        assert callable(register_hooks)

    def test_purchasing_stores_module_uses_core_entities(self):
        """
        Verify that purchasing_stores module can import and use core entities.
        """
        from app.modules.purchasing_stores.hooks import register_hooks
        
        assert callable(register_hooks)

    def test_asset_management_module_uses_core_entities(self):
        """
        Verify that asset_management module can import and use core entities.
        """
        from app.modules.asset_management.hooks import register_hooks
        
        assert callable(register_hooks)

    def test_maintenance_mgmt_module_uses_core_entities(self):
        """
        Verify that maintenance_mgmt module can import and use core entities.
        """
        from app.modules.maintenance_mgmt.hooks import register_hooks
        
        assert callable(register_hooks)

    def test_work_mgmt_module_uses_core_entities(self):
        """
        Verify that work_mgmt module can import and use core entities.
        """
        from app.modules.work_mgmt.hooks import register_hooks
        
        assert callable(register_hooks)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
