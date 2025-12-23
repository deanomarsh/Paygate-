"""
Unit tests for the Payment Gateway Analysis System
"""

import pytest
from datetime import datetime
import time

from core import PaymentTransaction, PaymentStatus, VulnerabilityLevel, SecurityVulnerability
from payment_flow import PaymentFlowController
from vulnerability_scanner import VulnerabilityScanner
from bug_detector import AutomatedBugFixer
from monitoring import MonitoringService
from ai_learning import SelfLearningAI
from gateway import PaymentGateway


class TestPaymentFlowController:
    """Tests for payment flow control"""
    
    def test_initiate_payment(self):
        """Test payment initiation"""
        controller = PaymentFlowController()
        
        transaction = controller.initiate_payment(
            amount=100.0,
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card"
        )
        
        assert transaction is not None
        assert transaction.amount == 100.0
        assert transaction.currency == "USD"
        assert transaction.status == PaymentStatus.PENDING
    
    def test_validate_payment_valid(self):
        """Test validation of valid payment"""
        controller = PaymentFlowController()
        
        transaction = controller.initiate_payment(
            amount=50.0,
            currency="EUR",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="paypal"
        )
        
        assert controller.validate_payment(transaction.transaction_id) is True
    
    def test_validate_payment_invalid_amount(self):
        """Test validation rejects invalid amount"""
        controller = PaymentFlowController()
        
        transaction = controller.initiate_payment(
            amount=-10.0,
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card"
        )
        
        assert controller.validate_payment(transaction.transaction_id) is False
    
    def test_process_payment(self):
        """Test payment processing"""
        controller = PaymentFlowController()
        
        transaction = controller.initiate_payment(
            amount=75.0,
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card"
        )
        
        result = controller.process_payment(transaction.transaction_id)
        assert result is True
        
        transaction = controller.get_transaction(transaction.transaction_id)
        assert transaction.status == PaymentStatus.COMPLETED
    
    def test_refund_payment(self):
        """Test payment refund"""
        controller = PaymentFlowController()
        
        transaction = controller.initiate_payment(
            amount=100.0,
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card"
        )
        
        controller.process_payment(transaction.transaction_id)
        result = controller.refund_payment(transaction.transaction_id)
        
        assert result is True
        transaction = controller.get_transaction(transaction.transaction_id)
        assert transaction.status == PaymentStatus.REFUNDED


class TestVulnerabilityScanner:
    """Tests for vulnerability scanning"""
    
    def test_sql_injection_detection(self):
        """Test SQL injection detection"""
        scanner = VulnerabilityScanner()
        
        malicious_input = "admin' OR '1'='1"
        vulnerabilities = scanner.scan_input(malicious_input, "username")
        
        assert len(vulnerabilities) > 0
        assert any(v.level == VulnerabilityLevel.CRITICAL for v in vulnerabilities)
    
    def test_xss_detection(self):
        """Test XSS detection"""
        scanner = VulnerabilityScanner()
        
        malicious_input = "<script>alert('XSS')</script>"
        vulnerabilities = scanner.scan_input(malicious_input, "comment")
        
        assert len(vulnerabilities) > 0
        assert any(v.level == VulnerabilityLevel.HIGH for v in vulnerabilities)
    
    def test_scan_transaction(self):
        """Test transaction scanning"""
        scanner = VulnerabilityScanner()
        
        transaction = PaymentTransaction(
            transaction_id="test_123",
            amount=100.0,
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1' OR '1'='1",  # Malicious
            payment_method="credit_card"
        )
        
        vulnerabilities = scanner.scan_transaction(transaction)
        assert len(vulnerabilities) > 0
    
    def test_large_amount_detection(self):
        """Test detection of unusually large amounts"""
        scanner = VulnerabilityScanner()
        
        transaction = PaymentTransaction(
            transaction_id="test_123",
            amount=9999999.0,
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card"
        )
        
        vulnerabilities = scanner.scan_transaction(transaction)
        assert any("large" in v.description.lower() for v in vulnerabilities)


class TestAutomatedBugFixer:
    """Tests for automated bug detection and fixing"""
    
    def test_currency_format_fix(self):
        """Test automatic currency format correction"""
        fixer = AutomatedBugFixer()
        
        transaction = PaymentTransaction(
            transaction_id="test_123",
            amount=100.0,
            currency="usd",  # Should be uppercase
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card"
        )
        
        bugs = fixer.detect_bugs(transaction)
        assert len(bugs) > 0
        
        fixes = fixer.apply_fixes(transaction)
        assert fixes > 0
        assert transaction.currency == "USD"
    
    def test_amount_precision_fix(self):
        """Test automatic amount precision correction"""
        fixer = AutomatedBugFixer()
        
        transaction = PaymentTransaction(
            transaction_id="test_123",
            amount=100.999,  # Too many decimals
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card"
        )
        
        bugs = fixer.detect_bugs(transaction)
        fixes = fixer.apply_fixes(transaction)
        
        assert fixes > 0
        # round(100.999, 2) = 101.0
        assert transaction.amount == 101.00


