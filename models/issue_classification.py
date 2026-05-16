# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Ported from Agent365-devTools (autoTriage/models/issue_classification.py)
# — stripped GitHub/ADO coupling, kept core data classes.

"""
Issue Classification Models
— Dùng cho LLM classification, triage, fix suggestions.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TriageRationale:
    """Detailed rationale cho từng quyết định triage."""
    type_rationale: str = ""
    priority_rationale: str = ""
    copilot_rationale: str = ""
    assignment_rationale: str = ""
    labels_rationale: str = ""

    def to_dict(self) -> dict:
        return {
            "type_rationale": self.type_rationale,
            "priority_rationale": self.priority_rationale,
            "copilot_rationale": self.copilot_rationale,
            "assignment_rationale": self.assignment_rationale,
            "labels_rationale": self.labels_rationale,
        }

    def to_summary(self) -> str:
        parts = []
        if self.type_rationale:
            parts.append(f"**Type:** {self.type_rationale}")
        if self.priority_rationale:
            parts.append(f"**Priority:** {self.priority_rationale}")
        if self.copilot_rationale:
            parts.append(f"**Copilot:** {self.copilot_rationale}")
        if self.assignment_rationale:
            parts.append(f"**Assignment:** {self.assignment_rationale}")
        if self.labels_rationale:
            parts.append(f"**Labels:** {self.labels_rationale}")
        return "\n".join(parts) if parts else "No rationale provided"

    @staticmethod
    def from_dict(data: dict) -> "TriageRationale":
        return TriageRationale(
            type_rationale=data.get("type_rationale", ""),
            priority_rationale=data.get("priority_rationale", ""),
            copilot_rationale=data.get("copilot_rationale", ""),
            assignment_rationale=data.get("assignment_rationale", ""),
            labels_rationale=data.get("labels_rationale", ""),
        )


@dataclass
class IssueClassification:
    """Kết quả classification của LLM."""
    issue_url: str = ""
    issue_number: int = 0
    issue_type: str = "unknown"  # bug, feature, question, documentation
    priority: str = "P3"  # P0–P4
    suggested_labels: list[str] = field(default_factory=list)
    suggested_assignee: Optional[str] = None
    is_copilot_fixable: bool = False
    reason: str = ""
    confidence: float = 0.0
    rationale: TriageRationale = field(default_factory=TriageRationale)
    fix_suggestions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "issue_number": self.issue_number,
            "issue_url": self.issue_url,
            "issue_type": self.issue_type,
            "priority": self.priority,
            "suggested_labels": self.suggested_labels,
            "suggested_assignee": self.suggested_assignee,
            "is_copilot_fixable": self.is_copilot_fixable,
            "reason": self.reason,
            "confidence": self.confidence,
            "rationale": self.rationale.to_dict(),
            "fix_suggestions": self.fix_suggestions,
        }

    @staticmethod
    def from_dict(data: dict, issue_number: int = 0, issue_url: str = "") -> "IssueClassification":
        rationale_data = data.get("rationale", {})
        return IssueClassification(
            issue_url=issue_url or data.get("issue_url", ""),
            issue_number=issue_number or data.get("issue_number", 0),
            issue_type=data.get("issue_type", "unknown"),
            priority=data.get("priority", "P3"),
            suggested_labels=data.get("suggested_labels", []),
            suggested_assignee=data.get("suggested_assignee") or data.get("assignee"),
            is_copilot_fixable=data.get("is_copilot_fixable", False),
            reason=data.get("reason", ""),
            confidence=float(data.get("confidence", 0.0)),
            rationale=TriageRationale.from_dict(rationale_data) if rationale_data else TriageRationale(),
            fix_suggestions=data.get("fix_suggestions", []),
        )
