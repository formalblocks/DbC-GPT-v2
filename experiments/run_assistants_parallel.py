import argparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import logging
import os
import psutil
import time
import sys
from loop_contract_verifier import run_verification_process as run_loop_verification
from func_by_func_verifier import run_verification_process as run_func_by_func_verification
from itertools import combinations

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


ALL_ASSISTANTS = {
    "4o-mini",
    "erc-1155-001-5-16",
    "erc-20-001-5-16",
    "erc-721-001-5-16",
    "erc-20-721-001-5-16",
    "erc-20-1155-001-5-16",
    "erc-721-1155-001-5-16",
    "erc-20-721-1155-001-5-16"
}

ALL_CONTEXT_TYPES = ["erc20", "erc721", "erc1155"]

def get_optimal_worker_count():
    """More conservative worker count for containers"""
    try:
        cpu_count = os.cpu_count() or 4
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # More conservative for containers
        if memory_gb < 12:
            max_workers = min(2, cpu_count // 2)  # Even more conservative
        elif memory_gb < 16:
            max_workers = min(3, cpu_count // 2)
        else:
            max_workers = min(4, cpu_count // 2)
            
        logging.info(f"Container-optimized: {cpu_count} CPUs, {memory_gb:.1f}GB RAM, using {max_workers} workers")
        return max_workers
    except Exception as e:
        logging.warning(f"Could not determine resources: {e}, using 1 worker")
        return 1  # Very conservative fallback

def check_container_health():
    """Check if container is under stress"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        if memory_percent > 85:
            logging.warning(f"High memory usage: {memory_percent}% - pausing")
            time.sleep(30)  # Longer pause
            return False
        if cpu_percent > 95:
            logging.warning(f"High CPU usage: {cpu_percent}% - pausing")
            time.sleep(10)
            return False
        return True
    except:
        return True

def get_all_context_combinations():
    """Generate all possible combinations of context types"""
    all_combinations: list = [None]  # Start with no context
    # Generate all possible combinations of 1 to len(ALL_CONTEXT_TYPES) contexts
    for r in range(1, len(ALL_CONTEXT_TYPES) + 1):
        for combo in combinations(ALL_CONTEXT_TYPES, r):
            all_combinations.append(list(combo))
    return all_combinations

def run_single_assistant(assistant_key, requested_type, context_types, num_runs, max_iterations, mode):
    """Run verification process for a single assistant and context type"""
    try:
        # Enhanced resource monitoring before starting
        if not check_container_health():
            logging.warning(f"Container under stress before starting assistant: {assistant_key}")
            time.sleep(30)
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        logging.info(f"Starting verification for assistant: {assistant_key} with contexts: {context_types} (CPU: {cpu_percent}%, Memory: {memory_percent}%)")
        
        if mode == "entire_contract":
            results = run_loop_verification(
                requested_type=requested_type,
                context_types=context_types if context_types else [],
                assistant_key=assistant_key,
                num_runs=num_runs,
                max_iterations=max_iterations
            )
        else:  # func_by_func mode
            results = run_func_by_func_verification(
                requested_type=requested_type,
                context_types=context_types if context_types else [],
                assistant_key=assistant_key,
                num_runs=num_runs,
                max_iterations=max_iterations
            )
            
        # Force cleanup after completion
        import gc
        gc.collect()
            
        logging.info(f"Completed verification for assistant: {assistant_key} with contexts: {context_types}")
        return results
    except Exception as e:
        logging.error(f"Error running assistant {assistant_key} with contexts {context_types}: {str(e)}")
        # Force cleanup on error
        import gc
        gc.collect()
        return None

def main():
    parser = argparse.ArgumentParser(description='Run all assistants in parallel')
    parser.add_argument('--mode', type=str, required=True,
                        choices=['entire_contract', 'func_by_func'],
                        help='Verification mode: entire_contract or func_by_func')
    parser.add_argument('--requested', type=str, required=True, 
                         choices=['erc20', 'erc721', 'erc1155', 'ercx'],
                         help='The contract type to verify')
    parser.add_argument('--runs', type=int, default=10,
                        help='Number of verification runs per assistant')
    parser.add_argument('--max-iterations', type=int, default=10,
                        help='Maximum iterations per run')
    parser.add_argument('--max-workers', type=int, default=None,
                        help='Maximum number of parallel workers (auto-detect if not specified)')
    parser.add_argument('--executor-type', type=str, default='process',
                        choices=['thread', 'process'],
                        help='Type of executor to use: thread (safer for containers) or process (faster but more memory)')
    parser.add_argument('--assistants', type=str, default='all',
                        help='Comma-separated list of assistants to run, or "all" for all available assistants')
    parser.add_argument('--contexts', type=str, default='all',
                        help='Comma-separated list of context types to use, or "all" for all possible combinations, or empty for no context')
    parser.add_argument('--all-contexts-only', action='store_true',
                        help='Run only the combination with all specified context types together (ignores other combinations)')
    parser.add_argument('--batch-size', type=int, default=None,
                        help='Process tasks in batches to prevent resource exhaustion')
    parser.add_argument('--restart-after', type=int, default=50,
                        help='Restart container after this many runs to prevent resource leaks')
    
    args = parser.parse_args()

    # Constants for container health management
    RESTART_AFTER_RUNS = args.restart_after

    # Determine optimal worker count if not specified
    if args.max_workers is None:
        args.max_workers = get_optimal_worker_count()

    # Get list of assistants to run
    if args.assistants.lower() == 'all':
        assistants = ALL_ASSISTANTS
    else:
        assistants = [a.strip() for a in args.assistants.split(',') if a.strip()]
        # Validate that all requested assistants exist
        invalid_assistants = [a for a in assistants if a not in ALL_ASSISTANTS]
        if invalid_assistants:
            raise ValueError(f"Invalid assistant(s): {', '.join(invalid_assistants)}")

    # Get list of context combinations to run
    if args.contexts.lower() == 'all':
        context_combinations = get_all_context_combinations()
    elif args.contexts.strip() == '':
        context_combinations = [None]  # Use None to indicate empty context
    else:
        requested_contexts = [c.strip() for c in args.contexts.split(',') if c.strip()]
        # Validate that all requested context types exist
        invalid_contexts = [c for c in requested_contexts if c not in ALL_CONTEXT_TYPES]
        if invalid_contexts:
            raise ValueError(f"Invalid context type(s): {', '.join(invalid_contexts)}")
        # Generate all possible combinations of the requested contexts
        if args.all_contexts_only:
            # Only run the combination with all contexts together
            context_combinations = [requested_contexts]
        else:
            # Generate all possible combinations
            context_combinations = [None]  # Start with no context
            for r in range(1, len(requested_contexts) + 1):
                for combo in combinations(requested_contexts, r):
                    context_combinations.append(list(combo))  # type: ignore

    # Create all tasks
    all_tasks = [
        (assistant_key, args.requested, context_types, args.runs, args.max_iterations, args.mode)
        for assistant_key in assistants
        for context_types in context_combinations
    ]

    logging.info(f"Starting parallel execution with {args.max_workers} workers")
    logging.info(f"Running {args.runs} runs per assistant with max {args.max_iterations} iterations")
    logging.info(f"Mode: {args.mode}")
    logging.info(f"Requested type: {args.requested}")
    logging.info(f"Executor type: {args.executor_type}")
    logging.info(f"Total tasks: {len(all_tasks)}")
    logging.info(f"Assistants: {assistants}")
    logging.info(f"Context combinations: {context_combinations}")
    logging.info(f"Container will restart after {RESTART_AFTER_RUNS} runs")

    # Choose executor type - default to thread for containers
    ExecutorClass = ThreadPoolExecutor if args.executor_type == 'thread' else ProcessPoolExecutor
    
    # Process tasks in batches if specified
    if args.batch_size:
        batch_size = args.batch_size
    else:
        # More conservative batch size for containers
        batch_size = args.max_workers if args.executor_type == 'thread' else max(1, args.max_workers // 2)

    completed_tasks = 0
    total_tasks = len(all_tasks)

    # Process tasks in batches to prevent resource exhaustion
    for i in range(0, len(all_tasks), batch_size):
        # Check container health before starting each batch
        if not check_container_health():
            logging.info("System under stress, extending pause...")
            time.sleep(60)
        
        # Check for restart condition
        if completed_tasks > 0 and completed_tasks % RESTART_AFTER_RUNS == 0:
            logging.info(f"Scheduled restart after {completed_tasks} completed tasks")
            logging.info("Saving current state and exiting gracefully for container restart")
            # Force cleanup before restart
            import gc
            gc.collect()
            sys.exit(0)  # Let container orchestration restart
        
        batch = all_tasks[i:i + batch_size]
        logging.info(f"Processing batch {i//batch_size + 1}/{(len(all_tasks) + batch_size - 1)//batch_size} with {len(batch)} tasks")
        
        # Create executor for this batch
        with ExecutorClass(max_workers=args.max_workers) as executor:
            # Submit batch tasks
            future_to_run = {
                executor.submit(run_single_assistant, *task): task
                for task in batch
            }

            # Process completed futures as they finish
            for future in as_completed(future_to_run):
                task = future_to_run[future]
                assistant_key, requested_type, context_types, num_runs, max_iterations, mode = task
                completed_tasks += 1
                
                try:
                    results = future.result()
                    if results:
                        logging.info(f"[{completed_tasks}/{total_tasks}] Successfully completed assistant: {assistant_key} with contexts: {context_types}")
                    else:
                        logging.error(f"[{completed_tasks}/{total_tasks}] Failed to complete assistant: {assistant_key} with contexts: {context_types}")
                except Exception as e:
                    logging.error(f"[{completed_tasks}/{total_tasks}] Error processing assistant {assistant_key} with contexts {context_types}: {str(e)}")

        # Enhanced pause between batches with health check
        if i + batch_size < len(all_tasks):
            logging.info("Pausing between batches for system recovery...")
            time.sleep(5)  # Longer pause for containers
            
            # Force garbage collection between batches
            import gc
            gc.collect()
            
            # Additional health check
            if not check_container_health():
                logging.info("Additional recovery pause due to system stress...")
                time.sleep(30)

    logging.info("All parallel executions completed")
    
    # Final cleanup
    import gc
    gc.collect()

if __name__ == "__main__":
    main()