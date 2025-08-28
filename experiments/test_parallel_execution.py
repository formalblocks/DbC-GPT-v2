#!/usr/bin/env python3
"""
Test script for validating parallel execution improvements and path resolution fixes.
"""

import os
import sys
import logging
import argparse
from run_assistants_parallel import get_optimal_worker_count, monitor_resources

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_path_resolution():
    """Test that path resolution works from different directories"""
    print("Testing path resolution...")
    
    try:
        from func_by_func_verifier import SolcVerifyWrapper
        
        # Test base path detection
        base_path = SolcVerifyWrapper._get_base_path()
        print(f"✓ Base path detected: {base_path}")
        
        # Test template paths
        template_paths = SolcVerifyWrapper._get_template_paths()
        print(f"✓ Template paths: {list(template_paths.keys())}")
        
        # Test merge paths
        merge_paths = SolcVerifyWrapper._get_merge_paths()
        print(f"✓ Merge paths: {list(merge_paths.keys())}")
        
        # Verify files exist
        for erc_type, path in template_paths.items():
            if os.path.exists(path):
                print(f"✓ Template file exists: {erc_type} -> {path}")
            else:
                print(f"✗ Template file missing: {erc_type} -> {path}")
                return False
                
        return True
        
    except Exception as e:
        print(f"✗ Path resolution test failed: {e}")
        return False

def test_resource_monitoring():
    """Test resource monitoring functionality"""
    print("\nTesting resource monitoring...")
    
    try:
        # Test optimal worker count detection
        worker_count = get_optimal_worker_count()
        print(f"✓ Optimal worker count: {worker_count}")
        
        # Test resource monitoring
        cpu_percent, memory_percent = monitor_resources()
        print(f"✓ Current resources: CPU {cpu_percent}%, Memory {memory_percent}%")
        
        return True
        
    except Exception as e:
        print(f"✗ Resource monitoring test failed: {e}")
        return False

def test_imports():
    """Test that all required modules can be imported"""
    print("\nTesting imports...")
    
    try:
        import psutil
        print("✓ psutil imported successfully")
        
        from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
        print("✓ concurrent.futures imported successfully")
        
        from func_by_func_verifier import run_verification_process as run_func_verification
        print("✓ func_by_func_verifier imported successfully")
        
        from loop_contract_verifier import run_verification_process as run_loop_verification
        print("✓ loop_contract_verifier imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def run_mini_test():
    """Run a minimal verification test to ensure everything works"""
    print("\nRunning mini verification test...")
    
    try:
        from func_by_func_verifier import run_verification_process
        
        # Run with minimal parameters
        results = run_verification_process(
            requested_type="erc20",
            context_types=["erc721"],
            assistant_key="4o-mini",
            num_runs=1,
            max_iterations=1
        )
        
        if results:
            print("✓ Mini verification test completed successfully")
            return True
        else:
            print("✗ Mini verification test returned no results")
            return False
            
    except Exception as e:
        print(f"✗ Mini verification test failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test parallel execution improvements')
    parser.add_argument('--skip-verification', action='store_true',
                        help='Skip the actual verification test (faster)')
    
    args = parser.parse_args()
    
    print("=== Testing Parallel Execution Improvements ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {os.path.abspath(__file__)}")
    
    all_tests_passed = True
    
    # Run tests
    if not test_imports():
        all_tests_passed = False
        
    if not test_path_resolution():
        all_tests_passed = False
        
    if not test_resource_monitoring():
        all_tests_passed = False
        
    if not args.skip_verification:
        if not run_mini_test():
            all_tests_passed = False
    else:
        print("\nSkipping verification test (--skip-verification specified)")
    
    # Summary
    print("\n" + "="*50)
    if all_tests_passed:
        print("✓ All tests passed! The parallel execution improvements are working correctly.")
        print("\nRecommended usage:")
        print("  # For safer execution (default):")
        print("  python run_assistants_parallel.py --mode func_by_func --requested erc20 --executor-type thread")
        print("\n  # For faster execution (if you have sufficient resources):")
        print("  python run_assistants_parallel.py --mode func_by_func --requested erc20 --executor-type process --max-workers 2")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 