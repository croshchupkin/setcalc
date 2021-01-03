#!/bin/bash
source ./setcalc_venv/bin/activate
python -m setcalc $@
deactivate
