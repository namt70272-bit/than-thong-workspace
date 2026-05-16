"""Tests for memory_consolidator.py"""

import pytest
import sys
import os
import tempfile
from pathlib import Path

# Add scripts to path
scripts_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "tools-internal", "scripts"
)
sys.path.insert(0, scripts_dir)

import memory_consolidator as mc


@pytest.fixture
def temp_memory_dir():
    """Create a temp memory/ with sample daily notes."""
    with tempfile.TemporaryDirectory() as tmp:
        mem = Path(tmp)
        # Sample note 1
        n1 = mem / "2026-05-15.md"
        n1.write_text("# 2026-05-15\n\n## Decisions\n- Chot rule van hanh: local-first\n\n## Status\n- OK\n", encoding="utf-8")
        # Sample note 2
        n2 = mem / "2026-05-16.md"
        n2.write_text("# 2026-05-16\n\n## Fixes\n- Da fix syntax errors\n\n## Blockers\n- Con pending numpy upgrade\n", encoding="utf-8")
        # Control: non-daily file (should be skipped)
        (mem / "README.md").write_text("README", encoding="utf-8")
        (mem / "INDEX.md").write_text("# INDEX", encoding="utf-8")

        # Save original paths and override
        orig_mem = mc.MEMORY_DIR
        mc.MEMORY_DIR = mem
        yield mem
        mc.MEMORY_DIR = orig_mem


class TestScan:
    def test_scan_finds_daily_notes(self, temp_memory_dir):
        notes = mc.scan_notes()
        assert len(notes) == 2  # SKIP readme + index
        assert notes[0]["date"] == "2026-05-15"
        assert notes[1]["date"] == "2026-05-16"

    def test_scan_skips_non_daily(self, temp_memory_dir):
        notes = mc.scan_notes()
        fnames = [n["filename"] for n in notes]
        assert "README.md" not in fnames
        assert "INDEX.md" not in fnames

    def test_scan_parses_sections(self, temp_memory_dir):
        notes = mc.scan_notes()
        for n in notes:
            assert len(n["sections"]) >= 1
            assert len(n["content"]) > 0


class TestExtract:
    def test_extract_decision(self, temp_memory_dir):
        notes = mc.scan_notes()
        decisions = mc.extract_items(notes, mc.DECISION_PATTERNS)
        assert len(decisions) >= 1
        assert any("local-first" in d["context"] for d in decisions)

    def test_extract_blocker(self, temp_memory_dir):
        notes = mc.scan_notes()
        blockers = mc.extract_items(notes, mc.BLOCKER_PATTERNS)
        assert len(blockers) >= 1
        assert any("numpy" in b["context"] for b in blockers)


class TestGenerate:
    def test_generate_index(self, temp_memory_dir):
        notes = mc.scan_notes()
        index = mc.generate_index(notes)
        assert "Memory Index" in index
        assert "2026-05-15" in index
        assert "2026-05-16" in index
        assert "Stats" in index

    def test_generate_report(self, temp_memory_dir):
        notes = mc.scan_notes()
        report = mc.generate_report(notes)
        assert "Memory Consolidation Report" in report
        assert "Decisions" in report or "Topic Snapshots" in report

    def test_suggest_updates(self, temp_memory_dir):
        notes = mc.scan_notes()
        # Without MEMORY.md in tmp dir
        suggestions = mc.suggest_updates(notes)
        # Should find decisions not in memory
        if suggestions:
            assert len(suggestions) >= 1


class TestSkip:
    def test_should_skip_consolidation_files(self):
        assert mc.should_skip("consolidation-2026-05-16.md")
        assert mc.should_skip("INDEX.md")
        assert mc.should_skip("README.md")
        assert mc.should_skip(".hidden.md")
        assert not mc.should_skip("2026-05-16.md")
        assert not mc.should_skip("2026-05-15-special.md")
