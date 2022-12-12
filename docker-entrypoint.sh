#!/bin/bash 

cd /app

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

if [[ -z "${RUN}" ]]; then
    RUN="run.py"
fi 

python $RUN