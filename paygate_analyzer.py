#!/usr/bin/env python3
"""
Payment Gateway Analysis System
Main analyzer module for monitoring and analyzing payment gateway security and transactions.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class RiskLevel(Enum):
    """Risk level classification"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TransactionStatus(Enum):
    """Transaction status types"""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    FLAGGED = "flagged"


@dataclass
class Transaction:
    """Transaction data model"""
    transaction_id: str
    amount: float
    currency: str
    timestamp: str
    merchant_id: str
    card_type: str
    country: str
    status: TransactionStatus
    ip_address: str


@dataclass
class SecurityVulnerability:
    """Security vulnerability data model"""
    vulnerability_id: str
    title: str
    description: str
    risk_level: RiskLevel
    affected_component: str
    recommendation: str
    detected_at: str


@dataclass
class AnalysisReport:
    """Analysis report data model"""
    report_id: str
    generated_at: str
    total_transactions: int
    flagged_transactions: int
    vulnerabilities_found: int
    risk_score: float
    summary: str


class PaymentGatewayAnalyzer:
    """Main payment gateway analyzer class"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the payment gateway analyzer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or self._default_config()
        self.logger = self._setup_logger()
        self.transactions: List[Transaction] = []
        self.vulnerabilities: List[SecurityVulnerability] = []
        self._cached_flagged: Optional[List[Transaction]] = None
        
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'fraud_threshold': 1000.0,
            'velocity_check_minutes': 10,
            'max_transactions_per_period': 5,
            'suspicious_countries': ['XX', 'YY'],
            'log_level': 'INFO',
            'fraud_ratio_weight': 30,
            'vuln_weight_low': 5,
            'vuln_weight_medium': 15,
            'vuln_weight_high': 30,
            'vuln_weight_critical': 50,
            'risk_threshold_high': 70,
            'risk_threshold_medium': 50,
            'risk_threshold_low': 30
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('PaymentGatewayAnalyzer')
        log_level = self.config.get('log_level', 'INFO')
        logger.setLevel(getattr(logging, log_level))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add a transaction for analysis
        
        Args:
            transaction: Transaction object to analyze
        """
        self.transactions.append(transaction)
        self._cached_flagged = None  # Invalidate cache
        self.logger.info(f"Added transaction {transaction.transaction_id}")
    
    def analyze_fraud_patterns(self) -> List[Transaction]:
        """
        Analyze transactions for fraud patterns
        
        Returns:
            List of flagged transactions
        """
        # Return cached result if available
        if self._cached_flagged is not None:
            return self._cached_flagged
            
        flagged = []
        threshold = self.config['fraud_threshold']
        suspicious_countries = self.config['suspicious_countries']
        
        for txn in self.transactions:
            # Check for high-value transactions
            if txn.amount > threshold:
                self.logger.warning(
                    f"High-value transaction detected: {txn.transaction_id} "
                    f"(${txn.amount})"
                )
                flagged.append(txn)
            
            # Check for suspicious countries
            if txn.country in suspicious_countries:
                self.logger.warning(
                    f"Transaction from suspicious country: {txn.transaction_id} "
                    f"({txn.country})"
                )
                flagged.append(txn)
        
        # Cache the result
        self._cached_flagged = flagged
        return flagged
    
    def check_velocity_patterns(self) -> Dict[str, List[Transaction]]:
        """
        Check for velocity abuse (multiple transactions in short time)
        
        Returns:
            Dictionary of merchant_id to suspicious transactions
        """
        from collections import defaultdict
        
        velocity_issues = defaultdict(list)
        merchant_transactions = defaultdict(list)
        
        # Group transactions by merchant
        for txn in self.transactions:
            merchant_transactions[txn.merchant_id].append(txn)
        
        # Check each merchant's transaction velocity
        max_txns = self.config['max_transactions_per_period']
        for merchant_id, txns in merchant_transactions.items():
            if len(txns) > max_txns:
                self.logger.warning(
                    f"Velocity abuse detected for merchant {merchant_id}: "
                    f"{len(txns)} transactions"
                )
                velocity_issues[merchant_id] = txns
        
        return dict(velocity_issues)
    
    def scan_security_vulnerabilities(self) -> List[SecurityVulnerability]:
        """
        Scan for common payment gateway security vulnerabilities
        
        Returns:
            List of detected vulnerabilities
        """
        vulnerabilities = []
        
        # Check for transactions without secure protocol indicators
        # In a real system, this would check if transactions use HTTPS/TLS
        unsecure_count = 0
        for txn in self.transactions:
            # Check if IP address suggests insecure connection
            # Real implementation would check actual encryption status
            if not any(indicator in txn.ip_address.lower() 
                      for indicator in ['secure', 'tls', 'ssl']):
                unsecure_count += 1
        
        if unsecure_count > 0:
            vuln = SecurityVulnerability(
                vulnerability_id="VULN-001",
                title="Potential Unencrypted Transactions",
                description=f"Detected {unsecure_count} transactions without secure protocol indicators",
                risk_level=RiskLevel.HIGH,
                affected_component="Transaction Layer",
                recommendation="Enforce TLS/SSL encryption for all transactions",
                detected_at=datetime.now().isoformat()
            )
            vulnerabilities.append(vuln)
            self.vulnerabilities.append(vuln)
        
        # Check for missing fraud prevention
        if len(self.transactions) > 0 and not self.config.get('fraud_prevention_enabled'):
            vuln = SecurityVulnerability(
                vulnerability_id="VULN-002",
                title="Fraud Prevention Not Enabled",
                description="Fraud prevention mechanisms are not configured",
                risk_level=RiskLevel.MEDIUM,
                affected_component="Security Configuration",
                recommendation="Enable and configure fraud prevention rules",
                detected_at=datetime.now().isoformat()
            )
            vulnerabilities.append(vuln)
            self.vulnerabilities.append(vuln)
        
        # Check for PCI-DSS compliance only if enabled and transactions exist
        if len(self.transactions) > 0 and self.config.get('pci_dss_mode', False):
            vuln = SecurityVulnerability(
                vulnerability_id="VULN-003",
                title="PCI-DSS Compliance Check Required",
                description="Regular PCI-DSS compliance validation recommended",
                risk_level=RiskLevel.MEDIUM,
                affected_component="Compliance",
                recommendation="Schedule regular PCI-DSS compliance audits",
                detected_at=datetime.now().isoformat()
            )
            vulnerabilities.append(vuln)
            self.vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def calculate_risk_score(self) -> float:
        """
        Calculate overall risk score based on analysis
        
        Returns:
            Risk score between 0 and 100
        """
        score = 0.0
        
        # Factor in flagged transactions
        if len(self.transactions) > 0:
            fraud_ratio = len(self.analyze_fraud_patterns()) / len(self.transactions)
            fraud_weight = self.config.get('fraud_ratio_weight', 30)
            score += fraud_ratio * fraud_weight
        
        # Factor in vulnerabilities
        vuln_weights = {
            RiskLevel.LOW: self.config.get('vuln_weight_low', 5),
            RiskLevel.MEDIUM: self.config.get('vuln_weight_medium', 15),
            RiskLevel.HIGH: self.config.get('vuln_weight_high', 30),
            RiskLevel.CRITICAL: self.config.get('vuln_weight_critical', 50)
        }
        
        for vuln in self.vulnerabilities:
            score += vuln_weights.get(vuln.risk_level, 0)
        
        # Normalize score to 0-100
        return min(score, 100.0)
    
    def generate_report(self) -> AnalysisReport:
        """
        Generate comprehensive analysis report
        
        Returns:
            AnalysisReport object
        """
        flagged = self.analyze_fraud_patterns()
        vulnerabilities = self.scan_security_vulnerabilities()
        risk_score = self.calculate_risk_score()
        
        report = AnalysisReport(
            report_id=f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            generated_at=datetime.now().isoformat(),
            total_transactions=len(self.transactions),
            flagged_transactions=len(flagged),
            vulnerabilities_found=len(vulnerabilities),
            risk_score=risk_score,
            summary=self._generate_summary(flagged, vulnerabilities, risk_score)
        )
        
        return report
    
    def _generate_summary(self, flagged: List[Transaction], 
                         vulnerabilities: List[SecurityVulnerability],
                         risk_score: float) -> str:
        """Generate summary text for the report"""
        risk_threshold_high = self.config.get('risk_threshold_high', 70)
        risk_threshold_medium = self.config.get('risk_threshold_medium', 50)
        risk_threshold_low = self.config.get('risk_threshold_low', 30)
        
        risk_level = "LOW"
        if risk_score > risk_threshold_high:
            risk_level = "CRITICAL"
        elif risk_score > risk_threshold_medium:
            risk_level = "HIGH"
        elif risk_score > risk_threshold_low:
            risk_level = "MEDIUM"
        
        summary = (
            f"Payment Gateway Analysis Summary:\n"
            f"- Total Transactions Analyzed: {len(self.transactions)}\n"
            f"- Flagged Transactions: {len(flagged)}\n"
            f"- Security Vulnerabilities: {len(vulnerabilities)}\n"
            f"- Overall Risk Score: {risk_score:.2f}/100\n"
            f"- Risk Level: {risk_level}\n"
        )
        
        return summary
    
    def export_report_json(self, report: AnalysisReport, filename: str) -> None:
        """
        Export report to JSON file
        
        Args:
            report: AnalysisReport object
            filename: Output filename
        """
        report_dict = asdict(report)
        
        with open(filename, 'w') as f:
            json.dump(report_dict, f, indent=2)
        
        self.logger.info(f"Report exported to {filename}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get current statistics
        
        Returns:
            Dictionary of statistics
        """
        return {
            'total_transactions': len(self.transactions),
            'total_vulnerabilities': len(self.vulnerabilities),
            'risk_score': self.calculate_risk_score(),
            'flagged_count': len(self.analyze_fraud_patterns())
        }


def main():
    """Main function for CLI usage"""
    print("Payment Gateway Analysis System")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = PaymentGatewayAnalyzer()
    
    # Example transactions
    sample_transactions = [
        Transaction(
            transaction_id="TXN001",
            amount=150.00,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH001",
            card_type="VISA",
            country="US",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.1"
        ),
        Transaction(
            transaction_id="TXN002",
            amount=2500.00,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH001",
            card_type="MASTERCARD",
            country="XX",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.2"
        ),
    ]
    
    # Add transactions
    for txn in sample_transactions:
        analyzer.add_transaction(txn)
    
    # Generate report
    report = analyzer.generate_report()
    
    print("\n" + report.summary)
    print(f"\nReport ID: {report.report_id}")
    
    # Export report
    analyzer.export_report_json(report, "payment_gateway_report.json")
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
