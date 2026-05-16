# Restructure Plan - Tái Cấu Trúc Toàn Hệ Thống

**Date:** 2026-05-12 10:24 GMT+7  
**Status:** 🔄 PLANNING  
**Target:** Apply all skills + clean restructure to best practices

## 📊 Hiện Tại

```
E: drive (runtime-mirror)
├── .openclaw/workspace/
│   ├── .openclaw/            (hidden)
│   ├── config/               (minimal)
│   ├── examples/             (2 files)
│   ├── khai-thac/            (skill source)
│   ├── memory/               (daily logs)
│   ├── references/           (10 files, including new awesome-skills-catalog)
│   ├── reports/              (10 files)
│   ├── scripts/              (10 files)
│   ├── skills/               (3 custom skills + 1 built-in)
│   ├── utils/                (6 utilities)
│   ├── AGENTS.md
│   ├── IDENTITY.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   ├── USER.md
│   └── MEMORY.md             (nếu tồn tại)
```

## 🎯 Mục Tiêu Restructure

1. **Clean & Organize** - Sắp xếp lại theo best practices
2. **Deduplicate** - Xóa file trùng lặp, dư thừa
3. **Clarify Purpose** - Mỗi folder có mục đích rõ ràng
4. **Enhance Docs** - Thêm README.md vào mỗi folder chính
5. **Archive Old** - Move obsolete files to archive/deprecated
6. **Skill Integration** - Setup các skills như system tools
7. **Config Consolidation** - Merge/clean config files

## 📋 Chi Tiết Kế Hoạch

### Phase 1: Analysis & Backup
- [ ] Scan tất cả files & folders
- [ ] Identify duplicates, obsolete files
- [ ] Check file sizes & content
- [ ] Create backup list
- [ ] Plan archive strategy

### Phase 2: Core Config Cleanup
- [ ] Review & update AGENTS.md (core identity)
- [ ] Update SOUL.md (personality)
- [ ] Refresh IDENTITY.md (name, emoji, avatar)
- [ ] Consolidate USER.md (human info)
- [ ] Reorganize TOOLS.md (section structure)

### Phase 3: Skills Setup
- [ ] Audit all 4 skills (billing-guard, khai-thac, review-code, skill-creator)
- [ ] Setup skill manifest/registry
- [ ] Create skills/README.md (skill guide)
- [ ] Link skills to TOOLS.md
- [ ] Test skill discovery

### Phase 4: References Organization
- [ ] Organize references/ by category
- [ ] Add README to each reference group
- [ ] Update awesome-skills-catalog section
- [ ] Create quick-links file (QUICK-REF.md)
- [ ] Archive outdated references

### Phase 5: Utilities & Scripts Organization
- [ ] Clean utils/ (remove dupes)
- [ ] Add utils/README.md (library guide)
- [ ] Organize scripts/ by purpose
- [ ] Add scripts/README.md (script catalog)
- [ ] Create index for quick access

### Phase 6: Memory & Logging
- [ ] Organize memory/ structure (YYYY-MM-DD daily logs)
- [ ] Archive old memory logs (>3 months)
- [ ] Create memory/INDEX.md (navigation)
- [ ] Setup MEMORY.md properly (curated long-term)
- [ ] Add memory/README.md

### Phase 7: Examples & Templates
- [ ] Audit examples/ (keep only good ones)
- [ ] Add examples/README.md
- [ ] Create template registry
- [ ] Link examples to skills
- [ ] Archive unused templates

### Phase 8: Reports & Outputs
- [ ] Organize reports/ by type
- [ ] Create reports/README.md
- [ ] Setup reporting structure
- [ ] Archive old reports
- [ ] Create report templates

### Phase 9: Create New Structure Docs
- [ ] Create WORKSPACE.md (overall guide)
- [ ] Create DIRECTORY-MAP.md (visual structure)
- [ ] Create QUICK-START.md (new user guide)
- [ ] Create SKILL-REGISTRY.md (skills index)
- [ ] Create REFERENCE-INDEX.md (refs guide)

### Phase 10: Final Integration & Testing
- [ ] Verify all paths work
- [ ] Test skill discovery
- [ ] Validate config files
- [ ] Check memory access
- [ ] Create CHANGES.md (what changed & why)

## 🗂️ Target Structure

