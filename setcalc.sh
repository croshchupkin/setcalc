#!/bin/bash
if [ ! -d ./setcalc_venv/ ]; then
    source ./bin/setup.sh
    echo
fi
source ./bin/run.sh $@
