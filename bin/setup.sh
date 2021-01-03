#!/bin/bash
echo "(re)Creating virtual environment..."
rm -rf ./setcalc_venv
python3 -m venv ./setcalc_venv
echo "Done."
echo "Installing dependencies..."
source setcalc_venv/bin/activate
pip install -r requirements.txt
deactivate
