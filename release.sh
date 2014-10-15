#!/bin/sh

rm -rf build dist __pycache__ */__pycache__
if [ -f build ]; then
    echo Please clean up
    exit
fi
python setup.py sdist upload
