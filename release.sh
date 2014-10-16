#!/bin/sh

rm -rf build dist __pycache__ */__pycache__
if [ -d build ]; then
    echo Please clean up
    exit
fi
git checkout stable || exit
git pull
git merge master || exit
git tag v`PYTHONPATH=. python -c 'import pyvx; print pyvx.__version__' 2>/dev/null | tail -1` || exit
git push --tags
python setup.py sdist || exit
twine upload dist/* || exit
git co master