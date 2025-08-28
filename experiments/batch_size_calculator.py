#!/usr/bin/env python3
"""
Batch Size Calculator for Parallel Contract Verification

This utility helps determine optimal batch sizes based on system resources,
task characteristics, and container constraints.
"""

import psutil
import os
import argparse
from typing import Dict, Any


def get_system_info() -> Dict[str, Any]:
    """Get current system resource information"""
    return {
        'cpu_count': os.cpu_count() or 4,
        'memory_gb': psutil.virtual_memory().total / (1024**3),
        'available_memory_gb': psutil.virtual_memory().available / (1024**3),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent
    }


def calculate_optimal_workers(memory_gb: float, cpu_count: int, is_container: bool = True) -> int:
    """Calculate optimal number of workers based on resources"""
    if is_container:
        # Container-optimized worker count
        if memory_gb < 12:
            return min(2, cpu_count // 2)
        elif memory_gb < 16:
            return min(3, cpu_count // 2)
        else:
            return min(4, cpu_count // 2)
    else:
        # Native system worker count
        if memory_gb < 8:
            return min(2, cpu_count)
        elif memory_gb < 16:
            return min(4, cpu_count)
        else:
            return min(6, cpu_count)


def calculate_batch_size(
    max_workers: int,
    executor_type: str,
    task_complexity: str,
    verification_mode: str,
    memory_gb: float,
    is_container: bool = True
) -> Dict[str, Any]:
    """
    Calculate optimal batch size based on multiple factors
    
    Args:
        max_workers: Number of parallel workers
        executor_type: 'thread' or 'process'
        task_complexity: 'light', 'medium', 'heavy'
        verification_mode: 'func_by_func' or 'entire_contract'
        memory_gb: Available memory in GB
        is_container: Whether running in container
    
    Returns:
        Dictionary with recommended batch sizes and reasoning
    """
    
    # Base batch size calculation
    if executor_type == 'thread':
        base_batch_size = max_workers
    else:  # process
        base_batch_size = max(1, max_workers // 2)
    
    # Adjust for task complexity
    complexity_multipliers = {
        'light': 1.5,    # Can handle more tasks
        'medium': 1.0,   # Standard
        'heavy': 0.5     # Need fewer concurrent tasks
    }
    
    complexity_adjusted = int(base_batch_size * complexity_multipliers.get(task_complexity, 1.0))
    
    # Adjust for verification mode
    if verification_mode == 'entire_contract':
        # Entire contract verification is more resource intensive
        mode_adjusted = max(1, complexity_adjusted // 2)
    else:  # func_by_func
        mode_adjusted = complexity_adjusted
    
    # Apply container constraints
    if is_container:
        if memory_gb < 12:
            container_adjusted = min(mode_adjusted, 2)
        elif memory_gb < 16:
            container_adjusted = min(mode_adjusted, 3)
        else:
            container_adjusted = min(mode_adjusted, 4)
    else:
        container_adjusted = mode_adjusted
    
    # Final safety bounds
    recommended_batch_size = max(1, min(container_adjusted, max_workers * 2))
    
    # Alternative recommendations
    conservative_batch_size = max(1, recommended_batch_size // 2)
    aggressive_batch_size = min(recommended_batch_size * 2, max_workers * 3)
    
    return {
        'recommended': recommended_batch_size,
        'conservative': conservative_batch_size,
        'aggressive': aggressive_batch_size,
        'reasoning': {
            'base_batch_size': base_batch_size,
            'complexity_adjusted': complexity_adjusted,
            'mode_adjusted': mode_adjusted,
            'container_adjusted': container_adjusted,
            'executor_type': executor_type,
            'task_complexity': task_complexity,
            'verification_mode': verification_mode,
            'memory_constraint': f"{memory_gb:.1f}GB",
            'is_container': is_container
        }
    }


def get_recommendations(
    verification_mode: str = 'func_by_func',
    task_complexity: str = 'medium',
    executor_type: str = 'thread',
    is_container: bool = True
) -> None:
    """Generate batch size recommendations for current system"""
    
    print("=" * 60)
    print("🚀 BATCH SIZE CALCULATOR FOR CONTRACT VERIFICATION")
    print("=" * 60)
    
    # Get system info
    system_info = get_system_info()
    print(f"\n📊 SYSTEM RESOURCES:")
    print(f"   CPU Cores: {system_info['cpu_count']}")
    print(f"   Total Memory: {system_info['memory_gb']:.1f} GB")
    print(f"   Available Memory: {system_info['available_memory_gb']:.1f} GB")
    print(f"   Current CPU Usage: {system_info['cpu_percent']:.1f}%")
    print(f"   Current Memory Usage: {system_info['memory_percent']:.1f}%")
    
    # Calculate optimal workers
    optimal_workers = calculate_optimal_workers(
        system_info['memory_gb'], 
        system_info['cpu_count'], 
        is_container
    )
    
    print(f"\n⚙️  CONFIGURATION:")
    print(f"   Environment: {'Container' if is_container else 'Native'}")
    print(f"   Verification Mode: {verification_mode}")
    print(f"   Task Complexity: {task_complexity}")
    print(f"   Executor Type: {executor_type}")
    print(f"   Recommended Workers: {optimal_workers}")
    
    # Calculate batch sizes
    batch_info = calculate_batch_size(
        optimal_workers,
        executor_type,
        task_complexity,
        verification_mode,
        system_info['memory_gb'],
        is_container
    )
    
    print(f"\n🎯 BATCH SIZE RECOMMENDATIONS:")
    print(f"   Conservative: {batch_info['conservative']:2d}  (safest, slower)")
    print(f"   Recommended:  {batch_info['recommended']:2d}  (balanced)")
    print(f"   Aggressive:   {batch_info['aggressive']:2d}  (faster, riskier)")
    
    print(f"\n💡 COMMAND EXAMPLES:")
    print(f"   # Conservative approach")
    print(f"   python run_assistants_parallel.py \\")
    print(f"     --max-workers {optimal_workers} \\")
    print(f"     --batch-size {batch_info['conservative']} \\")
    print(f"     --executor-type {executor_type}")
    
    print(f"\n   # Recommended approach") 
    print(f"   python run_assistants_parallel.py \\")
    print(f"     --max-workers {optimal_workers} \\")
    print(f"     --batch-size {batch_info['recommended']} \\")
    print(f"     --executor-type {executor_type}")
    
    print(f"\n   # Aggressive approach (monitor resources closely)")
    print(f"   python run_assistants_parallel.py \\")
    print(f"     --max-workers {optimal_workers} \\")
    print(f"     --batch-size {batch_info['aggressive']} \\")
    print(f"     --executor-type {executor_type}")
    
    # Warning conditions
    print(f"\n⚠️  WARNINGS:")
    if system_info['memory_percent'] > 80:
        print(f"   • High memory usage ({system_info['memory_percent']:.1f}%) - use conservative batch size")
    if system_info['cpu_percent'] > 80:
        print(f"   • High CPU usage ({system_info['cpu_percent']:.1f}%) - reduce workers/batch size")
    if system_info['available_memory_gb'] < 4:
        print(f"   • Low available memory ({system_info['available_memory_gb']:.1f}GB) - use batch_size=1")
    if not is_container and system_info['memory_gb'] < 16:
        print(f"   • Limited system memory - consider using container limits")
    
    print(f"\n📋 BATCH SIZE CALCULATION BREAKDOWN:")
    reasoning = batch_info['reasoning']
    print(f"   Base (executor):     {reasoning['base_batch_size']}")
    print(f"   Complexity adjust:   {reasoning['complexity_adjusted']}")
    print(f"   Mode adjust:         {reasoning['mode_adjusted']}")
    print(f"   Container adjust:    {reasoning['container_adjusted']}")
    print(f"   Final recommended:   {batch_info['recommended']}")


def main():
    parser = argparse.ArgumentParser(description='Calculate optimal batch sizes for contract verification')
    parser.add_argument('--mode', type=str, default='func_by_func',
                        choices=['func_by_func', 'entire_contract'],
                        help='Verification mode')
    parser.add_argument('--complexity', type=str, default='medium',
                        choices=['light', 'medium', 'heavy'],
                        help='Task complexity level')
    parser.add_argument('--executor', type=str, default='thread',
                        choices=['thread', 'process'],
                        help='Executor type')
    parser.add_argument('--container', action='store_true', default=True,
                        help='Running in container (default: True)')
    parser.add_argument('--native', action='store_true',
                        help='Running on native system')
    
    args = parser.parse_args()
    
    is_container = not args.native  # Default to container unless --native specified
    
    get_recommendations(
        verification_mode=args.mode,
        task_complexity=args.complexity,
        executor_type=args.executor,
        is_container=is_container
    )


if __name__ == "__main__":
    main() 