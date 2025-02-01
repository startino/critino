from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

@pytest.fixture
def mock_transcript(mocker):
    mocker.patch(
        "app.utils.youtube.get_transcript",
        return_value="Sample transcript text about AI development."
    )

def test_generate_critiques(mock_transcript):
    test_request = {
        "youtube_url": "https://www.youtube.com/watch?v=gR8QvFmNuLE",
        "context": "AI Development",
        "query": "what are they addressing about",
        "optimal_response": "Follow these steps..."
    }
    
    response = client.post("/critiques/", json=test_request)
    assert response.status_code == 200
    assert len(response.json()) > 0
    first = response.json()[0]
    assert all(key in first for key in 
        ["context", "query", "optimal_response", "situation"])