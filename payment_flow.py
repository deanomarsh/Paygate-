"""
Payment Flow Controller

Manages the flow of payments through the e-commerce system,
ensuring proper validation, processing, and routing.
"""

from typing import Dict, List, Optional
from datetime import datetime
import uuid
import logging

from core import PaymentTransaction, PaymentStatus, Alert


class PaymentFlowController:
    """Controls and manages payment transaction flow"""
    
    def __init__(self):
        self.transactions: Dict[str, PaymentTransaction] = {}
        self.processing_queue: List[str] = []
        self.logger = logging.getLogger(__name__)
        
    def initiate_payment(
        self,
        amount: float,
        currency: str,
        merchant_id: str,
        customer_id: str,
        payment_method: str,
        metadata: Optional[Dict] = None
    ) -> PaymentTransaction:
        """
        Initiate a new payment transaction
        
        Args:
            amount: Payment amount
            currency: Currency code (e.g., USD, EUR)
            merchant_id: Merchant identifier
            customer_id: Customer identifier
            payment_method: Payment method (e.g., credit_card, paypal)
            metadata: Additional transaction metadata
            
        Returns:
            PaymentTransaction object
        """
        transaction_id = str(uuid.uuid4())
        
        transaction = PaymentTransaction(
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            merchant_id=merchant_id,
            customer_id=customer_id,
            payment_method=payment_method,
            metadata=metadata or {}
        )
        
        self.transactions[transaction_id] = transaction
        self.processing_queue.append(transaction_id)
        
        self.logger.info(f"Payment initiated: {transaction_id} for amount {amount} {currency}")
        
        return transaction
    
    def validate_payment(self, transaction_id: str) -> bool:
        """
        Validate a payment transaction
        
        Args:
            transaction_id: Transaction identifier
            
        Returns:
            True if valid, False otherwise
        """
        if transaction_id not in self.transactions:
            self.logger.error(f"Transaction not found: {transaction_id}")
            return False
        
        transaction = self.transactions[transaction_id]
        
        # Basic validation checks
        if transaction.amount <= 0:
            self.logger.error(f"Invalid amount: {transaction.amount}")
            return False
        
        if not transaction.currency or len(transaction.currency) != 3:
            self.logger.error(f"Invalid currency: {transaction.currency}")
            return False
        
        if not transaction.merchant_id or not transaction.customer_id:
            self.logger.error("Missing merchant or customer ID")
            return False
        
        # Check for duplicate transactions (simple check)
        tx_hash = transaction.calculate_hash()
        for tid, tx in self.transactions.items():
            if tid != transaction_id and tx.calculate_hash() == tx_hash:
                if (datetime.now() - tx.timestamp).seconds < 300:  # 5 minutes
                    self.logger.warning(f"Potential duplicate transaction: {transaction_id}")
                    return False
        
        return True
    
    def process_payment(self, transaction_id: str) -> bool:
        """
        Process a validated payment
        
        Args:
            transaction_id: Transaction identifier
            
        Returns:
            True if processing started successfully
        """
        if transaction_id not in self.transactions:
            return False
        
        transaction = self.transactions[transaction_id]
        
        if not self.validate_payment(transaction_id):
            transaction.status = PaymentStatus.FAILED
            return False
        
        transaction.status = PaymentStatus.PROCESSING
        self.logger.info(f"Processing payment: {transaction_id}")
        
        # In a real system, this would integrate with payment processors
        # For now, we'll simulate successful processing
        transaction.status = PaymentStatus.COMPLETED
        
        if transaction_id in self.processing_queue:
            self.processing_queue.remove(transaction_id)
        
        self.logger.info(f"Payment completed: {transaction_id}")
        
        return True
    
    def get_transaction(self, transaction_id: str) -> Optional[PaymentTransaction]:
        """Get transaction details"""
        return self.transactions.get(transaction_id)
    
    def get_transaction_status(self, transaction_id: str) -> Optional[PaymentStatus]:
        """Get transaction status"""
        transaction = self.transactions.get(transaction_id)
        return transaction.status if transaction else None
    
    def refund_payment(self, transaction_id: str) -> bool:
        """
        Refund a completed payment
        
        Args:
            transaction_id: Transaction identifier
            
        Returns:
            True if refund successful
        """
        if transaction_id not in self.transactions:
            return False
        
        transaction = self.transactions[transaction_id]
        
        if transaction.status != PaymentStatus.COMPLETED:
            self.logger.error(f"Cannot refund non-completed transaction: {transaction_id}")
            return False
        
        transaction.status = PaymentStatus.REFUNDED
        self.logger.info(f"Payment refunded: {transaction_id}")
        
        return True
    
    def get_pending_transactions(self) -> List[PaymentTransaction]:
        """Get all pending transactions"""
        return [tx for tx in self.transactions.values() if tx.status == PaymentStatus.PENDING]
    
    def get_flagged_transactions(self) -> List[PaymentTransaction]:
        """Get all flagged transactions"""
        return [tx for tx in self.transactions.values() if tx.status == PaymentStatus.FLAGGED]
