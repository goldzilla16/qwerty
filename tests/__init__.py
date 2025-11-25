"""
Test package for Task Management API
This file makes the tests directory a Python package
"""

import sys
import os

# Add parent directory to path so tests can import app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
