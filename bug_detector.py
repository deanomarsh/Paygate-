"""
Automated Bug Detection and Fix System

Detects common bugs and issues in the payment system
and applies automated fixes where possible.
"""

from typing import List, Dict, Optional, Callable
from datetime import datetime
import uuid
import logging

from core import PaymentTransaction, PaymentStatus, SecurityVulnerability


class BugReport:
    """Represents a detected bug"""
    
    def __init__(self, bug_id: str, severity: str, description: str, 
                 component: str, auto_fixable: bool = False):
        self.bug_id = bug_id
        self.severity = severity
        self.description = description
        self.component = component
        self.auto_fixable = auto_fixable
        self.fixed = False
        self.fix_applied = None
        self.detected_at = datetime.now()
        
    def to_dict(self) -> dict:
        return {
            "bug_id": self.bug_id,
            "severity": self.severity,
            "description": self.description,
            "component": self.component,
            "auto_fixable": self.auto_fixable,
            "fixed": self.fixed,
            "fix_applied": self.fix_applied,
            "detected_at": self.detected_at.isoformat()
        }


class AutomatedBugFixer:
    """Detects and automatically fixes common bugs"""
    
    def __init__(self):
        self.bugs: Dict[str, BugReport] = {}
        self.fix_strategies: Dict[str, Callable] = self._initialize_fix_strategies()
        self.logger = logging.getLogger(__name__)
        
    def _initialize_fix_strategies(self) -> Dict[str, Callable]:
        """Initialize automated fix strategies"""
        return {
            "currency_mismatch": self._fix_currency_mismatch,
            "invalid_amount": self._fix_invalid_amount,
            "missing_metadata": self._fix_missing_metadata,
            "timeout": self._fix_timeout_issue,
            "race_condition": self._fix_race_condition
        }
    
    def detect_bugs(self, transaction: PaymentTransaction) -> List[BugReport]:
        """
        Detect bugs in a transaction
        
        Args:
            transaction: Transaction to analyze
            
        Returns:
            List of detected bugs
        """
        detected = []
        
        # Check for currency formatting issues
        if transaction.currency and not transaction.currency.isupper():
            bug_id = str(uuid.uuid4())
            bug = BugReport(
                bug_id=bug_id,
                severity="low",
                description=f"Currency code not uppercase: {transaction.currency}",
                component="transaction.currency",
                auto_fixable=True
            )
            detected.append(bug)
            self.bugs[bug_id] = bug
        
        # Check for precision issues in amount
        if isinstance(transaction.amount, float):
            decimal_places = len(str(transaction.amount).split('.')[-1]) if '.' in str(transaction.amount) else 0
            if decimal_places > 2:
                bug_id = str(uuid.uuid4())
                bug = BugReport(
                    bug_id=bug_id,
                    severity="medium",
                    description=f"Amount has too many decimal places: {transaction.amount}",
                    component="transaction.amount",
                    auto_fixable=True
                )
                detected.append(bug)
                self.bugs[bug_id] = bug
        
        # Check for missing critical metadata
        required_metadata = ["ip_address", "user_agent"]
        missing = [field for field in required_metadata if field not in transaction.metadata]
        if missing:
            bug_id = str(uuid.uuid4())
            bug = BugReport(
                bug_id=bug_id,
                severity="medium",
                description=f"Missing metadata fields: {', '.join(missing)}",
                component="transaction.metadata",
                auto_fixable=True
            )
            detected.append(bug)
            self.bugs[bug_id] = bug
        
        # Check for stuck transactions (processing too long)
        if transaction.status == PaymentStatus.PROCESSING:
            time_processing = (datetime.now() - transaction.timestamp).seconds
            if time_processing > 300:  # 5 minutes
                bug_id = str(uuid.uuid4())
                bug = BugReport(
                    bug_id=bug_id,
                    severity="high",
                    description=f"Transaction stuck in processing: {time_processing}s",
                    component="transaction.status",
                    auto_fixable=True
                )
                detected.append(bug)
                self.bugs[bug_id] = bug
        
        return detected
    
    def _fix_currency_mismatch(self, bug: BugReport, transaction: PaymentTransaction) -> bool:
        """Fix currency formatting issue"""
        transaction.currency = transaction.currency.upper()
        self.logger.info(f"Fixed currency formatting: {transaction.currency}")
        return True
    
    def _fix_invalid_amount(self, bug: BugReport, transaction: PaymentTransaction) -> bool:
        """Fix amount precision issue"""
        transaction.amount = round(transaction.amount, 2)
        self.logger.info(f"Fixed amount precision: {transaction.amount}")
        return True
    
    def _fix_missing_metadata(self, bug: BugReport, transaction: PaymentTransaction) -> bool:
        """Add default metadata for missing fields"""
        if "ip_address" not in transaction.metadata:
            transaction.metadata["ip_address"] = "unknown"
        if "user_agent" not in transaction.metadata:
            transaction.metadata["user_agent"] = "unknown"
        self.logger.info("Added missing metadata fields")
        return True
    
    def _fix_timeout_issue(self, bug: BugReport, transaction: PaymentTransaction) -> bool:
        """Fix timeout by resetting status"""
        transaction.status = PaymentStatus.PENDING
        self.logger.info(f"Reset stuck transaction: {transaction.transaction_id}")
        return True
    
    def _fix_race_condition(self, bug: BugReport, transaction: PaymentTransaction) -> bool:
        """Fix race condition by adding lock metadata"""
        transaction.metadata["lock"] = str(uuid.uuid4())
        self.logger.info(f"Applied race condition fix: {transaction.transaction_id}")
        return True
    
    def apply_fixes(self, transaction: PaymentTransaction) -> int:
        """
        Apply automated fixes to a transaction
        
        Args:
            transaction: Transaction to fix
            
        Returns:
            Number of fixes applied
        """
        bugs = self.detect_bugs(transaction)
        fixes_applied = 0
        
        for bug in bugs:
            if bug.auto_fixable:
                # Determine fix strategy based on bug description
                fix_applied = False
                
                if "currency" in bug.description.lower():
                    fix_applied = self._fix_currency_mismatch(bug, transaction)
                elif "decimal places" in bug.description.lower():
                    fix_applied = self._fix_invalid_amount(bug, transaction)
                elif "missing metadata" in bug.description.lower():
                    fix_applied = self._fix_missing_metadata(bug, transaction)
                elif "stuck" in bug.description.lower():
                    fix_applied = self._fix_timeout_issue(bug, transaction)
                
                if fix_applied:
                    bug.fixed = True
                    bug.fix_applied = "Automated fix applied"
                    fixes_applied += 1
                    self.logger.info(f"Fixed bug: {bug.bug_id}")
        
        return fixes_applied
    
    def get_unfixed_bugs(self) -> List[BugReport]:
        """Get all unfixed bugs"""
        return [bug for bug in self.bugs.values() if not bug.fixed]
    
    def get_critical_bugs(self) -> List[BugReport]:
        """Get all critical/high severity bugs"""
        return [bug for bug in self.bugs.values() 
                if bug.severity in ["critical", "high"] and not bug.fixed]