```
E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace/
│
├── 📖 CORE CONFIG (Identity & Setup)
│   ├── AGENTS.md                  (agent identity & behavior)
│   ├── SOUL.md                    (personality & values)
│   ├── IDENTITY.md                (name, emoji, avatar)
│   ├── USER.md                    (human context)
│   ├── MEMORY.md                  (curated long-term memory)
│   └── README.md                  (workspace overview)
│
├── 🛠️ TOOLS & SKILLS
│   ├── TOOLS.md                   (local setup notes)
│   ├── skills/
│   │   ├── README.md              (skill guide)
│   │   ├── SKILL-REGISTRY.md      (all skills list)
│   │   ├── billing-guard/
│   │   ├── khai-thac/
│   │   ├── review-code/
│   │   └── skill-creator/
│   ├── utils/
│   │   ├── README.md              (utilities guide)
│   │   ├── rate_limiter.py
│   │   ├── prompt_utils.py
│   │   └── ...
│   └── scripts/
│       ├── README.md              (scripts guide)
│       ├── model_usage.py
│       ├── tmux/
│       ├── video/
│       └── ...
│
├── 📚 REFERENCES & KNOWLEDGE
│   ├── README.md                  (references overview)
│   ├── QUICK-REF.md               (quick links)
│   ├── 1password/
│   ├── himalaya/
│   ├── model-usage/
│   ├── awesome-skills-catalog/
│   └── ...
│
├── 📝 MEMORY & LOGS
│   ├── README.md                  (memory guide)
│   ├── INDEX.md                   (navigation)
│   ├── memory/
│   │   ├── 2026-05-12-awesome-skills-intake.md
│   │   ├── heartbeat-state.json
│   │   └── ...
│   └── archives/
│       └── (old memory files >3 months)
│
├── 💡 EXAMPLES & TEMPLATES
│   ├── README.md                  (examples guide)
│   ├── inbox-triage.lobster
│   ├── pr-intake.lobster
│   └── templates/
│       └── (new template folder)
│
├── 📊 REPORTS & OUTPUT
│   ├── README.md                  (reports guide)
│   ├── reports/
│   │   └── (organized by date/type)
│   └── templates/
│       └── (report templates)
│
└── 📋 DOCUMENTATION
    ├── WORKSPACE.md               (overall guide)
    ├── DIRECTORY-MAP.md           (visual structure)
    ├── QUICK-START.md             (new user guide)
    ├── SKILL-REGISTRY.md          (skills index)
    ├── REFERENCE-INDEX.md         (references guide)
    ├── CHANGES.md                 (restructure log)
    └── RESTRUCTURE-PLAN.md        (this file)
```

## 🚀 Execution Order

### Week 1: Core (Phases 1-3)
1. Analysis & Backup → Identify everything
2. Core Config Cleanup → Setup identity right
3. Skills Setup → Make skills discoverable

### Week 1-2: Organization (Phases 4-8)
4. References Organization
5. Utilities & Scripts Organization
6. Memory & Logging Setup
7. Examples & Templates
8. Reports & Output Organization

### Week 2: Documentation (Phase 9)
9. Create Structure Documentation
   - WORKSPACE.md
   - DIRECTORY-MAP.md
   - QUICK-START.md
   - SKILL-REGISTRY.md
   - REFERENCE-INDEX.md

### Week 2 Final: Validation (Phase 10)
10. Final Integration & Testing
    - Test all paths
    - Verify skill discovery
    - Validate configs
    - Create CHANGES.md

## ⚠️ Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Data loss during move | Create full backup first |
| Broken file paths | Test all references after move |
| Skills stop working | Verify skill paths in config |
| Memory loss | Archive old files, don't delete |
| Config conflicts | Merge carefully, document changes |
| Duplicate files | Identify before cleanup |

## 📌 Important Notes

- ✅ Run on E: drive (confirmed available)
- ✅ All local, no cloud sync issues
- ✅ Backup strategy: archive/ folder for deprecated
- ✅ No downtime: can test offline first
- ✅ Documentation: every change logged in CHANGES.md

## 🎯 Success Criteria

After restructure:
- [ ] All configs in clear locations
- [ ] Each folder has README.md
- [ ] Skills are discoverable & documented
- [ ] References are organized by category
- [ ] Memory structure is clean & navigable
- [ ] Zero broken paths/links
- [ ] Full documentation in place
- [ ] CHANGES.md documents everything

## 📞 Next Steps

1. Approve this plan
2. Run Phase 1 (Analysis & Backup)
3. Continue with remaining phases
4. Validate at each phase
5. Final integration testing

---

**Ready to proceed?** Confirm and I'll start Phase 1.
