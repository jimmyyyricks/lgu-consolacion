"""Requests-based integration checks for the role-based dashboard orchestrator."""

import os
import sys

import pytest
import requests


BASE_URL = "http://localhost:8000"
ALL_WIDGET_TYPES = {
    "pr_status_summary",
    "pr_attention_list",
    "po_status_summary",
    "inventory_summary",
    "inventory_low_stock",
    "stock_count_summary",
    "work_order_summary",
    "work_order_attention_list",
    "my_work_order_list",
    "maintenance_summary",
}
ALL_DASHBOARDS = {"procurement", "work-management", "inventory"}


def get_token(username: str = "admin", password: str = "admin123") -> str:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": username, "password": password},
    )
    response.raise_for_status()
    return response.json()["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def admin_token() -> str:
    return get_token("admin", "admin123")


@pytest.fixture(scope="module")
def dashboard_response(admin_token: str):
    return requests.get(
        f"{BASE_URL}/api/operations/dashboard/role-based",
        headers=auth_headers(admin_token),
    )


class TestResponseShape:
    def test_status_200(self, dashboard_response):
        assert dashboard_response.status_code == 200

    def test_top_level_keys(self, dashboard_response):
        body = dashboard_response.json()
        assert "user_roles" in body
        assert "generated_at" in body
        assert "allowed_dashboards" in body
        assert "selected_dashboard" in body

    def test_allowed_dashboards_is_list(self, dashboard_response):
        body = dashboard_response.json()
        assert isinstance(body["allowed_dashboards"], list)

    def test_selected_dashboard_is_object_for_superuser(self, dashboard_response):
        body = dashboard_response.json()
        assert isinstance(body["selected_dashboard"], dict)


class TestDashboardSelection:
    def test_superuser_gets_all_dashboards(self, dashboard_response):
        body = dashboard_response.json()
        keys = {dashboard["key"] for dashboard in body["allowed_dashboards"]}
        assert keys == ALL_DASHBOARDS

    def test_default_selected_dashboard_is_first_allowed(self, dashboard_response):
        body = dashboard_response.json()
        assert body["allowed_dashboards"][0]["key"] == "procurement"
        assert body["selected_dashboard"]["key"] == "procurement"

    def test_requested_dashboard_is_returned_when_allowed(self, admin_token):
        response = requests.get(
            f"{BASE_URL}/api/operations/dashboard/role-based",
            headers=auth_headers(admin_token),
            params={"dashboard_key": "work-management"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["selected_dashboard"]["key"] == "work-management"

    def test_invalid_dashboard_falls_back_to_first_allowed(self, admin_token):
        response = requests.get(
            f"{BASE_URL}/api/operations/dashboard/role-based",
            headers=auth_headers(admin_token),
            params={"dashboard_key": "does-not-exist"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["selected_dashboard"]["key"] == "procurement"


class TestSelectedDashboardPayload:
    def test_selected_dashboard_has_required_fields(self, dashboard_response):
        selected = dashboard_response.json()["selected_dashboard"]
        assert {"key", "label", "description", "icon", "widgets"}.issubset(selected)

    def test_widgets_match_selected_dashboard_scope(self, admin_token):
        response = requests.get(
            f"{BASE_URL}/api/operations/dashboard/role-based",
            headers=auth_headers(admin_token),
            params={"dashboard_key": "inventory"},
        )
        body = response.json()
        types = {widget["type"] for widget in body["selected_dashboard"]["widgets"]}
        assert types <= {"inventory_summary", "inventory_low_stock", "stock_count_summary"}

    def test_selected_widget_types_are_known(self, dashboard_response):
        widgets = dashboard_response.json()["selected_dashboard"]["widgets"]
        unknown = {widget["type"] for widget in widgets} - ALL_WIDGET_TYPES
        assert not unknown

    def test_widget_config_has_readonly_flag(self, dashboard_response):
        for widget in dashboard_response.json()["selected_dashboard"]["widgets"]:
            assert "readonly" in widget["config"]
            assert isinstance(widget["config"]["readonly"], bool)


class TestDirectMappingContracts:
    @staticmethod
    def _import_service_symbols():
        backend_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        from app.application.services.role_based_dashboard_service import (
            DASHBOARD_DEFINITIONS,
            ROLE_WIDGET_MAP,
            WIDGET_DASHBOARD_MAP,
        )

        return DASHBOARD_DEFINITIONS, ROLE_WIDGET_MAP, WIDGET_DASHBOARD_MAP

    def test_dashboard_definitions_cover_expected_dashboards(self):
        dashboard_definitions, _, _ = self._import_service_symbols()
        assert set(dashboard_definitions.keys()) == ALL_DASHBOARDS

    def test_requestor_widgets_are_readonly(self):
        _, role_widget_map, _ = self._import_service_symbols()
        for widget in role_widget_map["Requestor"]:
            assert widget["readonly"] is True

    def test_technician_summary_is_readonly(self):
        _, role_widget_map, _ = self._import_service_symbols()
        summary_widget = next(
            widget
            for widget in role_widget_map["Technician"]
            if widget["type"] == "work_order_summary"
        )
        assert summary_widget["readonly"] is True

    def test_each_widget_maps_to_a_dashboard(self):
        _, role_widget_map, widget_dashboard_map = self._import_service_symbols()
        widget_types = {
            widget["type"]
            for widgets in role_widget_map.values()
            for widget in widgets
        }
        assert widget_types <= set(widget_dashboard_map.keys())


class TestNonRegression:
    def test_work_orders_dashboard_still_200(self, admin_token):
        response = requests.get(
            f"{BASE_URL}/api/operations/dashboard/work-orders",
            headers=auth_headers(admin_token),
        )
        assert response.status_code == 200

    def test_purchase_requests_dashboard_still_200(self, admin_token):
        response = requests.get(
            f"{BASE_URL}/api/operations/dashboard/purchase-requests",
            headers=auth_headers(admin_token),
        )
        assert response.status_code == 200

    def test_inventory_dashboard_still_200(self, admin_token):
        response = requests.get(
            f"{BASE_URL}/api/operations/dashboard/inventory",
            headers=auth_headers(admin_token),
        )
        assert response.status_code == 200
