#!/bin/bash

source venv/bin/activate
pip3 install -r requirements.txt
uvicorn app.main:app --reload --port 8000
