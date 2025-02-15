import time
import json
import os
import platform
import psutil
from robot import version
from datetime import datetime
from typing import Optional, Dict
from threading import Lock, local
from contextlib import contextmanager
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from jinja2 import Environment, FileSystemLoader

class PerformanceMonitor:
    """Singleton class for managing performance monitoring."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._init_monitor()
        return cls._instance

    def _init_monitor(self):
        self._metrics = {}
        self._local = local()
        self._lock = Lock()
        self._is_performance_monitoring_enabled = False

    def enable_monitoring(self, enable: bool):
        """Enable or disable performance monitoring"""
        self._is_performance_monitoring_enabled = enable

    def _get_results_dir(self) -> str:
        """Get results directory from Robot Framework variables."""
        try:
            results_dir = BuiltIn().get_variable_value("${RESULTS_DIR}")
            if results_dir:
                return results_dir
        except Exception:
            pass  # Fall back to default if variable is not set

        # Default results directory
        return os.path.join(os.getcwd(), "results")

    def _get_system_info(self) -> Dict:
        """Retrieve system information."""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "cpu": f"{psutil.cpu_percent(interval=1)}%",  # Get CPU usage as a percentage
            "memory": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",  # Total memory in GB
        }

    def _get_execution_context(self) -> Dict:
        """Retrieve execution context information."""
        try:
            browser_type = BuiltIn().get_variable_value("${BROWSER_TYPE}", "chromium")
            headless_mode = BuiltIn().get_variable_value("${HEADLESS_MODE}", "False")
        except:
            browser_type = "chromium"
            headless_mode = "False"

        return {
            "robot_version": version.get_version(),
            "python_version": platform.python_version(),
            "browser": browser_type,
            "headless_mode": headless_mode.lower() == "true",
        }

    def _ensure_test_info(self):
        """Ensure test info is initialized for the current thread."""
        if not hasattr(self._local, 'test_info'):
            self._local.test_info = {
                'test_name': '',
                'test_start_time': None,
                'step_order': 0,
            }

    def start_test_session(self, test_name: str):
        """Start a new test session."""
        if not self._is_performance_monitoring_enabled:
            logger.info(f"Performance monitoring is disabled for tests {test_name}")
            return
        self._ensure_test_info()
        self._local.test_info['test_name'] = test_name
        self._local.test_info['test_start_time'] = datetime.now()

        with self._lock:
            if test_name not in self._metrics:
                system_info = self._get_system_info()
                logger.info(f"System Info: {json.dumps(system_info, indent=2)}")
                execution_context = self._get_execution_context()
                logger.info(f"Execution Context: {json.dumps(execution_context, indent=2)}")

                self._metrics[test_name] = {
                    "test_case_id": test_name,
                    "start_time": datetime.now().isoformat(),
                    "actions": [],
                    "system_info": system_info,
                    "execution_context": execution_context,
                }
                print("self._metrics[test_name]:", json.dumps(self._metrics[test_name], indent=4))

    @contextmanager
    def measure_action(self, action_name: str, user_id: Optional[str] = None, params: Optional[Dict] = None):
        """Context manager to measure action duration."""
        if not self._is_performance_monitoring_enabled:
            yield # Skip monitoring
            return
        self._ensure_test_info()
        self._local.test_info['step_order'] += 1
        step_order = self._local.test_info['step_order']

        # Log when the action is being measured
        logger.info(f"Measuring action: {action_name} - Step Order: {step_order}")
        start_time = time.perf_counter()
        try:
            yield
        finally:
            end_time = time.perf_counter()
            duration = end_time - start_time

            action_data = {
                "action": action_name,
                "start_time": datetime.now().isoformat(),
                "duration": duration,
                "parameters": params or {},
                "step_order": step_order,
                "cpu_usage": f"{psutil.cpu_percent()}%",
                "memory_usage": f"{psutil.virtual_memory().used / (1024 ** 2):.2f} MB",
            }

            # Lock to ensure thread-safety while modifying the shared metrics
            with self._lock:
                self._metrics[self._local.test_info['test_name']]["actions"].append(action_data)

            # Log action details for debugging
            logger.info(f"Action recorded: {json.dumps(action_data, indent=2)}")

            # After recording the action, update the summary of actions
            self._update_summary(self._local.test_info['test_name'])

    def _update_summary(self, test_name: str):
        """Update the action summary after an action is recorded."""
        if not self._is_performance_monitoring_enabled:
            logger.info(f"Performance monitoring is disabled. Skipping summary update for test: {test_name}.")
            return
    
        if test_name in self._metrics:
            metrics = self._metrics[test_name]
            actions = metrics.get("actions", [])

            # Reset the summary to ensure no cumulative additions
            summary = {}

            for action in actions:
                action_name = action["action"]
                if action_name not in summary:
                    summary[action_name] = {
                        "count": 0,
                        "total_duration": 0,
                        "min_duration": float('inf'),
                        "max_duration": 0,
                    }

                summary[action_name]["count"] += 1
                summary[action_name]["total_duration"] += action["duration"]
                summary[action_name]["min_duration"] = min(
                    summary[action_name]["min_duration"], action["duration"]
                )
                summary[action_name]["max_duration"] = max(
                    summary[action_name]["max_duration"], action["duration"]
                )

            # Calculate average duration
            for action_name, data in summary.items():
                data["avg_duration"] = data["total_duration"] / data["count"]

            # Update metrics summary
            metrics["summary"] = summary


    def save_metrics(self):
        """Save all metrics to files and ensure summary is populated."""
        if not self._is_performance_monitoring_enabled:
            logger.info("Performance monitoring is disabled. No metrics to save.")
            return
        
        results_dir = self._get_results_dir()
        os.makedirs(results_dir, exist_ok=True)
        logger.info(f"Saving metrics to {results_dir}")
        
        suite_name = BuiltIn().get_variable_value("${SUITE_NAME}", "default_suite")
        logger.info(f"Suite name: {suite_name}")
        
        for test_name, metrics in self._metrics.items():
            # Ensure the summary is up-to-date before saving
            self._update_summary(test_name)
            
            logger.info(f"Saving metrics for test: {test_name}")
            filename = os.path.join(results_dir, f"{suite_name}_metrics.json")
            with open(filename, 'w') as f:
                json.dump(metrics, f, indent=2)
                logger.info(f"Metrics saved to {filename}")


    def generate_report(self, test_name: str) -> Dict:
        """Generate performance report for a specific test."""
        if not self._is_performance_monitoring_enabled:
            logger.info("Performance monitoring is disabled. No report generated.")
            return {}
        
        if test_name not in self._metrics:
            return {}

        metrics = self._metrics[test_name]
        actions_summary = {}

        # Summarize actions performance
        for action in metrics["actions"]:
            action_name = action["action"]
            if action_name not in actions_summary:
                actions_summary[action_name] = {
                    "count": 0,
                    "total_duration": 0,
                    "min_duration": float('inf'),
                    "max_duration": 0,
                }

            actions_summary[action_name]["count"] += 1
            actions_summary[action_name]["total_duration"] += action["duration"]
            actions_summary[action_name]["min_duration"] = min(
                actions_summary[action_name]["min_duration"], action["duration"]
            )
            actions_summary[action_name]["max_duration"] = max(
                actions_summary[action_name]["max_duration"], action["duration"]
            )

        for action_name, summary in actions_summary.items():
            summary["avg_duration"] = summary["total_duration"] / summary["count"]

        # Include system and execution context info
        performance_report = {
            "test_case_id": test_name,
            "start_time": metrics["start_time"],
            "system_info": metrics["system_info"],  # Ensure this includes OS, CPU, and Memory
            "execution_context": metrics["execution_context"],
            "summary": actions_summary,
            "current_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Current time for the report
            "actions": metrics["actions"]
        }

        return performance_report

    def generate_html_report(self, suite_name: str):
        if not self._is_performance_monitoring_enabled:
            logger.info("Performance monitoring is disabled. No HTML report generated.")
            return None
        
        """Generate an HTML report based on the metrics collected and the template."""
        # Define the template directory and ensure it exists
        template_dir = os.path.join(os.getcwd(), 'templates')  # Default 'templates' folder
        if not os.path.isdir(template_dir):
            raise FileNotFoundError(f"Template directory '{template_dir}' does not exist.")

        # Initialize Jinja2 environment
        env = Environment(loader=FileSystemLoader(template_dir))

        # Load the HTML template
        try:
            template = env.get_template('performance_report_template.html')
        except Exception as e:
            raise FileNotFoundError(f"Template 'performance_report_template.html' not found in '{template_dir}'.") from e

        # Load metrics from the saved JSON file
        results_dir = self._get_results_dir()
        metrics_file = os.path.join(results_dir, f"{suite_name}_metrics.json")
        if not os.path.exists(metrics_file):
            raise FileNotFoundError(f"Metrics file '{metrics_file}' not found.")

        with open(metrics_file, 'r') as f:
            metrics = json.load(f)
            
        logger.info(f"Loaded metrics for {suite_name}: {json.dumps(metrics, indent=2)}")

        # Prepare data for rendering the template
        report_data = {
            "test_case_id": metrics.get("test_case_id", "N/A"),
            "start_time": metrics.get("start_time", "N/A"),
            "system_info": metrics.get("system_info", {}),
            "execution_context": metrics.get("execution_context", {}),
            "summary": metrics.get("summary", {}),
            "actions": metrics.get("actions", []),
            "current_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Add the current timestamp
        }

        # Render the template
        try:
            html_content = template.render(report_data)
        except Exception as e:
            logger.error("Error rendering HTML template:", exc_info=e)
            raise RuntimeError("Failed to render HTML report.") from e

        # Save the generated HTML report
        report_file = os.path.join(results_dir, f"{suite_name}_performance_report.html")
        with open(report_file, 'w') as f:
            f.write(html_content)

        # Log the report location
        logger.info(f"Performance report saved to {report_file}")
        return report_file

