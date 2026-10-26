from main import app

import pytest
from fastapi.testclient import TestClient


# IDs correspond to the contract-derived case table shown before generation.
# No database, external API, or state shared between requests is required.
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.parametrize(
    "amount, expected",
    [
        pytest.param(5000, {"amount": 5000, "discount": 0, "payable": 5000}, id="N01"),
        pytest.param(20000, {"amount": 20000, "discount": 1000, "payable": 19000}, id="N02"),
        pytest.param(1, {"amount": 1, "discount": 0, "payable": 1}, id="L01"),
        pytest.param(100000, {"amount": 100000, "discount": 1000, "payable": 99000}, id="L02"),
        pytest.param(9999, {"amount": 9999, "discount": 0, "payable": 9999}, id="R01"),
        pytest.param(10000, {"amount": 10000, "discount": 1000, "payable": 9000}, id="R02"),
        pytest.param(10001, {"amount": 10001, "discount": 1000, "payable": 9001}, id="R03"),
    ],
)
def test_quote_success(client, amount, expected):
    # Oracle: amount >= 10000 receives exactly 1000 off; payable = amount - discount.
    # Use literal expectations instead of calling the implementation's helper.
    response = client.post("/quotes", json={"amount": amount})

    assert response.status_code == 200
    actual = response.json()
    assert actual == expected
    # bool and float compare equal to some ints in Python; reject those responses.
    assert all(type(actual[key]) is int for key in expected)


@pytest.mark.parametrize(
    "body",
    [
        pytest.param({"amount": 0}, id="B01"),
        pytest.param({"amount": 100001}, id="B02"),
        pytest.param({}, id="M01"),
        pytest.param({"amount": "10000"}, id="T01"),
        pytest.param({"amount": 10000.0}, id="T02"),
        pytest.param({"amount": 1.5}, id="T03"),
        pytest.param({"amount": True}, id="T04"),
        pytest.param({"amount": None}, id="T05"),
        pytest.param({"amount": []}, id="T06"),
        pytest.param({"amount": {}}, id="T07"),
    ],
)
def test_quote_invalid_amount(client, body):
    response = client.post("/quotes", json=body)

    assert response.status_code == 422
    # Match the provided FastAPI error envelope without freezing full messages.
    detail = response.json()["detail"]
    assert isinstance(detail, list) and detail
    assert any(error.get("loc") == ["body", "amount"] for error in detail)


@pytest.mark.parametrize("case_id", [pytest.param("M02", id="M02")])
def test_quote_missing_body(client, case_id):
    response = client.post("/quotes")

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert isinstance(detail, list) and detail
    assert any(error.get("loc") == ["body"] for error in detail)
