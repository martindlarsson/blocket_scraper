#!/bin/bash

cd "/mnt/Blocket/Kod (1)/"
echo "Source blocket-env/bin/activate"
source "blocket-env/bin/activate"
echo "python main.py"
python main.py
echo "deactivate"
deactivate
