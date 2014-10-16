#!/bin/sh

rm -rf build dist __pycache__ */__pycache__
if [ -d build ]; then
    echo Please clean up
    exit
fi
git checkout stable || exit
git merge master || exit

python setup.py sdist || exit
twine upload dist/*
