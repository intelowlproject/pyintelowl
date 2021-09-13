#!/usr/bin/env bash
make html
cd _build/html && python3 -m http.server 6969 && cd ../../