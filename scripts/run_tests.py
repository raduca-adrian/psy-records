import unittest
import os
import argparse
from unittest import TextTestRunner, TestResult
import sys
from coverage import Coverage

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class ColoredTestResult(TestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success_count = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        sys.stdout.write('\033[92m.\033[0m')  # Green for success
        sys.stdout.flush()

    def addFailure(self, test, err):
        super().addFailure(test, err)
        sys.stdout.write('\033[91mF\033[0m')  # Red for failure
        sys.stdout.flush()

    def addError(self, test, err):
        super().addError(test, err)
        sys.stdout.write('\033[91mE\033[0m')  # Red for error
        sys.stdout.flush()

    def startTest(self, test):
        super().startTest(test)

    def stopTest(self, test):
        super().stopTest(test)

class ColoredTestRunner(TextTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, resultclass=ColoredTestResult, **kwargs)

    def run(self, test):
        result = super().run(test)
        total_tests = result.testsRun
        passed = result.success_count
        failures = len(result.failures)
        errors = len(result.errors)
        
        pass_rate = (passed / total_tests) * 100 if total_tests > 0 else 0

        print(f"\n\n{'='*70}")
        print("Test Run Summary")
        print(f"{'='*70}")
        print(f"Total tests run: {total_tests}")
        print(f"\033[92mPassed: {passed}\033[0m")
        print(f"\033[91mFailures: {failures}\033[0m")
        print(f"\033[91mErrors: {errors}\033[0m")
        print(f"Pass Rate: {pass_rate:.2f}%")
        print(f"{'='*70}")
        
        return result

def run_tests(test_category='all', verbosity=2, use_coverage=False):
    """
    Runs tests based on the specified category.
    - 'all': Runs all tests.
    - 'unit': Runs only unit tests.
    - 'integration': Runs only integration tests.
    - 'ui': Runs only UI-related tests.
    - 'layout': Runs responsive layout tests.
    - 'qss': Runs QSS helper tests.
    - 'config': Runs config and settings tests.
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tests'))

    if test_category == 'all':
        suite = loader.discover(start_dir=test_dir, pattern="test_*.py")
    else:
        # Define test modules for each category
        test_files = {
            'unit': ['test_modern_ui.py', 'test_config.py'],
            'integration': ['test_integration.py'],
            'ui': ['test_modern_ui.py'],
            'layout': ['test_responsive_layout.py'],
            'qss': ['test_modern_qss.py'],
            'comprehensive': ['test_comprehensive.py'],
            'config': ['test_config.py']
        }
        files_to_load = test_files.get(test_category)
        if files_to_load:
            for file_pattern in files_to_load:
                discovered_suite = loader.discover(start_dir=test_dir, pattern=file_pattern)
                suite.addTest(discovered_suite)
        else:
            print(f"Warning: Test category '{test_category}' not found. No tests will be run.")
            return


    if use_coverage:
        cov = Coverage(source=['src'])
        cov.start()

    runner = ColoredTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    if use_coverage:
        cov.stop()
        cov.save()
        print("\nCoverage Report:")
        cov.report(show_missing=True)

    # Exit with a non-zero status code if there were failures or errors
    if result.failures or result.errors:
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tests for the Psychological Records application.")
    parser.add_argument(
        '--category', 
        type=str, 
        default='all', 
        choices=['all', 'unit', 'integration', 'ui', 'layout', 'qss', 'config', 'comprehensive'],
        help="The category of tests to run."
    )
    parser.add_argument(
        '-v', '--verbosity',
        type=int,
        default=2,
        choices=[0, 1, 2],
        help="Verbosity level (0=quiet, 1=default, 2=verbose)."
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help="Enable code coverage reporting."
    )
    
    args = parser.parse_args()
    run_tests(args.category, args.verbosity, args.coverage)
