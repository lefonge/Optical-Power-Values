#!/bin/bash

# Define script paths
JUNOS_SCRIPT="junos_optical_v1.6.py"  # Corrected filename
SROS_SCRIPT="sros_optical_v1.7.py"

# Define input files
JUNOS_INPUT="juniper_output.txt"
SROS_INPUT="nokia_output.txt"

# Ensure Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if Juniper input file exists
if [ ! -f "$JUNOS_INPUT" ]; then
    echo "Error: $JUNOS_INPUT not found!"
    exit 1
fi

# Run Juniper script
echo "Running Juniper Optical Parsing..."
python3 "$JUNOS_SCRIPT"

# Check if Nokia input file exists
if [ ! -f "$SROS_INPUT" ]; then
    echo "Error: $SROS_INPUT not found!"
    exit 1
fi

# Run Nokia script
echo "Running Nokia Optical Parsing..."
python3 "$SROS_SCRIPT"

echo "Processing completed!"
