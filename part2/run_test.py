#!/usr/bin/env python3
"""Test runner for all tests"""
import unittest
import sys
import os

def run_tests():
    """Run all tests"""
    # Ajoute le chemin du projet au PYTHONPATH
    project_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_path)
    
    # Découvre et lance tous les tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_path, 'app/tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Lance les tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_tests()