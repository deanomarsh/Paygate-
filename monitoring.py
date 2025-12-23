"""
24/7 Monitoring and Alert System

Continuously monitors the payment gateway system and generates
alerts for issues, anomalies, and security concerns.
"""

from typing import List, Dict, Optional, Callable
from datetime import datetime, timedelta
from threading import Thread, Event
import time
import uuid
import logging

from core import Alert, PaymentTransaction, SecurityVulnerability


class MonitoringService:
    """24/7 monitoring service for the payment gateway"""
    
    def __init__(self):
        self.alerts: Dict[str, Alert] = {}
        self.metrics: Dict[str, List[float]] = {
            "transaction_count": [],
            "success_rate": [],
            "avg_processing_time": [],
            "error_count": []
        }
        self.thresholds = {
            "max_error_rate": 0.05,  # 5%
            "min_success_rate": 0.95,  # 95%
            "max_avg_processing_time": 5.0,  # 5 seconds
            "max_transaction_rate": 1000  # per minute
        }
        self.monitoring_active = False
        self.monitoring_thread = None
        self.stop_event = Event()
        self.logger = logging.getLogger(__name__)
        
    def start_monitoring(self):
        """Start 24/7 monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.stop_event.clear()
            self.monitoring_thread = Thread(target=self._monitoring_loop, daemon=False)
            self.monitoring_thread.start()
            self.logger.info("24/7 monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        if self.monitoring_active:
            self.monitoring_active = False
            self.stop_event.set()
            if self.monitoring_thread:
                self.monitoring_thread.join(timeout=5)
            self.logger.info("Monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while not self.stop_event.is_set():
            try:
                self._check_system_health()
                self._check_metrics()
                self._check_anomalies()
                time.sleep(10)  # Check every 10 seconds
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(10)
    
    def _check_system_health(self):
        """Check overall system health"""
        # Simulate system health checks
        # In a real system, this would check database connections,
        # service availability, disk space, memory, etc.
        pass
    
    def _check_metrics(self):
        """Check if metrics are within acceptable thresholds"""
        # Check success rate
        if self.metrics["success_rate"]:
            current_success_rate = self.metrics["success_rate"][-1]
            if current_success_rate < self.thresholds["min_success_rate"]:
                self.create_alert(
                    severity="high",
                    message=f"Success rate below threshold: {current_success_rate:.2%}",
                    component="metrics"
                )
        
        # Check processing time
        if self.metrics["avg_processing_time"]:
            current_avg_time = self.metrics["avg_processing_time"][-1]
            if current_avg_time > self.thresholds["max_avg_processing_time"]:
                self.create_alert(
                    severity="medium",
                    message=f"Average processing time high: {current_avg_time:.2f}s",
                    component="performance"
                )
    
    def _check_anomalies(self):
        """Check for anomalies in transaction patterns"""
        # Simple anomaly detection based on transaction count
        if len(self.metrics["transaction_count"]) >= 10:
            recent = self.metrics["transaction_count"][-10:]
            avg = sum(recent) / len(recent)
            current = recent[-1]
            
            # Alert if current is 3x average (spike detection)
            if current > avg * 3:
                self.create_alert(
                    severity="high",
                    message=f"Transaction spike detected: {current} (avg: {avg:.0f})",
                    component="anomaly_detection"
                )
    
    def create_alert(self, severity: str, message: str, component: str) -> Alert:
        """
        Create a new alert
        
        Args:
            severity: Alert severity (low, medium, high, critical)
            message: Alert message
            component: Affected component
            
        Returns:
            Created Alert object
        """
        alert_id = str(uuid.uuid4())
        alert = Alert(
            alert_id=alert_id,
            severity=severity,
            message=message,
            component=component
        )
        self.alerts[alert_id] = alert
        self.logger.warning(f"Alert created [{severity}]: {message}")
        return alert
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """
        Acknowledge an alert
        
        Args:
            alert_id: Alert identifier
            
        Returns:
            True if acknowledged successfully
        """
        if alert_id in self.alerts:
            self.alerts[alert_id].acknowledged = True
            self.logger.info(f"Alert acknowledged: {alert_id}")
            return True
        return False
    
    def record_transaction_metric(self, success: bool, processing_time: float):
        """
        Record transaction metrics
        
        Args:
            success: Whether transaction succeeded
            processing_time: Time taken to process
        """
        # Record transaction count
        self.metrics["transaction_count"].append(1)
        
        # Keep only last 1000 data points
        if len(self.metrics["transaction_count"]) > 1000:
            self.metrics["transaction_count"].pop(0)
        
        # Record success rate
        if success:
            self.metrics["success_rate"].append(1.0)
        else:
            self.metrics["success_rate"].append(0.0)
            self.metrics["error_count"].append(1)
        
        if len(self.metrics["success_rate"]) > 1000:
            self.metrics["success_rate"].pop(0)
        
        # Record processing time
        self.metrics["avg_processing_time"].append(processing_time)
        if len(self.metrics["avg_processing_time"]) > 1000:
            self.metrics["avg_processing_time"].pop(0)
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all unacknowledged alerts"""
        return [alert for alert in self.alerts.values() if not alert.acknowledged]
    
    def get_critical_alerts(self) -> List[Alert]:
        """Get critical unacknowledged alerts"""
        return [alert for alert in self.alerts.values() 
                if alert.severity == "critical" and not alert.acknowledged]
    
    def get_metrics_summary(self) -> Dict:
        """Get summary of current metrics"""
        summary = {}
        
        for metric_name, values in self.metrics.items():
            if values:
                summary[metric_name] = {
                    "current": values[-1],
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "count": len(values)
                }
            else:
                summary[metric_name] = {
                    "current": 0,
                    "average": 0,
                    "min": 0,
                    "max": 0,
                    "count": 0
                }
        
        return summary
    
    def check_uptime(self) -> Dict:
        """
        Check system uptime and availability
        
        Returns:
            Dictionary with uptime statistics
        """
        # Calculate uptime based on success rate
        if self.metrics["success_rate"]:
            success_rate = sum(self.metrics["success_rate"]) / len(self.metrics["success_rate"])
            uptime_percentage = success_rate * 100
        else:
            uptime_percentage = 100.0
        
        return {
            "uptime_percentage": uptime_percentage,
            "monitoring_active": self.monitoring_active,
            "total_transactions": sum(self.metrics["transaction_count"]),
            "total_errors": sum(self.metrics["error_count"])
        }
