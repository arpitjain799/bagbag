#!/bin/bash 

cd /app

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

python run.py 