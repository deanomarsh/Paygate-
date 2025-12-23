"""
Payment Gateway Analysis System - Main Integration

Integrates all components of the payment gateway system:
- Payment flow control
- Vulnerability scanning
- Bug detection and automated fixes
- 24/7 monitoring and alerts
- Self-learning AI
"""

from typing import Optional, Dict, List
import logging
from datetime import datetime

from core import PaymentTransaction, PaymentStatus
from payment_flow import PaymentFlowController
from vulnerability_scanner import VulnerabilityScanner
from bug_detector import AutomatedBugFixer
from monitoring import MonitoringService
from ai_learning import SelfLearningAI


class PaymentGateway:
    """
    Main Payment Gateway Analysis System
    
    Provides comprehensive payment processing with:
    - Automated security scanning
    - Bug detection and fixes
    - Real-time monitoring
    - AI-powered fraud detection
    - Zero-downtime architecture
    """
    
    def __init__(self):
        # Initialize all components
        self.payment_controller = PaymentFlowController()
        self.vulnerability_scanner = VulnerabilityScanner()
        self.bug_fixer = AutomatedBugFixer()
        self.monitoring_service = MonitoringService()
        self.ai_system = SelfLearningAI()
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        self._configure_logging()
        
        # Start 24/7 monitoring
        self.monitoring_service.start_monitoring()
        self.logger.info("Payment Gateway Analysis System initialized")
    
    def _configure_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def process_payment(
        self,
        amount: float,
        currency: str,
        merchant_id: str,
        customer_id: str,
        payment_method: str,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Process a payment with comprehensive analysis and protection
        
        Args:
            amount: Payment amount
            currency: Currency code
            merchant_id: Merchant identifier
            customer_id: Customer identifier
            payment_method: Payment method
            metadata: Additional metadata
            
        Returns:
            Dictionary with processing results
        """
        start_time = datetime.now()
        
        try:
            # Step 1: Initiate payment
            transaction = self.payment_controller.initiate_payment(
                amount=amount,
                currency=currency,
                merchant_id=merchant_id,
                customer_id=customer_id,
                payment_method=payment_method,
                metadata=metadata
            )
            
            # Step 2: Scan for vulnerabilities
            vulnerabilities = self.vulnerability_scanner.scan_transaction(transaction)
            
            if vulnerabilities:
                critical_vulns = [v for v in vulnerabilities if v.level.value == "critical"]
                if critical_vulns:
                    transaction.status = PaymentStatus.FLAGGED
                    self.monitoring_service.create_alert(
                        severity="critical",
                        message=f"Critical vulnerabilities detected in transaction {transaction.transaction_id}",
                        component="security"
                    )
                    return self._build_response(transaction, success=False, 
                                               message="Transaction blocked due to security concerns",
                                               vulnerabilities=vulnerabilities)
            
            # Step 3: Detect and fix bugs automatically
            bugs_detected = self.bug_fixer.detect_bugs(transaction)
            if bugs_detected:
                fixes_applied = self.bug_fixer.apply_fixes(transaction)
                self.logger.info(f"Applied {fixes_applied} automated fixes to transaction {transaction.transaction_id}")
            
            # Step 4: AI-powered fraud analysis
            ai_analysis = self.ai_system.analyze_transaction(transaction)
            
            if ai_analysis["is_likely_fraud"]:
                transaction.status = PaymentStatus.FLAGGED
                self.monitoring_service.create_alert(
                    severity="high",
                    message=f"Potential fraud detected: {transaction.transaction_id} (score: {ai_analysis['fraud_score']:.2f})",
                    component="fraud_detection"
                )
                return self._build_response(transaction, success=False,
                                           message="Transaction flagged for review",
                                           ai_analysis=ai_analysis)
            
            # Step 5: Process payment
            success = self.payment_controller.process_payment(transaction.transaction_id)
            
            # Step 6: Learn from transaction (if successful)
            if success:
                self.ai_system.learn_from_transaction(transaction)
            
            # Step 7: Record metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            self.monitoring_service.record_transaction_metric(success, processing_time)
            
            return self._build_response(
                transaction,
                success=success,
                message="Payment processed successfully" if success else "Payment failed",
                ai_analysis=ai_analysis,
                vulnerabilities=vulnerabilities,
                bugs_fixed=len(bugs_detected)
            )
            
        except Exception as e:
            self.logger.error(f"Error processing payment: {e}")
            self.monitoring_service.create_alert(
                severity="critical",
                message=f"Payment processing error: {str(e)}",
                component="payment_processing"
            )
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
    
    def _build_response(self, transaction: PaymentTransaction, success: bool,
                       message: str, **kwargs) -> Dict:
        """Build standardized response"""
        response = {
            "success": success,
            "message": message,
            "transaction_id": transaction.transaction_id,
            "status": transaction.status.value,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "timestamp": transaction.timestamp.isoformat()
        }
        
        # Add optional fields
        for key, value in kwargs.items():
            if value:
                response[key] = value
        
        return response
    
    def get_transaction_status(self, transaction_id: str) -> Optional[Dict]:
        """Get transaction status and details"""
        transaction = self.payment_controller.get_transaction(transaction_id)
        if not transaction:
            return None
        
        return {
            "transaction_id": transaction.transaction_id,
            "status": transaction.status.value,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "timestamp": transaction.timestamp.isoformat()
        }
    
    def get_system_health(self) -> Dict:
        """Get overall system health status"""
        return {
            "monitoring_active": self.monitoring_service.monitoring_active,
            "uptime": self.monitoring_service.check_uptime(),
            "active_alerts": len(self.monitoring_service.get_active_alerts()),
            "critical_alerts": len(self.monitoring_service.get_critical_alerts()),
            "metrics": self.monitoring_service.get_metrics_summary(),
            "unfixed_vulnerabilities": len(self.vulnerability_scanner.get_unfixed_vulnerabilities()),
            "unfixed_bugs": len(self.bug_fixer.get_unfixed_bugs())
        }
    
    def get_alerts(self, severity: Optional[str] = None) -> List[Dict]:
        """Get system alerts"""
        if severity == "critical":
            alerts = self.monitoring_service.get_critical_alerts()
        else:
            alerts = self.monitoring_service.get_active_alerts()
        
        return [alert.to_dict() for alert in alerts]
    
    def get_customer_insights(self, customer_id: str) -> Optional[Dict]:
        """Get AI-learned insights about a customer"""
        return self.ai_system.get_customer_insights(customer_id)
    
    def shutdown(self):
        """Graceful shutdown of the system"""
        self.logger.info("Shutting down Payment Gateway Analysis System")
        self.monitoring_service.stop_monitoring()
        self.logger.info("System shutdown complete")


# Example usage
if __name__ == "__main__":
    # Initialize the payment gateway
    gateway = PaymentGateway()
    
    # Process a sample payment
    result = gateway.process_payment(
        amount=99.99,
        currency="USD",
        merchant_id="merchant_123",
        customer_id="customer_456",
        payment_method="credit_card",
        metadata={
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0"
        }
    )
    
    print("Payment Result:", result)
    
    # Check system health
    health = gateway.get_system_health()
    print("\nSystem Health:", health)
    
    # Graceful shutdown
    gateway.shutdown()
