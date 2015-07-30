#!/bin/sh

exec pypy -m unittest discover -p '*.py' "$@"
