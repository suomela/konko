#!/bin/sh

exec python -m unittest discover -p '*.py' "$@"
