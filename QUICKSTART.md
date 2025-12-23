# Quick Start Guide

Get started with the Payment Gateway Analysis System in minutes!

## Installation

```bash
git clone https://github.com/deanomarsh/Paygate-.git
cd Paygate-
```

No additional dependencies required - uses Python 3 standard library only!

## Quick Start

### 1. Run the Example

```bash
python3 example.py
```

This demonstrates all features with sample data.

### 2. Create Sample Data

```bash
python3 cli.py sample
```

Generates `sample_transactions.json` with test data.

### 3. Analyze Transactions

```bash
python3 cli.py analyze -t sample_transactions.json -o report.json -v
```

Options:
- `-t, --transactions`: Input transaction file (required)
- `-c, --config`: Custom configuration file (optional)
- `-o, --output`: Output report file (optional)
- `-v, --verbose`: Show detailed output (optional)

### 4. View Statistics

```bash
python3 cli.py stats -t sample_transactions.json
```

## Python API Quick Example

```python
from paygate_analyzer import PaymentGatewayAnalyzer, Transaction, TransactionStatus
from datetime import datetime

# Create analyzer
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

# Analyze and report
report = analyzer.generate_report()
print(report.summary)
```

## Common Use Cases

### Detect High-Value Transactions

Configure the fraud threshold in `config.json`:

```json
{
  "fraud_threshold": 1000.0
}
```

### Monitor Suspicious Countries

Add countries to watch list:

```json
{
  "suspicious_countries": ["XX", "YY", "ZZ"]
}
```

### Check Transaction Velocity

Set maximum transactions per period:

```json
{
  "max_transactions_per_period": 5,
  "velocity_check_minutes": 10
}
```

## Running Tests

```bash
python3 -m unittest test_paygate_analyzer.py -v
```

All 13 tests should pass.

## Output Files

Generated reports are in JSON format and include:
- Report ID and timestamp
- Transaction statistics
- Flagged transaction count
- Vulnerability count
- Risk score (0-100)
- Summary text

## Configuration Parameters

Key parameters in `config.json`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `fraud_threshold` | 1000.0 | Amount threshold for high-value alerts |
| `max_transactions_per_period` | 5 | Max transactions before velocity alert |
| `suspicious_countries` | ["XX", "YY"] | Countries to flag |
| `fraud_ratio_weight` | 30 | Weight for fraud ratio in risk score |
| `risk_threshold_high` | 70 | Threshold for HIGH risk level |

## Risk Levels

- **LOW**: 0-30 points
- **MEDIUM**: 31-50 points
- **HIGH**: 51-70 points
- **CRITICAL**: 71-100 points

## Next Steps

1. Customize `config.json` for your needs
2. Prepare your transaction data in JSON format
3. Run analysis on real data
4. Review generated reports
5. Set up automated monitoring (cron jobs, etc.)

## Getting Help

See `README.md` for full documentation or run:

```bash
python3 cli.py --help
python3 cli.py analyze --help
```

## Tips

- Start with sample data to understand the output format
- Use verbose mode (`-v`) to see detailed vulnerability information
- Export reports for record keeping and compliance
- Adjust thresholds based on your risk tolerance
- Run regular scans to monitor security posture

Happy analyzing! 🔒
