#!/bin/bash
echo "🚀 Iniciando Merse-Codex Backend…"
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-9000}
