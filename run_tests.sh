#!/usr/bin/bash
CURRDIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)
PYTHONPATH=$CURRDIR/src
export PYTHONPATH=$PYTHONPATH
cd test/
python3 -m unittest discover .
cd ..