import pytest
from unittest.mock import MagicMock
from backend.stock_analisis import app, get_store_warehouse_data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_store_warehouse_data_basic(client, mocker):
    # Mock the Gemini API to return a predefined JSON response
    mock_response = {
        "stores": [{"id": "store_id_1"}, {"id": "store_id_2"}],
        "warehouses": [{"id": "warehouse_id_1"}, {"id": "warehouse_id_2"}],
        "edges": []
    }
    mocker.patch('backend.stock_analisis.client.chats.create', return_value=MagicMock(send_message=MagicMock(return_value=MagicMock(text=str(mock_response)))))

    # Send a request to the endpoint
    response = client.get('/get_store_warehouse_data')

    # Verify the response
    assert response.status_code == 200
    assert response.json == mock_response

def test_get_store_warehouse_data_relationships(client, mocker):
    # Mock the Gemini API to return a predefined JSON response
    mock_response = {
        "stores": [{"id": "store_id_1"}, {"id": "store_id_2"}],
        "warehouses": [{"id": "warehouse_id_1"}, {"id": "warehouse_id_2"}],
        "edges": [{"source": "store_id_1", "target": "warehouse_id_1"}]
    }
    mocker.patch('backend.stock_analisis.client.chats.create', return_value=MagicMock(send_message=MagicMock(return_value=MagicMock(text=str(mock_response)))))

    # Send a request to the endpoint
    response = client.get('/get_store_warehouse_data')

    # Verify the response
    assert response.status_code == 200
    assert response.json == mock_response

def test_get_store_warehouse_data_invalid_prompt(client, mocker):
    # Mock the Gemini API to return an error
    mocker.patch('backend.stock_analisis.client.chats.create', side_effect=Exception("Invalid prompt"))

    # Send a request to the endpoint
    response = client.get('/get_store_warehouse_data')

    # Verify the response
    assert response.status_code == 500
    assert response.json == {"error": "Invalid prompt"}
