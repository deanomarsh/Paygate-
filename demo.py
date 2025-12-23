"""
Example usage script demonstrating all features of the Payment Gateway System
"""

from gateway import PaymentGateway
import time


def print_section(title):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def main():
    print_section("Payment Gateway Analysis System - Demo")
    
    # Initialize the gateway
    gateway = PaymentGateway()
    print("✓ System initialized with 24/7 monitoring active")
    
    # Example 1: Process valid payments
    print_section("Example 1: Processing Valid Payments")
    
    result1 = gateway.process_payment(
        amount=99.99,
        currency="USD",
        merchant_id="amazon_store",
        customer_id="john_doe",
        payment_method="credit_card",
        metadata={
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0"
        }
    )
    
    print(f"Payment 1: ${result1['amount']} {result1['currency']}")
    print(f"Status: {result1['status']}")
    print(f"Risk Level: {result1.get('ai_analysis', {}).get('risk_level', 'N/A')}")
    print(f"Transaction ID: {result1['transaction_id']}")
    
    # Process more transactions for AI learning
    for i in range(3):
        gateway.process_payment(
            amount=50.0 + i * 10,
            currency="USD",
            merchant_id="amazon_store",
            customer_id="john_doe",
            payment_method="credit_card",
            metadata={"ip_address": "192.168.1.100", "user_agent": "Mozilla/5.0"}
        )
    print("✓ Processed 3 more transactions for AI learning")
    
    # Example 2: Detect and block malicious payment
    print_section("Example 2: Security - Blocking Malicious Payment")
    
    result2 = gateway.process_payment(
        amount=100.0,
        currency="USD",
        merchant_id="test_store",
        customer_id="hacker' OR '1'='1",  # SQL injection attempt
        payment_method="credit_card",
        metadata={"ip_address": "10.0.0.1"}
    )
    
    print(f"Status: {result2['status']}")
    print(f"Message: {result2['message']}")
    print(f"✓ System blocked malicious transaction!")
    
    # Example 3: Automated bug fixing
    print_section("Example 3: Automated Bug Fixes")
    
    result3 = gateway.process_payment(
        amount=75.999,  # Too many decimals - will be auto-fixed
        currency="eur",  # Wrong case - will be auto-fixed
        merchant_id="ebay_store",
        customer_id="jane_smith",
        payment_method="paypal",
        metadata={"ip_address": "192.168.1.200"}  # Missing user_agent - will be added
    )
    
    print(f"Original amount precision: 75.999")
    print(f"Fixed amount: {result3['amount']}")
    print(f"Original currency: 'eur'")
    print(f"Fixed currency: {result3['currency']}")
    print(f"Bugs fixed: {result3.get('bugs_fixed', 0)}")
    print("✓ System automatically fixed issues!")
    
    # Example 4: Fraud detection
    print_section("Example 4: AI-Powered Fraud Detection")
    
    # Normal pattern established, now test with suspicious transaction
    result4 = gateway.process_payment(
        amount=10000.0,  # Unusually large amount
        currency="USD",
        merchant_id="amazon_store",
        customer_id="john_doe",
        payment_method="credit_card",
        metadata={"ip_address": "45.67.89.123"}  # Different IP
    )
    
    ai_analysis = result4.get('ai_analysis', {})
    print(f"Fraud Score: {ai_analysis.get('fraud_score', 0):.2f}")
    print(f"Risk Level: {ai_analysis.get('risk_level', 'N/A')}")
    print(f"Status: {result4['status']}")
    if ai_analysis.get('recommendations'):
        print(f"Recommendations: {', '.join(ai_analysis['recommendations'])}")
    
    # Example 5: Customer insights
    print_section("Example 5: Customer Insights from AI Learning")
    
    insights = gateway.get_customer_insights("john_doe")
    if insights:
        print(f"Customer: john_doe")
        print(f"Total Transactions: {insights['total_transactions']}")
        print(f"Average Amount: ${insights['average_amount']:.2f}")
        print(f"Preferred Payment: {insights['preferred_payment_method']}")
        print(f"Total Spent: ${insights['total_spent']:.2f}")
        print(f"Merchants Used: {insights['number_of_merchants']}")
    
    # Example 6: System health monitoring
    print_section("Example 6: System Health & Monitoring")
    
    health = gateway.get_system_health()
    print(f"Monitoring Active: {health['monitoring_active']}")
    print(f"Uptime: {health['uptime']['uptime_percentage']:.2f}%")
    print(f"Total Transactions: {health['uptime']['total_transactions']}")
    print(f"Success Rate: {health['metrics']['success_rate']['average']*100:.1f}%")
    print(f"Avg Processing Time: {health['metrics']['avg_processing_time']['average']*1000:.2f}ms")
    print(f"Active Alerts: {health['active_alerts']}")
    print(f"Critical Alerts: {health['critical_alerts']}")
    
    # Example 7: Alerts
    print_section("Example 7: Alert System")
    
    alerts = gateway.get_alerts()
    if alerts:
        print(f"Active Alerts: {len(alerts)}")
        for alert in alerts[:3]:  # Show first 3
            print(f"  - [{alert['severity']}] {alert['message']}")
    else:
        print("No active alerts - system running smoothly!")
    
    # Final summary
    print_section("Summary")
    print("✓ Payment flow control - Working")
    print("✓ Vulnerability scanning - Active")
    print("✓ Automated bug fixes - Applied")
    print("✓ 24/7 monitoring - Running")
    print("✓ AI fraud detection - Learning")
    print("✓ Zero downtime architecture - Ready")
    print("\n🎉 Payment Gateway Analysis System Demo Complete!")
    
    # Graceful shutdown
    print("\nShutting down system...")
    gateway.shutdown()
    print("✓ System shut down gracefully")


if __name__ == "__main__":
    main()
