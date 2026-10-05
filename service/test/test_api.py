from fastapi.testclient import TestClient

from service.app import app


class TestSummarizeApi:
    def setup_method(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_summarize_returns_requested_number_of_sentences(self) -> None:
        payload = {
            "text": (
                "Python — это язык программирования. "
                "Python используется в машинном обучении. "
                "Python популярен среди разработчиков. "
                "Бананы — жёлтые фрукты."
            ),
            "num_sentences": 2,
        }
        response = self.client.post("/summarize", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body["num_sentences"] == 2
        assert body["summary"]

    def test_summarize_validation_error_on_empty_text(self) -> None:
        response = self.client.post("/summarize", json={"text": ""})
        assert response.status_code == 422
