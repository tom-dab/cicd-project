import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_product(client):
    response = client.get('/product')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Stylo'
    assert data['price'] == 2.5

def test_add_product_ok(client):
    response = client.post('/product', json={"name": "Cahier", "price": 3.0})
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Produit ajouté'

def test_add_product_negative_price(client):
    response = client.post('/product', json={"name": "Cahier", "price": -1})
    assert response.status_code == 400
    assert 'prix doit être positif' in response.get_json()['error']
