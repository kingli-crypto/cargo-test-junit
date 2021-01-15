#!/bin/bash -l

echo "Transforming cargo test output"
cat $1 | python /app/junit.py $2