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

    # Provide lightweight stand-ins for langchain components to avoid heavy
    # dependencies when importing the application module.
    langchain_pkg = types.ModuleType("langchain")
    embeddings_pkg = types.ModuleType("langchain.embeddings")
    vectorstores_pkg = types.ModuleType("langchain.vectorstores")
    splitter_pkg = types.ModuleType("langchain.text_splitter")
    loaders_pkg = types.ModuleType("langchain.document_loaders")

    class DummyEmbeddings:
        def __init__(self, *a, **k):
            pass

    class DummyChroma:
        @classmethod
        def from_documents(cls, docs, embedding):
            return cls()

        def similarity_search(self, *a, **k):
            return []

    class DummySplitter:
        def __init__(self, *a, **k):
            pass

        def split_documents(self, docs):
            return docs

    class DummyLoader:
        def __init__(self, *a, **k):
            pass

        def load(self):
            return [types.SimpleNamespace(page_content="dummy")]

    embeddings_pkg.HuggingFaceEmbeddings = DummyEmbeddings
    vectorstores_pkg.Chroma = DummyChroma
    splitter_pkg.RecursiveCharacterTextSplitter = DummySplitter
    loaders_pkg.TextLoader = DummyLoader

    langchain_pkg.embeddings = embeddings_pkg
    langchain_pkg.vectorstores = vectorstores_pkg
    langchain_pkg.text_splitter = splitter_pkg
    langchain_pkg.document_loaders = loaders_pkg

    monkeypatch.setitem(sys.modules, "langchain", langchain_pkg)
    monkeypatch.setitem(sys.modules, "langchain.embeddings", embeddings_pkg)
    monkeypatch.setitem(sys.modules, "langchain.vectorstores", vectorstores_pkg)
    monkeypatch.setitem(sys.modules, "langchain.text_splitter", splitter_pkg)
    monkeypatch.setitem(sys.modules, "langchain.document_loaders", loaders_pkg)

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
