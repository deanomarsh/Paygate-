#!/usr/bin/env python3
"""
Example usage of the Payment Gateway Analysis System
Demonstrates all key features and functionality
"""

from datetime import datetime
from paygate_analyzer import (
    PaymentGatewayAnalyzer,
    Transaction,
    TransactionStatus,
    RiskLevel
)


def main():
    print("=" * 70)
    print("Payment Gateway Analysis System - Comprehensive Example")
    print("=" * 70)
    print()
    
    # Initialize analyzer with custom configuration
    custom_config = {
        'fraud_threshold': 1500.0,
        'velocity_check_minutes': 10,
        'max_transactions_per_period': 3,
        'suspicious_countries': ['XX', 'YY', 'ZZ'],
        'log_level': 'INFO',
        'fraud_prevention_enabled': False,
        'pci_dss_mode': True
    }
    
    analyzer = PaymentGatewayAnalyzer(config=custom_config)
    print("✓ Analyzer initialized with custom configuration")
    print()
    
    # Create sample transactions with various scenarios
    transactions = [
        # Normal transaction
        Transaction(
            transaction_id="TXN-001",
            amount=50.00,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH-001",
            card_type="VISA",
            country="US",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.100"
        ),
        # High-value transaction (should be flagged)
        Transaction(
            transaction_id="TXN-002",
            amount=2500.00,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH-001",
            card_type="MASTERCARD",
            country="US",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.101"
        ),
        # Suspicious country (should be flagged)
        Transaction(
            transaction_id="TXN-003",
            amount=200.00,
            currency="EUR",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH-002",
            card_type="AMEX",
            country="XX",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.102"
        ),
        # Multiple transactions from same merchant (velocity check)
        Transaction(
            transaction_id="TXN-004",
            amount=100.00,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH-003",
            card_type="VISA",
            country="UK",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.103"
        ),
        Transaction(
            transaction_id="TXN-005",
            amount=150.00,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH-003",
            card_type="VISA",
            country="UK",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.104"
        ),
        Transaction(
            transaction_id="TXN-006",
            amount=200.00,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH-003",
            card_type="VISA",
            country="UK",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.105"
        ),
        Transaction(
            transaction_id="TXN-007",
            amount=250.00,
            currency="USD",
            timestamp=datetime.now().isoformat(),
            merchant_id="MERCH-003",
            card_type="VISA",
            country="UK",
            status=TransactionStatus.SUCCESS,
            ip_address="192.168.1.106"
        ),
    ]
    
    # Add all transactions
    print(f"Adding {len(transactions)} transactions...")
    for txn in transactions:
        analyzer.add_transaction(txn)
    print(f"✓ {len(transactions)} transactions added\n")
    
    # Perform fraud analysis
    print("-" * 70)
    print("FRAUD PATTERN ANALYSIS")
    print("-" * 70)
    flagged = analyzer.analyze_fraud_patterns()
    print(f"Flagged transactions: {len(flagged)}")
    for txn in flagged:
        print(f"  - {txn.transaction_id}: ${txn.amount:.2f} ({txn.country})")
    print()
    
    # Check velocity patterns
    print("-" * 70)
    print("VELOCITY PATTERN CHECK")
    print("-" * 70)
    velocity_issues = analyzer.check_velocity_patterns()
    if velocity_issues:
        print(f"Merchants with velocity issues: {len(velocity_issues)}")
        for merchant_id, txns in velocity_issues.items():
            print(f"  - {merchant_id}: {len(txns)} transactions")
    else:
        print("No velocity issues detected")
    print()
    
    # Scan for security vulnerabilities
    print("-" * 70)
    print("SECURITY VULNERABILITY SCAN")
    print("-" * 70)
    vulnerabilities = analyzer.scan_security_vulnerabilities()
    print(f"Vulnerabilities found: {len(vulnerabilities)}")
    for vuln in vulnerabilities:
        print(f"\n  [{vuln.risk_level.value.upper()}] {vuln.title}")
        print(f"  ID: {vuln.vulnerability_id}")
        print(f"  Component: {vuln.affected_component}")
        print(f"  Description: {vuln.description}")
        print(f"  Recommendation: {vuln.recommendation}")
    print()
    
    # Calculate risk score
    print("-" * 70)
    print("RISK ASSESSMENT")
    print("-" * 70)
    risk_score = analyzer.calculate_risk_score()
    print(f"Overall Risk Score: {risk_score:.2f}/100")
    
    if risk_score > 70:
        risk_level = "CRITICAL"
        status_emoji = "🔴"
    elif risk_score > 50:
        risk_level = "HIGH"
        status_emoji = "🟠"
    elif risk_score > 30:
        risk_level = "MEDIUM"
        status_emoji = "🟡"
    else:
        risk_level = "LOW"
        status_emoji = "🟢"
    
    print(f"Risk Level: {status_emoji} {risk_level}")
    print()
    
    # Get statistics
    print("-" * 70)
    print("STATISTICS")
    print("-" * 70)
    stats = analyzer.get_statistics()
    print(f"Total Transactions: {stats['total_transactions']}")
    print(f"Flagged Transactions: {stats['flagged_count']}")
    print(f"Security Vulnerabilities: {stats['total_vulnerabilities']}")
    print(f"Risk Score: {stats['risk_score']:.2f}/100")
    print()
    
    # Generate comprehensive report
    print("-" * 70)
    print("GENERATING COMPREHENSIVE REPORT")
    print("-" * 70)
    report = analyzer.generate_report()
    print(f"\n{report.summary}")
    print(f"Report ID: {report.report_id}")
    print(f"Generated at: {report.generated_at}")
    
    # Export report to JSON
    report_filename = "comprehensive_report.json"
    analyzer.export_report_json(report, report_filename)
    print(f"\n✓ Report exported to: {report_filename}")
    
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
