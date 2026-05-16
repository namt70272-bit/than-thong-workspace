# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Ported from Agent365-devTools (autoTriage/models/team_config.py)
# — stripped ADO coupling, kept core config data classes.

"""
Team Configuration Models
— Dùng cho LLM classification, priority rules, Copilot config.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PriorityRules:
    """Rules for determining issue priority."""
    p0_keywords: list[str] = field(
        default_factory=lambda: ["crash", "outage", "security", "data loss"]
    )
    p1_keywords: list[str] = field(
        default_factory=lambda: ["bug", "broken", "error"]
    )
    p2_keywords: list[str] = field(
        default_factory=lambda: ["enhancement", "feature"]
    )
    p3_keywords: list[str] = field(
        default_factory=lambda: ["minor", "low"]
    )
    p4_keywords: list[str] = field(
        default_factory=lambda: ["trivial", "nice-to-have"]
    )
    default_priority: str = "P3"


@dataclass
class CopilotFixableConfig:
    """Configuration for Copilot/agent-fixable issue detection."""
    enabled: bool = False
    criteria: list[str] = field(
        default_factory=lambda: [
            "typo", "simple fix", "documentation",
            "good first issue",
        ]
    )
    max_issues_per_day: int = 5


@dataclass
class TriageMeta:
    """Triage behavior configuration."""
    auto_assign: bool = True
    auto_label: bool = True
    copilot_enabled: bool = False
    copilot_max_issues_per_day: int = 5


@dataclass
class SecurityConfig:
    """Security issue detection config."""
    keywords: list[str] = field(
        default_factory=lambda: [
            "vulnerability", "CVE", "security", "exploit", "injection",
            "XSS", "CSRF", "SQL injection", "auth bypass",
        ]
    )
    assignee: str = ""
    default_priority: str = "P1"


@dataclass
class TeamConfig:
    """Complete team configuration."""
    repo: str = ""
    owner: str = ""
    team_name: str = ""
    standup_time: str = "09:00"
    timezone: str = "America/Los_Angeles"
    priority_rules: PriorityRules = field(default_factory=PriorityRules)
    copilot_fixable: CopilotFixableConfig = field(default_factory=CopilotFixableConfig)
    triage_meta: TriageMeta = field(default_factory=TriageMeta)
    labels: dict = field(default_factory=dict)
    team_members: list[dict] = field(default_factory=list)
    copilot_fixable_labels: list[str] = field(default_factory=list)
    features_enabled: dict = field(default_factory=dict)
    security: Optional[SecurityConfig] = None
    sla_hours: Optional[dict] = None
    escalation_chain: Optional[dict] = None

    @property
    def assignees(self) -> list[str]:
        return [m.get("login") for m in self.team_members if m.get("login")]

    def is_copilot_enabled(self) -> bool:
        return self.triage_meta.copilot_enabled
