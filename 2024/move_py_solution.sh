#!/bin/bash

# Script to move all .txt and .py files to a subdirectory called python_solution
# and remove .venv directory in a specified directory

# Check if a directory argument is provided
if [ $# -eq 0 ]; then
    echo "Error: Please provide a directory path"
    echo "Usage: $0 <directory_path>"
    exit 1
fi

# Store the provided directory path
target_dir="$1"

# Check if the provided directory exists
if [ ! -d "$target_dir" ]; then
    echo "Error: Directory '$target_dir' does not exist"
    exit 1
fi

# Change to the target directory
cd "$target_dir" || exit 1

# Create python_solution subdirectory if it doesn't exist
if [ ! -d "python_solution" ]; then
    echo "Creating 'python_solution' directory..."
    mkdir -p python_solution
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create 'python_solution' directory"
        exit 1
    fi
fi

# Move .txt files to python_solution
echo "Moving .txt files to python_solution..."
txt_files=$(find . -maxdepth 1 -type f -name "*.txt")
if [ -n "$txt_files" ]; then
    for file in $txt_files; do
        # Skip files that are already in python_solution
        if [[ "$file" != "./python_solution/"* ]]; then
            mv "$file" python_solution/
            echo "Moved: $file"
        fi
    done
else
    echo "No .txt files found in the current directory"
fi

# Move .py files to python_solution
echo "Moving .py files to python_solution..."
py_files=$(find . -maxdepth 1 -type f -name "*.py")
if [ -n "$py_files" ]; then
    for file in $py_files; do
        # Skip files that are already in python_solution
        if [[ "$file" != "./python_solution/"* ]]; then
            mv "$file" python_solution/
            echo "Moved: $file"
        fi
    done
else
    echo "No .py files found in the current directory"
fi

# Remove .venv directory if it exists
if [ -d ".venv" ]; then
    echo "Removing .venv directory..."
    rm -rf .venv
    if [ $? -eq 0 ]; then
        echo ".venv directory removed successfully"
    else
        echo "Error: Failed to remove .venv directory"
        exit 1
    fi
else
    echo "No .venv directory found"
fi

echo "Operation completed successfully!"


