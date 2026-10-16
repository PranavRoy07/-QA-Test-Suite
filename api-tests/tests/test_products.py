import pytest

REQUIRED_PRODUCT_FIELDS = {"id", "title", "price", "description", "category", "rating", "stock"}


@pytest.mark.smoke
def test_get_all_products_returns_200(session, api_base_url):
    resp = session.get(f"{api_base_url}/products")
    assert resp.status_code == 200
    body = resp.json()
    # dummyjson wraps lists: {"products": [...], "total": N, "skip": 0, "limit": 30}
    assert "products" in body
    assert isinstance(body["products"], list)
    assert len(body["products"]) > 0


@pytest.mark.regression
def test_product_schema_has_required_fields(session, api_base_url):
    resp = session.get(f"{api_base_url}/products/1")
    assert resp.status_code == 200
    body = resp.json()
    missing = REQUIRED_PRODUCT_FIELDS - body.keys()
    assert not missing, f"Response missing fields: {missing}"


@pytest.mark.regression
def test_product_field_types_are_correct(session, api_base_url):
    resp = session.get(f"{api_base_url}/products/1")
    body = resp.json()
    assert isinstance(body["id"], int)
    assert isinstance(body["title"], str)
    assert isinstance(body["price"], (int, float))
    assert isinstance(body["category"], str)
    assert isinstance(body["rating"], (int, float))
    assert isinstance(body["stock"], int)


@pytest.mark.regression
def test_get_products_by_category(session, api_base_url):
    resp = session.get(f"{api_base_url}/products/category/smartphones")
    assert resp.status_code == 200
    body = resp.json()
    assert all(item["category"] == "smartphones" for item in body["products"])


@pytest.mark.regression
def test_products_limit_query_param(session, api_base_url):
    resp = session.get(f"{api_base_url}/products?limit=3")
    assert resp.status_code == 200
    assert len(resp.json()["products"]) <= 3


@pytest.mark.negative
def test_get_nonexistent_product_returns_404(session, api_base_url):
    resp = session.get(f"{api_base_url}/products/999999")
    assert resp.status_code == 404


@pytest.mark.negative
def test_get_product_with_non_numeric_id_handled_gracefully(session, api_base_url):
    resp = session.get(f"{api_base_url}/products/not-a-number")
    # Should be rejected or treated as not-found, never a hard server crash.
    assert resp.status_code in (400, 404)
