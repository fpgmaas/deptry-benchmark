#!/bin/bash

# Check for correct number of command line arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <version> <source>"
  echo "<version> is the version number of deptry to install."
  echo "<source> is either 'pypi' for the Python Package Index or 'test-pypi' for Test PyPI."
  exit 1
fi

VERSION=$1
SOURCE=$2
PYPI_URL="https://pypi.org/simple"
TEST_PYPI_URL="https://test.pypi.org/simple"

# Determine which PyPI URL to use based on the source argument
if [ "$SOURCE" = "pypi" ]; then
  INSTALL_URL="$PYPI_URL"
elif [ "$SOURCE" = "test-pypi" ]; then
  INSTALL_URL="$TEST_PYPI_URL"
else
  echo "Error: source must be either 'pypi' or 'test-pypi'"
  exit 1
fi

# Define large Python repositories with requirements.txt
REPOS=(
  "https://github.com/pandas-dev/pandas.git"
  "https://github.com/matplotlib/matplotlib.git"
  "https://github.com/aws/aws-cli"
  "https://github.com/pydantic/pydantic"
  "https://github.com/pallets/flask"
)

# Create a directory for the benchmarks
mkdir -p benchmark_results
cd benchmark_results

# Function to extract scanned files and found issues from deptry output
function extract_metrics {                       
  local file=$1
  # Extract numbers following specific phrases
  scanned_files=$(grep 'Scanning [0-9]* files' "$file" | awk '{print $2}')
  found_issues=$(grep 'Found [0-9]* dependency issues' "$file" | awk '{print $2}')
  echo "$scanned_files $found_issues"
}

# Loop through the repositories
for repo_url in "${REPOS[@]}"; do
  repo_name=$(basename -s .git "$repo_url")
  
  # Clone the repository
  git clone "$repo_url" --depth=1
  cd "$repo_name"

  # Create venv and install project
  python -m venv venv
  . ./venv/bin/activate
  pip install -e .

  # Install and benchmark deptry, capturing both stdout and stderr
  if [ "$SOURCE" = "test-pypi" ]; then
    pip install --index-url "$INSTALL_URL" deptry==$VERSION
  else
    pip install deptry==$VERSION
  fi

  deptry . > "../${repo_name}_deptry_${VERSION}_output.txt" 2>&1
  hyperfine -i -m 25 'deptry .' --warmup 2 > "../${repo_name}_deptry_${VERSION}_benchmark.txt"

  # No version comparison here, since we're focusing on a single version run per script execution
  
  echo "Completed benchmark for ${repo_name} with deptry ${VERSION}"

  # Clean up and move to the next repository
  cd ..
  rm -rf "$repo_name"
done

echo "Benchmarking complete."
cd ..
