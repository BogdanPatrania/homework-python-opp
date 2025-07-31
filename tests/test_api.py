from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_get():
    response = client.get("/")
    assert response.status_code == 200

def test_pow_api():
    response = client.post("/pow", json={"base": 2, "exponent": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 8

def test_fibonacci_api():
    response = client.get("/fibonacci?n=10")
    assert response.status_code == 200
    assert "result" in response.json()

def test_factorial_api():
    response = client.get("/factorial?n=5")
    assert response.status_code == 200
    assert response.json()["result"] == 120