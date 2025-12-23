"""
Unit tests for Payment Gateway Analyzer
"""

import unittest
from datetime import datetime
from paygate_analyzer import (
    PaymentGatewayAnalyzer,
    Transaction,
    TransactionStatus,
    RiskLevel,
    SecurityVulnerability
)


class TestPaymentGatewayAnalyzer(unittest.TestCase):
    """Test cases for PaymentGatewayAnalyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = PaymentGatewayAnalyzer()
        self.sample_transaction = Transaction(
            transaction_id="TEST001",
            amount=100.0,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH001",
            card_type="VISA",
            country="US",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.1"
        )
    
    def test_initialization(self):
        """Test analyzer initialization"""
        self.assertIsNotNone(self.analyzer)
        self.assertIsNotNone(self.analyzer.config)
        self.assertEqual(len(self.analyzer.transactions), 0)
    
    def test_add_transaction(self):
        """Test adding transactions"""
        self.analyzer.add_transaction(self.sample_transaction)
        self.assertEqual(len(self.analyzer.transactions), 1)
        self.assertEqual(
            self.analyzer.transactions[0].transaction_id,
            "TEST001"
        )
    
    def test_fraud_detection_high_value(self):
        """Test fraud detection for high-value transactions"""
        high_value_txn = Transaction(
            transaction_id="TEST002",
            amount=5000.0,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH001",
            card_type="VISA",
            country="US",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.1"
        )
        
        self.analyzer.add_transaction(high_value_txn)
        flagged = self.analyzer.analyze_fraud_patterns()
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0].transaction_id, "TEST002")
    
    def test_fraud_detection_suspicious_country(self):
        """Test fraud detection for suspicious countries"""
        suspicious_txn = Transaction(
            transaction_id="TEST003",
            amount=100.0,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH001",
            card_type="VISA",
            country="XX",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.1"
        )
        
        self.analyzer.add_transaction(suspicious_txn)
        flagged = self.analyzer.analyze_fraud_patterns()
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0].country, "XX")
    
    def test_velocity_check(self):
        """Test velocity pattern detection"""
        # Add multiple transactions for same merchant
        for i in range(10):
            txn = Transaction(
                transaction_id=f"TEST{i:03d}",
                amount=100.0,
                currency="USD",
                timestamp=datetime.now().isoformat(),
                merchant_id="MERCH001",
                card_type="VISA",
                country="US",
                status=TransactionStatus.SUCCESS,
                ip_address="192.168.1.1"
            )
            self.analyzer.add_transaction(txn)
        
        velocity_issues = self.analyzer.check_velocity_patterns()
        self.assertIn("MERCH001", velocity_issues)
        self.assertEqual(len(velocity_issues["MERCH001"]), 10)
    
    def test_security_vulnerability_scan(self):
        """Test security vulnerability scanning"""
        self.analyzer.add_transaction(self.sample_transaction)
        vulnerabilities = self.analyzer.scan_security_vulnerabilities()
        self.assertGreater(len(vulnerabilities), 0)
    
    def test_risk_score_calculation(self):
        """Test risk score calculation"""
        # Add normal transaction
        self.analyzer.add_transaction(self.sample_transaction)
        score = self.analyzer.calculate_risk_score()
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_report_generation(self):
        """Test report generation"""
        self.analyzer.add_transaction(self.sample_transaction)
        report = self.analyzer.generate_report()
        
        self.assertIsNotNone(report)
        self.assertIsNotNone(report.report_id)
        self.assertEqual(report.total_transactions, 1)
        self.assertGreaterEqual(report.risk_score, 0)
    
    def test_statistics(self):
        """Test statistics retrieval"""
        self.analyzer.add_transaction(self.sample_transaction)
        stats = self.analyzer.get_statistics()
        
        self.assertIn('total_transactions', stats)
        self.assertIn('risk_score', stats)
        self.assertEqual(stats['total_transactions'], 1)
    
    def test_custom_config(self):
        """Test custom configuration"""
        custom_config = {
            'fraud_threshold': 500.0,
            'log_level': 'DEBUG'
        }
        analyzer = PaymentGatewayAnalyzer(config=custom_config)
        self.assertEqual(analyzer.config['fraud_threshold'], 500.0)
    
    def test_no_transactions(self):
        """Test behavior with no transactions"""
        report = self.analyzer.generate_report()
        self.assertEqual(report.total_transactions, 0)
        self.assertEqual(report.flagged_transactions, 0)


class TestDataModels(unittest.TestCase):
    """Test cases for data models"""
    
    def test_transaction_creation(self):
        """Test Transaction creation"""
        txn = Transaction(
            transaction_id="TEST001",
            amount=100.0,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH001",
            card_type="VISA",
            country="US",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.1"
        )
        self.assertEqual(txn.transaction_id, "TEST001")
        self.assertEqual(txn.amount, 100.0)
    
    def test_security_vulnerability_creation(self):
        """Test SecurityVulnerability creation"""
        vuln = SecurityVulnerability(
            vulnerability_id="VULN001",
            title="Test Vulnerability",
            description="Test description",
            risk_level=RiskLevel.HIGH,
            affected_component="Test Component",
            recommendation="Test recommendation",
            detected_at=datetime.now().isoformat()
        )
        self.assertEqual(vuln.vulnerability_id, "VULN001")
        self.assertEqual(vuln.risk_level, RiskLevel.HIGH)


if __name__ == '__main__':
    unittest.main()
