from tests.conftest import client

def test_create_author(client):
    response = client.post("/authors/", json={"name": "Test Author"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Author"

def test_recommend_endpoint(client):
    # Сначала добавим книгу, затем проверим рекомендацию
    client.post("/authors/", json={"name": "Author1"})
    client.post("/books/", json={"title": "Book1", "year": 2020, "author_id": 1})
    response = client.post("/analytics/recommend", json={"min_year": 2010, "limit": 3})
    assert response.status_code == 200
    assert isinstance(response.json(), list)