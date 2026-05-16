---
name: review-code
description: Generate structured PR/staged review comments using AI agents. No GitHub auth required - uses local diff analysis.
---

# Review Code Skill

Analyze code changes and generate structured review feedback.

## Usage

```
/review <path>         # Review changes in path
/review <path> --post  # Post review (when GitHub available)
```

## What this skill does

1. **Reads diff/changes** from the specified path
2. **Architectural review**: Questions design decisions, checks scope
3. **Analyzes changes**: security, testing, design patterns, code quality
4. **Generates structured feedback**: Specific suggestions with file/line references
5. **Educational focus**: Explains "why" behind recommendations
6. **Balanced**: Acknowledges good practices alongside improvements

## Review checklist

- [ ] Architecture/design decisions aligned with project goals
- [ ] Security: input validation, secrets, permissions
- [ ] Testing: coverage, edge cases, integration
- [ ] Code quality: KISS, DRY, SOLID, YAGNI
- [ ] Dependencies: necessary? versions pinned?
- [ ] Documentation: README, comments, changelog

## Notes

- Adapted from Microsoft Agent365 devTools review-pr Claude skill
- Works fully local, no external API required
- Uses OpenClaw built-in tools for file/diff analysis
