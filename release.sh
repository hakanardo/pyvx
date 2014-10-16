#!/bin/sh

git tag v`PYTHONPATH=. python -c 'import pyvx; print pyvx.__version__' 2>/dev/null | tail -1` || exit
git checkout stable || exit
git pull
git merge master || exit
git push --tags
git co master