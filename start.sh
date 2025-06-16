#!/bin/bash
source venv/bin/activate
uvicorn vector_rag_fennec:app --reload --port 8000
