#!/usr/bin/env python3
"""
Process monitoring script for long-running verification tasks.
Monitors system resources and provides alerts/restart capabilities.
"""

import time
import psutil
import logging
import signal
import sys
import os
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/process_monitor.log'),
        logging.StreamHandler()
    ]
)

class ProcessMonitor:
    def __init__(self, check_interval=60, memory_threshold=85, cpu_threshold=90):
        """
        Initialize process monitor.
        
        Args:
            check_interval: How often to check resources (seconds)
            memory_threshold: Memory usage threshold to trigger alerts (%)
            cpu_threshold: CPU usage threshold to trigger alerts (%)
        """
        self.check_interval = check_interval
        self.memory_threshold = memory_threshold
        self.cpu_threshold = cpu_threshold
        self.start_time = datetime.now()
        self.alerts_sent = []
        
    def get_system_stats(self):
        """Get current system resource statistics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': disk.percent,
                'load_avg': os.getloadavg() if hasattr(os, 'getloadavg') else None,
                'uptime': datetime.now() - self.start_time
            }
        except Exception as e:
            logging.error(f"Error getting system stats: {e}")
            return None
    
    def check_docker_container(self):
        """Check if we're running in a Docker container and get container stats."""
        try:
            # Check if running in Docker
            if os.path.exists('/.dockerenv'):
                logging.info("Running in Docker container")
                return True
            return False
        except Exception as e:
            logging.error(f"Error checking Docker status: {e}")
            return False
    
    def log_resource_usage(self, stats):
        """Log current resource usage."""
        if not stats:
            return
            
        logging.info(f"Resource Usage - CPU: {stats['cpu_percent']:.1f}%, "
                    f"Memory: {stats['memory_percent']:.1f}%, "
                    f"Available Memory: {stats['memory_available_gb']:.1f}GB, "
                    f"Disk: {stats['disk_percent']:.1f}%, "
                    f"Uptime: {stats['uptime']}")
    
    def check_thresholds(self, stats):
        """Check if resource usage exceeds thresholds and send alerts."""
        if not stats:
            return
            
        alerts = []
        
        if stats['cpu_percent'] > self.cpu_threshold:
            alert = f"HIGH CPU USAGE: {stats['cpu_percent']:.1f}%"
            alerts.append(alert)
            
        if stats['memory_percent'] > self.memory_threshold:
            alert = f"HIGH MEMORY USAGE: {stats['memory_percent']:.1f}%"
            alerts.append(alert)
            
        if stats['disk_percent'] > 90:
            alert = f"HIGH DISK USAGE: {stats['disk_percent']:.1f}%"
            alerts.append(alert)
            
        # Log unique alerts (avoid spam)
        for alert in alerts:
            if alert not in self.alerts_sent:
                logging.warning(alert)
                self.alerts_sent.append(alert)
                
        # Clear old alerts after 1 hour
        if len(self.alerts_sent) > 10:
            self.alerts_sent = self.alerts_sent[-5:]
    
    def find_python_processes(self):
        """Find running Python verification processes."""
        python_processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_percent', 'cpu_percent']):
                try:
                    if proc.info['name'] in ['python', 'python3'] and proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if any(script in cmdline for script in ['run_assistants_parallel.py', 'func_by_func_verifier.py']):
                            python_processes.append({
                                'pid': proc.info['pid'],
                                'cmdline': cmdline,
                                'memory_percent': proc.info['memory_percent'],
                                'cpu_percent': proc.info['cpu_percent']
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logging.error(f"Error finding Python processes: {e}")
            
        return python_processes
    
    def monitor_processes(self, max_runtime_hours=8):
        """Monitor verification processes and system resources."""
        logging.info(f"Starting process monitor - checking every {self.check_interval}s")
        logging.info(f"Thresholds - CPU: {self.cpu_threshold}%, Memory: {self.memory_threshold}%")
        
        is_docker = self.check_docker_container()
        
        try:
            while True:
                stats = self.get_system_stats()
                if stats:
                    self.log_resource_usage(stats)
                    self.check_thresholds(stats)
                    
                    # Check if we've been running too long
                    runtime_hours = stats['uptime'].total_seconds() / 3600
                    if runtime_hours > max_runtime_hours:
                        logging.warning(f"Process has been running for {runtime_hours:.1f} hours. "
                                      f"Consider restarting to prevent resource leaks.")
                
                # Check running verification processes
                python_procs = self.find_python_processes()
                if python_procs:
                    logging.info(f"Found {len(python_procs)} verification processes running")
                    for proc in python_procs:
                        logging.info(f"PID {proc['pid']}: Memory {proc['memory_percent']:.1f}%, "
                                   f"CPU {proc['cpu_percent']:.1f}%")
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logging.info("Process monitor stopped by user")
        except Exception as e:
            logging.error(f"Error in monitor loop: {e}")

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logging.info(f"Received signal {signum}, shutting down monitor...")
    sys.exit(0)

def main():
    """Main entry point for the process monitor."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start monitor
    monitor = ProcessMonitor(
        check_interval=30,  # Check every 30 seconds
        memory_threshold=80,  # Alert at 80% memory usage
        cpu_threshold=85      # Alert at 85% CPU usage
    )
    
    monitor.monitor_processes(max_runtime_hours=6)

if __name__ == "__main__":
    main() 