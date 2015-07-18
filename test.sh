#!/bin/sh

exec python3 -m unittest discover -p '*.py' "$@"
