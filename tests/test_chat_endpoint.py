import importlib
import os
import sys
import types

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):
    dummy_module = types.ModuleType("llama_cpp")

    class DummyLlama:
        def __init__(self, *a, **k):
            pass

        def create_chat_completion(self, *a, **k):
            return {"choices": [{"message": {"content": "Hello"}}]}

    dummy_module.Llama = DummyLlama
    monkeypatch.setitem(sys.modules, "llama_cpp", dummy_module)

    root_dir = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, root_dir)

    module = importlib.import_module("vector_rag_fennec")
    importlib.reload(module)
    return TestClient(module.app)


def test_chat_endpoint(client):
    resp = client.post("/api/chat", json={"prompt": "Hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data
