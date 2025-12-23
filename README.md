# Payment Gateway Analysis System

A comprehensive Python-based system for analyzing payment gateway security and transaction patterns.

## Features

- **Transaction Analysis**: Monitor and analyze payment transactions in real-time
- **Fraud Detection**: Identify suspicious patterns including:
  - High-value transactions
  - Transactions from suspicious countries
  - Velocity abuse (multiple transactions in short periods)
- **Security Vulnerability Scanning**: Detect common payment gateway security issues
- **Risk Scoring**: Calculate overall risk scores based on multiple factors
- **Comprehensive Reporting**: Generate detailed analysis reports in JSON format
- **Command-Line Interface**: Easy-to-use CLI for batch analysis

## Installation

No external dependencies required! This system uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/deanomarsh/Paygate-.git
cd Paygate-

# Make CLI executable (optional)
chmod +x cli.py
```

## Usage

### Basic Analysis

```bash
# Create sample transaction data
python3 cli.py sample

# Analyze transactions
python3 cli.py analyze -t sample_transactions.json -o report.json

# With custom configuration
python3 cli.py analyze -t sample_transactions.json -c config.json -o report.json

# Verbose output with detailed vulnerabilities
python3 cli.py analyze -t sample_transactions.json -v
```

### Show Statistics

```bash
python3 cli.py stats -t sample_transactions.json
```

### Python API

```python
from paygate_analyzer import PaymentGatewayAnalyzer, Transaction, TransactionStatus
from datetime import datetime

# Initialize analyzer
analyzer = PaymentGatewayAnalyzer()

# Add transaction
txn = Transaction(
    transaction_id="TXN001",
    amount=150.00,
    currency="USD",
    timestamp=datetime.now().isoformat(),
    merchant_id="MERCH001",
    card_type="VISA",
    country="US",
    status=TransactionStatus.SUCCESS,
    ip_address="192.168.1.1"
)
analyzer.add_transaction(txn)

# Analyze fraud patterns
flagged = analyzer.analyze_fraud_patterns()

# Check velocity patterns
velocity_issues = analyzer.check_velocity_patterns()

# Scan for security vulnerabilities
vulnerabilities = analyzer.scan_security_vulnerabilities()

# Generate comprehensive report
report = analyzer.generate_report()
print(report.summary)

# Export report
analyzer.export_report_json(report, "report.json")
```

## Configuration

Create a `config.json` file to customize analysis parameters:

```json
{
  "fraud_threshold": 1000.0,
  "velocity_check_minutes": 10,
  "max_transactions_per_period": 5,
  "suspicious_countries": ["XX", "YY", "ZZ"],
  "log_level": "INFO",
  "fraud_prevention_enabled": false,
  "encryption_required": true,
  "pci_dss_mode": true
}
```

## Transaction Data Format

Transactions should be provided in JSON format:

```json
[
  {
    "transaction_id": "TXN001",
    "amount": 150.00,
    "currency": "USD",
    "timestamp": "2025-12-23T10:00:00",
    "merchant_id": "MERCH001",
    "card_type": "VISA",
    "country": "US",
    "status": "success",
    "ip_address": "192.168.1.1"
  }
]
```

## Security Features

- **PCI-DSS Compliance Checking**: Validates compliance indicators
- **Encryption Validation**: Checks for unencrypted transactions
- **Fraud Prevention**: Configurable fraud detection rules
- **Risk Scoring**: Multi-factor risk assessment
- **Vulnerability Scanning**: Identifies security weaknesses

## Risk Levels

- **LOW**: Risk score 0-30
- **MEDIUM**: Risk score 31-50
- **HIGH**: Risk score 51-70
- **CRITICAL**: Risk score 71-100

## Testing

Run the test suite:

```bash
python3 -m unittest test_paygate_analyzer.py -v
```

## Example Output

```
Payment Gateway Analysis Summary:
- Total Transactions Analyzed: 2
- Flagged Transactions: 1
- Security Vulnerabilities: 3
- Overall Risk Score: 45.00/100
- Risk Level: MEDIUM
```

## Architecture

The system consists of several key components:

- **PaymentGatewayAnalyzer**: Main analyzer class
- **Transaction**: Data model for payment transactions
- **SecurityVulnerability**: Data model for security issues
- **AnalysisReport**: Data model for analysis reports
- **CLI**: Command-line interface for batch operations

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting pull requests.

## License

See the repository for license information.

## Support

For issues and questions, please open an issue on GitHub.
