#!/bin/bash
set -e
echo "Starting Decentralized Finance Dashboard for Crypto Traders..."
uvicorn app:app --host 0.0.0.0 --port 9141 --workers 1
