"""Dedicated negative-path suite: malformed input, wrong content types,
and boundary IDs. Kept separate from the happy-path files so it's easy to
run in isolation with `pytest -m negative`.
"""
import pytest


@pytest.mark.negative
def test_add_product_with_missing_fields_does_not_500(session, api_base_url):
    resp = session.post(f"{api_base_url}/products/add", json={})
    assert resp.status_code < 500


@pytest.mark.negative
def test_malformed_json_body_is_rejected_or_ignored(session, api_base_url):
    resp = session.post(
        f"{api_base_url}/products/add",
        data="{not valid json",
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code < 500


@pytest.mark.negative
def test_negative_product_id_does_not_500(session, api_base_url):
    resp = session.get(f"{api_base_url}/products/-1")
    assert resp.status_code < 500


@pytest.mark.negative
def test_delete_nonexistent_user_does_not_500(session, api_base_url):
    resp = session.delete(f"{api_base_url}/users/999999")
    assert resp.status_code < 500


@pytest.mark.negative
def test_unsupported_http_method_on_products(session, api_base_url):
    resp = session.request("PATCH", f"{api_base_url}/products/abc")
    assert resp.status_code < 500
