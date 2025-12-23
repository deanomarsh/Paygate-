#!/usr/bin/env python3
"""
Command-line interface for Payment Gateway Analysis System
"""

import argparse
import json
import sys
from datetime import datetime
from paygate_analyzer import (
    PaymentGatewayAnalyzer,
    Transaction,
    TransactionStatus,
    RiskLevel
)


def load_config(config_file: str) -> dict:
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)


def load_transactions(transactions_file: str) -> list:
    """Load transactions from JSON file"""
    try:
        with open(transactions_file, 'r') as f:
            data = json.load(f)
            transactions = []
            for txn_data in data:
                txn = Transaction(
                    transaction_id=txn_data['transaction_id'],
                    amount=txn_data['amount'],
                    currency=txn_data['currency'],
                    timestamp=txn_data['timestamp'],
                    merchant_id=txn_data['merchant_id'],
                    card_type=txn_data['card_type'],
                    country=txn_data['country'],
                    status=TransactionStatus(txn_data['status']),
                    ip_address=txn_data['ip_address']
                )
                transactions.append(txn)
            return transactions
    except FileNotFoundError:
        print(f"Error: Transactions file '{transactions_file}' not found")
        sys.exit(1)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error: Invalid transaction data: {e}")
        sys.exit(1)


def analyze_transactions(args):
    """Analyze transactions command"""
    # Load configuration
    config = None
    if args.config:
        config = load_config(args.config)
    
    # Initialize analyzer
    analyzer = PaymentGatewayAnalyzer(config=config)
    
    # Load and add transactions
    transactions = load_transactions(args.transactions)
    for txn in transactions:
        analyzer.add_transaction(txn)
    
    print(f"Loaded {len(transactions)} transactions")
    
    # Perform analysis
    print("\nAnalyzing fraud patterns...")
    flagged = analyzer.analyze_fraud_patterns()
    print(f"Flagged transactions: {len(flagged)}")
    
    print("\nChecking velocity patterns...")
    velocity_issues = analyzer.check_velocity_patterns()
    print(f"Merchants with velocity issues: {len(velocity_issues)}")
    
    print("\nScanning security vulnerabilities...")
    vulnerabilities = analyzer.scan_security_vulnerabilities()
    print(f"Vulnerabilities found: {len(vulnerabilities)}")
    
    # Generate report
    report = analyzer.generate_report()
    
    print("\n" + "=" * 60)
    print(report.summary)
    print("=" * 60)
    
    # Export report if requested
    if args.output:
        analyzer.export_report_json(report, args.output)
        print(f"\nReport saved to: {args.output}")
    
    # Show detailed vulnerabilities if requested
    if args.verbose and vulnerabilities:
        print("\nDetailed Vulnerabilities:")
        for vuln in vulnerabilities:
            print(f"\n  [{vuln.risk_level.value.upper()}] {vuln.title}")
            print(f"  ID: {vuln.vulnerability_id}")
            print(f"  Component: {vuln.affected_component}")
            print(f"  Description: {vuln.description}")
            print(f"  Recommendation: {vuln.recommendation}")


def show_statistics(args):
    """Show statistics command"""
    config = None
    if args.config:
        config = load_config(args.config)
    
    analyzer = PaymentGatewayAnalyzer(config=config)
    
    if args.transactions:
        transactions = load_transactions(args.transactions)
        for txn in transactions:
            analyzer.add_transaction(txn)
    
    stats = analyzer.get_statistics()
    
    print("\nPayment Gateway Statistics")
    print("=" * 60)
    print(f"Total Transactions: {stats['total_transactions']}")
    print(f"Flagged Transactions: {stats['flagged_count']}")
    print(f"Security Vulnerabilities: {stats['total_vulnerabilities']}")
    print(f"Risk Score: {stats['risk_score']:.2f}/100")
    print("=" * 60)


def create_sample_data(args):
    """Create sample transaction data"""
    sample_transactions = [
        {
            "transaction_id": "TXN001",
            "amount": 150.00,
            "currency": "USD",
            "timestamp": datetime.now().isoformat(),
            "merchant_id": "MERCH001",
            "card_type": "VISA",
            "country": "US",
            "status": "success",
            "ip_address": "192.168.1.1"
        },
        {
            "transaction_id": "TXN002",
            "amount": 2500.00,
            "currency": "USD",
            "timestamp": datetime.now().isoformat(),
            "merchant_id": "MERCH001",
            "card_type": "MASTERCARD",
            "country": "XX",
            "status": "success",
            "ip_address": "192.168.1.2"
        },
        {
            "transaction_id": "TXN003",
            "amount": 75.50,
            "currency": "EUR",
            "timestamp": datetime.now().isoformat(),
            "merchant_id": "MERCH002",
            "card_type": "AMEX",
            "country": "UK",
            "status": "success",
            "ip_address": "192.168.1.3"
        }
    ]
    
    output_file = args.output or "sample_transactions.json"
    with open(output_file, 'w') as f:
        json.dump(sample_transactions, f, indent=2)
    
    print(f"Sample transaction data created: {output_file}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Payment Gateway Analysis System CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze transactions for fraud and security issues'
    )
    analyze_parser.add_argument(
        '-t', '--transactions',
        required=True,
        help='Path to transactions JSON file'
    )
    analyze_parser.add_argument(
        '-c', '--config',
        help='Path to configuration JSON file'
    )
    analyze_parser.add_argument(
        '-o', '--output',
        help='Path to output report JSON file'
    )
    analyze_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    
    # Statistics command
    stats_parser = subparsers.add_parser(
        'stats',
        help='Show statistics'
    )
    stats_parser.add_argument(
        '-t', '--transactions',
        help='Path to transactions JSON file'
    )
    stats_parser.add_argument(
        '-c', '--config',
        help='Path to configuration JSON file'
    )
    
    # Sample data command
    sample_parser = subparsers.add_parser(
        'sample',
        help='Create sample transaction data'
    )
    sample_parser.add_argument(
        '-o', '--output',
        help='Output file path (default: sample_transactions.json)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'analyze':
        analyze_transactions(args)
    elif args.command == 'stats':
        show_statistics(args)
    elif args.command == 'sample':
        create_sample_data(args)


if __name__ == '__main__':
    main()
