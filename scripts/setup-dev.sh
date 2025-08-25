#!/bin/bash
# Developer Setup Script for MTA-STS Policy Repository
# This script sets up a complete development environment

set -e  # Exit on any error

echo "🚀 Setting up MTA-STS Policy development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f ".well-known/mta-sts.txt" ]; then
    print_error "This script must be run from the mta-sts-policy repository root"
    exit 1
fi

print_status "Setting up Python virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Created virtual environment"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Activated virtual environment"

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip

# Create requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt << EOF
# MTA-STS Policy Validation Dependencies
# No external dependencies required for basic validation
EOF
    print_success "Created requirements.txt"
fi

print_success "Python environment setup complete"

# Set up git hooks
print_status "Setting up git hooks..."

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy pre-commit hook
if [ -f "scripts/pre-commit" ]; then
    cp scripts/pre-commit .git/hooks/
    chmod +x .git/hooks/pre-commit
    print_success "Installed pre-commit hook"
else
    print_warning "Pre-commit hook not found in scripts/ directory"
fi

# Set up git configuration
print_status "Configuring git..."

# Set up git user if not configured
if [ -z "$(git config user.name)" ]; then
    print_warning "Git user name not configured"
    print_status "Please run: git config user.name 'Your Name'"
fi

if [ -z "$(git config user.email)" ]; then
    print_warning "Git user email not configured"
    print_status "Please run: git config user.email 'your.email@example.com'"
fi

print_success "Git configuration complete"

# Test the validation script
print_status "Testing validation script..."
if python3 scripts/validate-policy.py; then
    print_success "Validation script test passed"
else
    print_error "Validation script test failed"
    exit 1
fi

# Create test directory and test policy
print_status "Setting up test environment..."
mkdir -p tests
if [ ! -f "tests/test-policy.txt" ]; then
    cat > tests/test-policy.txt << EOF
version: STSv1
mode: testing
mx: *.example.com
max_age: 86400
EOF
    print_success "Created test policy file"
fi

# Run tests
print_status "Running tests..."
if python3 tests/test-validation.py; then
    print_success "All tests passed"
else
    print_warning "Some tests failed - this is normal for initial setup"
fi

print_success "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Make changes to .well-known/mta-sts.txt"
echo "3. Test with: python3 scripts/validate-policy.py"
echo "4. Commit changes (validation will run automatically)"
echo ""
echo "Happy coding! 🚀"
