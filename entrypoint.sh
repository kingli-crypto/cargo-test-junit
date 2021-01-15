#!/bin/bash -l

echo "Transforming cargo test output"
cat $1 | python3 src/junit.py $2