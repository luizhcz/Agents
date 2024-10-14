import os
import pytest
import json
from fastapi.testclient import TestClient
from main import app  # Importe a instância da sua aplicação FastAPI

client = TestClient(app)

@pytest.fixture
def get_sample_text():
    """
    Helper fixture to load the sample text from the file.
    """
    file_path = os.path.join(os.path.dirname(__file__), '50275622000109-OPD26092023V01-000527158.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def test_process_endpoint(get_sample_text):
    """
    Test the /process/ endpoint using a sample text file and save the response to a JSON file.
    """
    input_data = {
        "id": "50275622000109-OPD26092023V01-000527158",  # Example ID for the test
        "texto": get_sample_text
    }

    response = client.post("/process/", json=input_data)

    # Check if the response status is 200 (success)
    assert response.status_code == 200
    response_data = response.json()

    # Check if the response contains processed data
    assert response_data["status"] == "success"
    assert "data" in response_data

    # Save the response to a JSON file inside the tests folder
    output_file_path = os.path.join(os.path.dirname(__file__), '50275622000109-OPD26092023V01-000527158.json')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(response_data, output_file, ensure_ascii=False, indent=4)

    # Ensure the data was saved correctly (optional assert)
    assert os.path.exists(output_file_path)