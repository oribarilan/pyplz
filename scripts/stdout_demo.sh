#!/bin/bash

# Simulate a long-running process with continuous output
for i in {1..20}; do
    echo "Output line $i"
    sleep 0.5 # Wait for 1 second
done
