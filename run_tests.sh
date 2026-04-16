#!/bin/bash

# Activate the virtual environment
source .venv/Scripts/activate

# Run the test suite
pytest test_app.py

# Capture pytest's exit code and pass it back
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Tests failed."
    exit 1
fi