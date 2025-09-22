# Convenience runner to launch the app without needing to run as a module.
# Usage: python run.py

import sys
from src.simple_main import main

if __name__ == "__main__":
    sys.exit(main())
