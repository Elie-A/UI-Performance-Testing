import functools
from typing import Optional
from robot.api import logger
from utils.perf_utils.performance_monitor import PerformanceMonitor

class PerformanceLibrary:
    """Robot Framework library for performance measurements"""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()

    def enabled_performance_monitoring(self, enable: bool):
        """Enable or disable performance monitoring"""
        self.monitor.enable_monitoring(enable)

    def start_performance_monitoring(self, test_name: str):
        """Start monitoring performance for a test"""
        self.monitor.start_test_session(test_name)
        
    def measure_action_keyword(self, action_name: str, user_id: Optional[str] = None, parameters: Optional[dict] = None):
        """Decorator for Robot Framework keywords to measure performance"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with self.monitor.measure_action(action_name, user_id, parameters):
                    return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def save_performance_metrics(self):
        """Save all collected metrics to file"""
        self.monitor.save_metrics()
        
    def generate_performance_report(self, test_name: str):
        """Generate and return performance report"""
        return self.monitor.generate_report(test_name)
        
    def generate_performance_html_report(self, test_name: str):
        """Generate and return performance report"""
        return self.monitor.generate_html_report(test_name)
