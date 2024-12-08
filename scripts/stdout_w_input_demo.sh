#!/bin/bash

# Simulate a long-running process with continuous output
for i in {1..20}; do
    echo "Output line $i"
    sleep 0.5 # Wait for 1 second

    # At the 25th iteration, prompt the user for input
    if [ "$i" -eq 10 ]; then
        while true; do
            read -p "Do you wish to continue? (y/n): " yn
            case $yn in
            [Yy]*)
                echo "Continuing..."
                break
                ;;
            [Nn]*)
                echo "Exiting..."
                exit
                ;;
            *) echo "Please answer yes or no." ;;
            esac
        done
    fi
done
