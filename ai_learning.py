"""
Self-Learning AI System

Machine learning-based system that learns from transaction patterns,
detects fraud, identifies anomalies, and improves over time.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import logging

from core import PaymentTransaction, PaymentStatus


class AnomalyDetector:
    """Simple anomaly detector using statistical methods"""
    
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold  # Standard deviations for anomaly
        self.transaction_history: List[float] = []
        
    def update(self, value: float):
        """Update history with new value"""
        self.transaction_history.append(value)
        # Keep only last 1000 transactions
        if len(self.transaction_history) > 1000:
            self.transaction_history.pop(0)
    
    def is_anomaly(self, value: float) -> bool:
        """Check if value is anomalous"""
        if len(self.transaction_history) < 30:
            return False  # Need enough data
        
        mean = np.mean(self.transaction_history)
        std = np.std(self.transaction_history)
        
        if std == 0:
            return False
        
        z_score = abs((value - mean) / std)
        return z_score > self.threshold


class FraudDetector:
    """Machine learning-based fraud detection"""
    
    def __init__(self):
        self.known_patterns: Dict[str, List[float]] = defaultdict(list)
        self.fraud_indicators: Dict[str, float] = {}
        self.logger = logging.getLogger(__name__)
        
    def learn_pattern(self, customer_id: str, amount: float, merchant_id: str):
        """
        Learn normal transaction patterns for a customer
        
        Args:
            customer_id: Customer identifier
            amount: Transaction amount
            merchant_id: Merchant identifier
        """
        key = f"{customer_id}_{merchant_id}"
        self.known_patterns[key].append(amount)
        
        # Keep only recent history
        if len(self.known_patterns[key]) > 100:
            self.known_patterns[key].pop(0)
    
    def calculate_fraud_score(self, transaction: PaymentTransaction) -> float:
        """
        Calculate fraud probability score (0-1)
        
        Args:
            transaction: Transaction to analyze
            
        Returns:
            Fraud score between 0 and 1
        """
        score = 0.0
        factors = []
        
        # Check 1: Unusual amount for this customer-merchant pair
        key = f"{transaction.customer_id}_{transaction.merchant_id}"
        if key in self.known_patterns and len(self.known_patterns[key]) >= 10:
            amounts = self.known_patterns[key]
            mean_amount = np.mean(amounts)
            std_amount = np.std(amounts)
            
            if std_amount > 0:
                z_score = abs((transaction.amount - mean_amount) / std_amount)
                if z_score > 3:
                    score += 0.3
                    factors.append("unusual_amount")
        
        # Check 2: Very high amount
        if transaction.amount > 10000:
            score += 0.2
            factors.append("high_amount")
        
        # Check 3: Rapid succession of transactions
        if "last_transaction_time" in transaction.metadata:
            try:
                last_time = datetime.fromisoformat(transaction.metadata["last_transaction_time"])
                time_diff = (transaction.timestamp - last_time).seconds
                if time_diff < 60:  # Less than 1 minute
                    score += 0.3
                    factors.append("rapid_succession")
            except:
                pass
        
        # Check 4: Unusual location (if available)
        if "ip_address" in transaction.metadata:
            ip = transaction.metadata["ip_address"]
            customer_key = f"customer_{transaction.customer_id}_ips"
            if customer_key in self.known_patterns:
                known_ips = self.known_patterns[customer_key]
                if ip not in known_ips and len(known_ips) >= 5:
                    score += 0.2
                    factors.append("new_location")
        
        # Check 5: Round numbers (common in fraud)
        if transaction.amount == int(transaction.amount) and transaction.amount >= 100:
            score += 0.1
            factors.append("round_amount")
        
        # Normalize score to 0-1
        score = min(score, 1.0)
        
        if score > 0.5:
            self.logger.warning(
                f"High fraud score {score:.2f} for transaction {transaction.transaction_id}. "
                f"Factors: {', '.join(factors)}"
            )
        
        return score
    
    def is_likely_fraud(self, transaction: PaymentTransaction, threshold: float = 0.6) -> bool:
        """
        Determine if transaction is likely fraudulent
        
        Args:
            transaction: Transaction to check
            threshold: Fraud score threshold
            
        Returns:
            True if likely fraud
        """
        score = self.calculate_fraud_score(transaction)
        return score >= threshold


class SelfLearningAI:
    """Self-learning AI system for payment gateway"""
    
    def __init__(self):
        self.amount_detector = AnomalyDetector()
        self.fraud_detector = FraudDetector()
        self.transaction_patterns: Dict[str, Dict] = {}
        self.learning_rate = 0.1
        self.logger = logging.getLogger(__name__)
        
    def learn_from_transaction(self, transaction: PaymentTransaction):
        """
        Learn from a completed transaction
        
        Args:
            transaction: Transaction to learn from
        """
        # Only learn from successful transactions
        if transaction.status == PaymentStatus.COMPLETED:
            # Update anomaly detector
            self.amount_detector.update(transaction.amount)
            
            # Update fraud detector patterns
            self.fraud_detector.learn_pattern(
                transaction.customer_id,
                transaction.amount,
                transaction.merchant_id
            )
            
            # Learn customer patterns
            customer_key = transaction.customer_id
            if customer_key not in self.transaction_patterns:
                self.transaction_patterns[customer_key] = {
                    "total_transactions": 0,
                    "total_amount": 0.0,
                    "avg_amount": 0.0,
                    "preferred_methods": defaultdict(int),
                    "merchants": set()
                }
            
            pattern = self.transaction_patterns[customer_key]
            pattern["total_transactions"] += 1
            pattern["total_amount"] += transaction.amount
            pattern["avg_amount"] = pattern["total_amount"] / pattern["total_transactions"]
            pattern["preferred_methods"][transaction.payment_method] += 1
            pattern["merchants"].add(transaction.merchant_id)
            
            self.logger.info(f"Learned from transaction: {transaction.transaction_id}")
    
    def analyze_transaction(self, transaction: PaymentTransaction) -> Dict[str, any]:
        """
        Analyze transaction using learned patterns
        
        Args:
            transaction: Transaction to analyze
            
        Returns:
            Analysis results dictionary
        """
        results = {
            "is_anomaly": False,
            "fraud_score": 0.0,
            "is_likely_fraud": False,
            "risk_level": "low",
            "recommendations": []
        }
        
        # Check for amount anomaly
        if self.amount_detector.is_anomaly(transaction.amount):
            results["is_anomaly"] = True
            results["recommendations"].append("Review unusual transaction amount")
        
        # Calculate fraud score
        fraud_score = self.fraud_detector.calculate_fraud_score(transaction)
        results["fraud_score"] = fraud_score
        
        if fraud_score >= 0.7:
            results["is_likely_fraud"] = True
            results["risk_level"] = "critical"
            results["recommendations"].append("Block transaction - high fraud risk")
        elif fraud_score >= 0.5:
            results["risk_level"] = "high"
            results["recommendations"].append("Require additional verification")
        elif fraud_score >= 0.3:
            results["risk_level"] = "medium"
            results["recommendations"].append("Monitor transaction closely")
        
        # Check customer history
        if transaction.customer_id in self.transaction_patterns:
            pattern = self.transaction_patterns[transaction.customer_id]
            
            # Check if merchant is new for this customer
            if transaction.merchant_id not in pattern["merchants"]:
                results["recommendations"].append("New merchant for customer")
            
            # Check if payment method is unusual
            preferred_method = max(pattern["preferred_methods"].items(), 
                                 key=lambda x: x[1])[0] if pattern["preferred_methods"] else None
            if preferred_method and transaction.payment_method != preferred_method:
                results["recommendations"].append("Unusual payment method for customer")
        
        return results
    
    def get_customer_insights(self, customer_id: str) -> Optional[Dict]:
        """
        Get learned insights about a customer
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            Customer insights dictionary or None
        """
        if customer_id not in self.transaction_patterns:
            return None
        
        pattern = self.transaction_patterns[customer_id]
        
        # Find preferred payment method
        preferred_method = None
        if pattern["preferred_methods"]:
            preferred_method = max(pattern["preferred_methods"].items(), 
                                 key=lambda x: x[1])[0]
        
        return {
            "total_transactions": pattern["total_transactions"],
            "average_amount": pattern["avg_amount"],
            "preferred_payment_method": preferred_method,
            "number_of_merchants": len(pattern["merchants"]),
            "total_spent": pattern["total_amount"]
        }
    
    def predict_risk_level(self, transaction: PaymentTransaction) -> str:
        """
        Predict risk level for a transaction
        
        Args:
            transaction: Transaction to predict
            
        Returns:
            Risk level: "low", "medium", "high", or "critical"
        """
        analysis = self.analyze_transaction(transaction)
        return analysis["risk_level"]
