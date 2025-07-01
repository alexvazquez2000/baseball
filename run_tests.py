
#!/usr/bin/env python3
"""
Test runner script for the Baseball League application.
This script runs all unit tests in the project.
"""

import unittest
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_all_tests():
    """Discover and run all tests in the project."""
    # Create a test loader
    loader = unittest.TestLoader()
    
    # Discover tests in the current directory
    # This will find all files that start with 'test_' and contain TestCase classes
    test_suite = loader.discover('.', pattern='test_*.py')
    
    # Create a test runner with verbosity level 2 for detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    result = runner.run(test_suite)
    
    # Return exit code based on test results
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
        return 1

def run_specific_test(test_module):
    """Run tests from a specific module."""
    try:
        # Load the specific test module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(test_module)
        
        # Run the tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1
    except Exception as e:
        print(f"Error loading test module '{test_module}': {e}")
        return 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test module if provided as argument
        test_module = sys.argv[1]
        if not test_module.startswith('test_'):
            test_module = f'test_{test_module}'
        if test_module.endswith('.py'):
            test_module = test_module[:-3]
        
        print(f"Running tests from module: {test_module}")
        exit_code = run_specific_test(test_module)
    else:
        # Run all tests
        print("Running all unit tests...")
        exit_code = run_all_tests()
    
    sys.exit(exit_code)
