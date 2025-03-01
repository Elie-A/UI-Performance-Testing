from functools import wraps
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from utils.perf_utils.performance_library import PerformanceLibrary
from typing import Optional, Dict

# Global instance of PerformanceLibrary
performance_library = PerformanceLibrary()

def performance_keyword(action_name: str):
    """Decorator to measure performance of a Robot Framework keyword."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
                # Use the decorator to wrap the keyword function
            return performance_library.measure_action_keyword(action_name)(func)(*args, **kwargs)
        return wrapper
    return decorator

@keyword("Start Performance Monitoring")
def start_performance_monitoring(test_name: str):
    """Start monitoring performance for a test."""
    performance_library.start_performance_monitoring(test_name)

@keyword("Measure Action")
def measure_action(action_name: str):
    """Measure an action during the test."""
    return performance_library.measure_action_keyword(action_name)

@keyword("Save Performance Metrics")
def save_performance_metrics():
    """Save all collected performance metrics to files."""
    performance_library.save_performance_metrics()

@keyword("Generate Performance Report")
def generate_performance_report(test_name: str) -> Dict:
    """Generate a performance report for a specific test."""
    return performance_library.generate_performance_report(test_name)

@keyword("Generate HTML Performance Report")
def generate_html_performance_report(suite_name: str):
    """Robot Framework keyword to generate an HTML performance report."""
    # Generate the HTML report by calling the function
    report_file = performance_library.generate_performance_html_report(suite_name)
    
    # Optionally log the file location
    from robot.libraries.BuiltIn import BuiltIn
    BuiltIn().log(f"HTML Performance Report saved to {report_file}")
    return report_file

@keyword("Enable Performance Monitoring")
def enable_performance_monitoring(enable: bool):
    """Enable or disable performance monitoring."""
    performance_library.monitor.enable_monitoring(enable)

@keyword("Measure Keyword")
def measure_keyword(keyword_name: str, *args, **kwargs):
    """Measure the performance of a Robot Framework keyword."""
    decorated_keyword = performance_keyword(keyword_name)(lambda: BuiltIn().run_keyword(keyword_name, *args, **kwargs))
    decorated_keyword()

@keyword("End Performance Monitoring")
def end_performance_monitoring(test_name: str):
    """End monitoring performance for a test."""
    performance_library.end_performance_monitoring(test_name)