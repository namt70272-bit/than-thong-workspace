"""
Governor billing guard integration.
Hooks RateGovernor with billing-guard skill rules.

Usage:
    from utils.governor_billing import GovernorWithBilling
    g = GovernorWithBilling()
    
    # Check before making LLM call
    if g.can_proceed("deepseek/deepseek-chat"):
        # Make call
        g.record_call(cost_cents=0.5)
    else:
        # Blocked by budget
        pass
"""
import os
import logging
from typing import Optional

from .rate_governor import Governor

logger = logging.getLogger(__name__)

_BUDGET_ENV_KEY = "LLM_DAILY_BUDGET_CENTS"
_APPROVED_MODELS_KEY = "LLM_APPROVED_MODELS"  # comma-separated
_BILLING_MODE = "LLM_BILLING_MODE"  # dry-run | live | audit


class GovernorWithBilling(Governor):
    """Extended Governor with billing-guard compliance.

    - dry-run mode: log costs but never block
    - live mode: block when budget exceeded
    - audit mode: allow but log all for later review
    """

    def __init__(self):
        super().__init__()
        self._billing_mode = os.environ.get(_BILLING_MODE, "live")
        self._approved_models = set(
            m.strip() for m in os.environ.get(_APPROVED_MODELS_KEY, "").split(",")
            if m.strip()
        )
        self._billing_state = {}
        logger.info(
            "GovernorWithBilling: mode=%s, approved_models=%s, budget=%d",
            self._billing_mode,
            self._approved_models or "all",
            self._daily_budget,
        )

    def can_proceed(self, model: Optional[str] = None) -> bool:
        """Check if call can proceed under billing guard rules.

        Returns True if:
        - billing mode is dry-run or audit
        - model is approved
        - budget not exceeded (live mode only)
        - circuit breaker is closed
        """
        # dry-run/audit: always allow (but log)
        if self._billing_mode in ("dry-run", "audit"):
            return True

        # live mode: check budget
        if self._daily_budget > 0:
            bill = self._state.get("billing", {})
            if bill.get("today_spent_cents", 0) >= self._daily_budget:
                logger.warning(
                    "Billing guard BLOCKED: %d/%d cents spent today on model=%s",
                    bill["today_spent_cents"], self._daily_budget, model or "any",
                )
                return False

        # Check approved models
        if self._approved_models and model:
            if not any(m in model for m in self._approved_models):
                logger.warning(
                    "Billing guard BLOCKED: model=%s not in approved list %s",
                    model, self._approved_models,
                )
                return False

        # Circuit breaker
        if self._is_circuit_open():
            return False

        return True

    def wait_if_needed(self, **kwargs) -> bool:
        """Override: add billing guard check before rate limit wait."""
        model = kwargs.get("model")
        cost_cents = kwargs.get("cost_cents", 0)

        if not self.can_proceed(model):
            return False

        # In dry-run, skip actual wait
        if self._billing_mode == "dry-run" and cost_cents > 0:
            self.record_call(cost_cents=cost_cents, model=model)
            return True

        return super().wait_if_needed(**kwargs)
