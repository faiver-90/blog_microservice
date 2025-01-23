#!/bin/bash

# Function to create the base project structure
create_base_structure() {
  echo "Creating base structure for project: $1..."
  mkdir -p "$1"/{app,tests}
  touch "$1"/{main.py,requirements.txt,Dockerfile,README.md}

  # Copy .gitignore from the script's directory if it exists
  SCRIPT_DIR=$(dirname "$(realpath "$0")")

  if [ -f "$SCRIPT_DIR/.gitignore" ]; then
    cp "$SCRIPT_DIR/.gitignore" "$1/.gitignore"
    echo "Copied .gitignore to $1/.gitignore from $SCRIPT_DIR/.gitignore"
  else
    echo "Warning: .gitignore file not found in the script's directory ($SCRIPT_DIR)."
    touch "$1/.gitignore"
    echo "Created an empty .gitignore in $1/.gitignore"
  fi

  # Create README.md, .gitignore, and docker-compose.yml in the execution directory if not present
  if [ ! -f "README.md" ]; then
    touch "README.md"
    echo "# Project Documentation" > "README.md"
    echo "Created README.md in the execution directory."
  fi

  if [ ! -f ".gitignore" ]; then
    touch ".gitignore"
    echo "# Ignore Python compiled files" >> ".gitignore"
    echo "*.pyc" >> ".gitignore"
    echo "__pycache__/" >> ".gitignore"
    echo ".idea" >> ".gitignore"
    echo "Created default .gitignore in the execution directory."
  fi

  if [ ! -f "docker-compose.yml" ]; then
    touch "docker-compose.yml"
    echo "version: '3.8'" > "docker-compose.yml"
    echo "services:" >> "docker-compose.yml"
    echo "  app:" >> "docker-compose.yml"
    echo "    build: ." >> "docker-compose.yml"
    echo "    ports:" >> "docker-compose.yml"
    echo "      - '8000:8000'" >> "docker-compose.yml"
    echo "Created docker-compose.yml in the execution directory."
  fi
}

# Function to create the app folder structure
create_app_structure() {
  echo "Creating app folder structure for project: $1..."
  mkdir -p "$1"/app/{api/{v1},core,db/{migrations},services,repositories,utils,schemas}
  touch "$1"/app/{__init__.py,core/{__init__.py,config.py,security.py},db/{__init__.py,session.py},services/__init__.py,repositories/__init__.py,utils/__init__.py,schemas/{__init__.py,pydantic_schema.py}}
  touch "$1"/app/api/{__init__.py,v1/{__init__.py,endpoints.py,dependencies.py}}
}

# Function to create the tests folder structure
create_tests_structure() {
  echo "Creating tests folder structure for project: $1..."
  mkdir -p "$1"/tests/test_api/test_v1
  touch "$1"/tests/{__init__.py,conftest.py,test_main.py}
  touch "$1"/tests/test_api/{__init__.py,test_v1/{__init__.py,test_endpoints.py,test_models.py}}
}

# Main function to execute all steps
main() {
  if [ -z "$1" ]; then
    echo "Error: Project name is required."
    echo "Usage: $0 <project_name>"
    exit 1
  fi

  create_base_structure "$1"
  create_app_structure "$1"
  create_tests_structure "$1"
  echo "Project structure for '$1' created successfully."
}

# Execute the main function
main "$1"