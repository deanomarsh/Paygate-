"""
Payment Gateway Analysis System - Core Module

A comprehensive payment gateway system that:
- Controls payment flow through e-commerce
- Detects vulnerabilities and security issues
- Provides automated bug fixes
- Offers 24/7 monitoring with alerts
- Ensures zero downtime with self-learning AI
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
import hashlib
import json


class PaymentStatus(Enum):
    """Payment transaction status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    FLAGGED = "flagged"


class VulnerabilityLevel(Enum):
    """Security vulnerability severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PaymentTransaction:
    """Represents a payment transaction"""
    transaction_id: str
    amount: float
    currency: str
    merchant_id: str
    customer_id: str
    payment_method: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: PaymentStatus = PaymentStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary"""
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "currency": self.currency,
            "merchant_id": self.merchant_id,
            "customer_id": self.customer_id,
            "payment_method": self.payment_method,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "metadata": self.metadata
        }
    
    def calculate_hash(self) -> str:
        """Generate transaction hash for integrity verification"""
        data = f"{self.transaction_id}{self.amount}{self.currency}{self.merchant_id}{self.customer_id}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class SecurityVulnerability:
    """Represents a detected security vulnerability"""
    vuln_id: str
    level: VulnerabilityLevel
    description: str
    affected_component: str
    detected_at: datetime = field(default_factory=datetime.now)
    fixed: bool = False
    fix_applied: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert vulnerability to dictionary"""
        return {
            "vuln_id": self.vuln_id,
            "level": self.level.value,
            "description": self.description,
            "affected_component": self.affected_component,
            "detected_at": self.detected_at.isoformat(),
            "fixed": self.fixed,
            "fix_applied": self.fix_applied
        }


@dataclass
class Alert:
    """Represents a system alert"""
    alert_id: str
    severity: str
    message: str
    component: str
    timestamp: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    
    def to_dict(self) -> dict:
        """Convert alert to dictionary"""
        return {
            "alert_id": self.alert_id,
            "severity": self.severity,
            "message": self.message,
            "component": self.component,
            "timestamp": self.timestamp.isoformat(),
            "acknowledged": self.acknowledged
        }