class TestMonitoringService:
    """Tests for monitoring service"""
    
    def test_start_stop_monitoring(self):
        """Test starting and stopping monitoring"""
        service = MonitoringService()
        
        service.start_monitoring()
        assert service.monitoring_active is True
        
        time.sleep(1)  # Let it run briefly
        
        service.stop_monitoring()
        assert service.monitoring_active is False
    
    def test_create_alert(self):
        """Test alert creation"""
        service = MonitoringService()
        
        alert = service.create_alert(
            severity="high",
            message="Test alert",
            component="test"
        )
        
        assert alert is not None
        assert alert.severity == "high"
        assert alert.acknowledged is False
    
    def test_acknowledge_alert(self):
        """Test alert acknowledgment"""
        service = MonitoringService()
        
        alert = service.create_alert(
            severity="medium",
            message="Test alert",
            component="test"
        )
        
        result = service.acknowledge_alert(alert.alert_id)
        assert result is True
        assert alert.acknowledged is True
    
    def test_record_metrics(self):
        """Test metrics recording"""
        service = MonitoringService()
        
        service.record_transaction_metric(success=True, processing_time=1.5)
        service.record_transaction_metric(success=True, processing_time=2.0)
        service.record_transaction_metric(success=False, processing_time=0.5)
        
        summary = service.get_metrics_summary()
        assert summary["transaction_count"]["count"] == 3


class TestSelfLearningAI:
    """Tests for self-learning AI system"""
    
    def test_learn_from_transaction(self):
        """Test learning from transactions"""
        ai = SelfLearningAI()
        
        transaction = PaymentTransaction(
            transaction_id="test_123",
            amount=100.0,
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card",
            status=PaymentStatus.COMPLETED
        )
        
        ai.learn_from_transaction(transaction)
        insights = ai.get_customer_insights("customer_1")
        
        assert insights is not None
        assert insights["total_transactions"] == 1
    
    def test_fraud_detection(self):
        """Test fraud detection"""
        ai = SelfLearningAI()
        
        # Train with normal transactions
        for i in range(10):
            transaction = PaymentTransaction(
                transaction_id=f"test_{i}",
                amount=50.0 + i,
                currency="USD",
                merchant_id="merchant_1",
                customer_id="customer_1",
                payment_method="credit_card",
                status=PaymentStatus.COMPLETED
            )
            ai.learn_from_transaction(transaction)
        
        # Test with suspicious transaction
        suspicious = PaymentTransaction(
            transaction_id="suspicious_1",
            amount=10000.0,  # Much larger than normal
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card"
        )
        
        fraud_score = ai.fraud_detector.calculate_fraud_score(suspicious)
        assert fraud_score > 0.2  # Should be flagged
    
    def test_risk_level_prediction(self):
        """Test risk level prediction"""
        ai = SelfLearningAI()
        
        transaction = PaymentTransaction(
            transaction_id="test_123",
            amount=100.0,
            currency="USD",
            merchant_id="merchant_1",
            customer_id="customer_1",
            payment_method="credit_card"
        )
        
        risk = ai.predict_risk_level(transaction)
        assert risk in ["low", "medium", "high", "critical"]


class TestPaymentGateway:
    """Integration tests for the complete payment gateway"""
    
    def test_gateway_initialization(self):
        """Test gateway initialization"""
        gateway = PaymentGateway()
        
        assert gateway.payment_controller is not None
        assert gateway.vulnerability_scanner is not None
        assert gateway.bug_fixer is not None
        assert gateway.monitoring_service is not None
        assert gateway.ai_system is not None
        
        gateway.shutdown()
    
    def test_process_valid_payment(self):
        """Test processing a valid payment"""
        gateway = PaymentGateway()
        
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
        
        assert result["success"] is True
        assert "transaction_id" in result
        
        gateway.shutdown()
    
    def test_block_malicious_payment(self):
        """Test blocking of malicious payment"""
        gateway = PaymentGateway()
        
        result = gateway.process_payment(
            amount=100.0,
            currency="USD",
            merchant_id="merchant_123",
            customer_id="customer' OR '1'='1",  # SQL injection attempt
            payment_method="credit_card",
            metadata={"ip_address": "192.168.1.1"}
        )
        
        assert result["success"] is False
        assert "security" in result["message"].lower() or "flagged" in result["message"].lower()
        
        gateway.shutdown()
    
    def test_get_system_health(self):
        """Test system health reporting"""
        gateway = PaymentGateway()
        
        health = gateway.get_system_health()
        
        assert "monitoring_active" in health
        assert "uptime" in health
        assert "metrics" in health
        
        gateway.shutdown()
