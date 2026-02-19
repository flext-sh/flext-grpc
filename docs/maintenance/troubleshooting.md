# Documentation Maintenance Troubleshooting Guide


<!-- TOC START -->
- [Table of Contents](#table-of-contents)
- [Quick Diagnosis](#quick-diagnosis)
  - [System Health Check](#system-health-check)
  - [Quick Health Assessment](#quick-health-assessment)
  - [Check for Critical Issues](#check-for-critical-issues)
  - [Verify System Components](#verify-system-components)
  - [Common Symptoms and Solutions](#common-symptoms-and-solutions)
- [🔍 Audit Issues](#audit-issues)
  - [Symptom: Audit fails with import errors](#symptom-audit-fails-with-import-errors)
  - [Install Missing Dependencies](#install-missing-dependencies)
  - [Or Install Individually](#or-install-individually)
  - [Verify Installation](#verify-installation)
  - [Symptom: Audit reports low quality scores](#symptom-audit-reports-low-quality-scores)
  - [Check Current Configuration](#check-current-configuration)
  - [Run Detailed Audit](#run-detailed-audit)
  - [Adjust Quality Thresholds if Needed](#adjust-quality-thresholds-if-needed)
  - [Or Fix Content Issues](#or-fix-content-issues)
  - [Symptom: Audit finds false positives](#symptom-audit-finds-false-positives)
- [🔗 Validation Issues](#validation-issues)
  - [Symptom: Link validation times out](#symptom-link-validation-times-out)
  - [Symptom: False broken link reports](#symptom-false-broken-link-reports)
  - [Symptom: Style validation too strict](#symptom-style-validation-too-strict)
- [🔧 Optimization Issues](#optimization-issues)
  - [Symptom: Optimization doesn't apply changes](#symptom-optimization-doesnt-apply-changes)
  - [Symptom: Table of contents not generating](#symptom-table-of-contents-not-generating)
- [🔄 Synchronization Issues](#synchronization-issues)
  - [Symptom: Git operations fail](#symptom-git-operations-fail)
  - [Symptom: Merge conflicts in documentation](#symptom-merge-conflicts-in-documentation)
- [📊 Reporting Issues](#reporting-issues)
  - [Symptom: Reports not generating](#symptom-reports-not-generating)
  - [Symptom: Dashboard not displaying correctly](#symptom-dashboard-not-displaying-correctly)
- [🚨 Critical Issues](#critical-issues)
  - [Symptom: System completely broken](#symptom-system-completely-broken)
  - [Symptom: Data corruption in reports](#symptom-data-corruption-in-reports)
- [🔧 Advanced Troubleshooting](#advanced-troubleshooting)
  - [Debug Mode](#debug-mode)
  - [Performance Issues](#performance-issues)
  - [Memory Issues](#memory-issues)
- [🆘 Getting Help](#getting-help)
  - [Self-Diagnosis Checklist](#self-diagnosis-checklist)
  - [Diagnostic Commands](#diagnostic-commands)
  - [Log Analysis](#log-analysis)
  - [Community Support](#community-support)
- [🚀 Preventive Maintenance](#preventive-maintenance)
  - [Regular Tasks](#regular-tasks)
  - [Configuration Validation](#configuration-validation)
  - [Dependency Updates](#dependency-updates)
- [📋 Recovery Procedures](#recovery-procedures)
  - [Data Recovery](#data-recovery)
  - [Configuration Recovery](#configuration-recovery)
  - [System Recovery](#system-recovery)
<!-- TOC END -->

## Table of Contents

- Documentation Maintenance Troubleshooting Guide
  - Quick Diagnosis
    - System Health Check
- Quick Health Assessment
- Check for Critical Issues
- Verify System Components
  - Common Symptoms and Solutions
  - 🔍 Audit Issues
    - Symptom: Audit fails with import errors
- Install Missing Dependencies
- Or Install Individually
- Verify Installation
  - Symptom: Audit reports low quality scores
- Check Current Configuration
- Run Detailed Audit
- Adjust Quality Thresholds if Needed
- Edit docs/maintenance/config.JSON
- Or fix content issues
  - Symptom: Audit finds false positives
- Create custom audit rules
- docs/maintenance/custom_rules.py
  - 🔗 Validation Issues
    - Symptom: Link validation times out
- Increase timeout in config
- Edit docs/maintenance/config.JSON
- Or exclude problematic domains
  - Symptom: False broken link reports
- Add to ignore patterns
- docs/maintenance/config.JSON
  - Symptom: Style validation too strict
- Adjust style rules
- docs/maintenance/config.JSON
  - 🔧 Optimization Issues
    - Symptom: Optimization doesn't apply changes
- Check file permissions
- Check if dry-run is enabled
- Fix permissions
- Run without dry-run
- Or run with explicit file
  - Symptom: Table of contents not generating
- Check heading count
- Adjust TOC settings
- docs/maintenance/config.JSON
  - 🔄 Synchronization Issues
    - Symptom: Git operations fail
- Check git status
- Configure git user (if needed)
- Check repository state
  - Symptom: Merge conflicts in documentation
- Check for conflicts
- Resolve manually or use automated resolution
- Create backup before resolving
  - 📊 Reporting Issues
    - Symptom: Reports not generating
- Ensure reports directory exists
- Run audit first
- Then generate report
  - Symptom: Dashboard not displaying correctly
- Check dashboard file
- Regenerate dashboard
- Open in browser
  - 🚨 Critical Issues
    - Symptom: System completely broken
- Complete system reset
- Reinstall dependencies
- Verify system integrity
  - Symptom: Data corruption in reports
- Clear corrupted reports
- Restore from backup
- Regenerate reports
  - 🔧 Advanced Troubleshooting
    - Debug Mode
- Enable debug logging
- Run with verbose output
- Check debug logs
  - Performance Issues
- Profile execution time
- Check for bottlenecks
  - Memory Issues
- Monitor memory usage
- Kill if needed
  - 🆘 Getting Help
    - Self-Diagnosis Checklist
    - Diagnostic Commands
- System information
- Repository status
- File system check
- Network connectivity
  - Log Analysis
- Check recent errors
- Analyze performance
- Check for patterns
  - Community Support
  - 🚀 Preventive Maintenance
    - Regular Tasks
- Weekly system health
- Monthly deep analysis
- Daily backup
  - Configuration Validation
- Validate configuration
- Check for deprecated settings
  - Dependency Updates
- Update dependencies
- Check for security vulnerabilities
- Test after updates
  - 📋 Recovery Procedures
    - Data Recovery
- From automatic backup
- From git history
- From manual backup
  - Configuration Recovery
- Reset to defaults
- Merge with custom settings
- Edit manually or use merge tool
  - System Recovery
- Complete rebuild
- Verify recovery

**Version**: 1.0.0 | **Last Updated**: 2025-10-10

Comprehensive troubleshooting guide for the FLEXT-gRPC Documentation Maintenance Framework.

## Quick Diagnosis

### System Health Check

```bash
### Quick Health Assessment
make docs DOCS_PHASE=audit

### Check for Critical Issues
make docs

### Verify System Components
python -c "
import sys
sys.path.insert(0, 'docs/maintenance')
from audit import DocumentationAuditor
from validation import DocumentationValidator
from optimization import DocumentationOptimizer
print('✅ All components importable')
"
```

### Common Symptoms and Solutions

## 🔍 Audit Issues

### Symptom: Audit fails with import errors

**Error:**

```yaml
ModuleNotFoundError: No module named 'frontmatter'
```

**Solution:**

```bash
### Install Missing Dependencies
pip install -r docs/maintenance/requirements.txt

### Or Install Individually
pip install python-frontmatter requests beautifulsoup4 markdown

### Verify Installation
python -c "import frontmatter, requests, markdown; print('✅ Dependencies installed')"
```

### Symptom: Audit reports low quality scores

**Cause:** Configuration thresholds too strict or content issues

**Diagnosis:**

```bash
### Check Current Configuration
cat docs/maintenance/config.JSON | jq '.audit.quality_thresholds'

### Run Detailed Audit
PYTHONPATH=. python docs/maintenance/audit.py --verbose
```

**Solution:**

```bash
### Adjust Quality Thresholds if Needed
# Edit docs/maintenance/config.JSON
{
  "audit": {
    "quality_thresholds": {
      "excellent": 85,  // Lowered from 90
      "good": 75        // Lowered from 80
    }
  }
}

### Or Fix Content Issues
make docs
```

### Symptom: Audit finds false positives

**Cause:** Custom content patterns not recognized

**Solution:**

```python
# Create custom audit rules
# docs/maintenance/custom_rules.py
CUSTOM_AUDIT_RULES = {
    "ignore_patterns": ["<!-- ignore-audit -->"],
    "custom_headings": ["Changelog", "Migration Guide"],
    "project_terms": ["gRPC", "FLEXT", "protobuf"]
}
```

## 🔗 Validation Issues

### Symptom: Link validation times out

**Error:**

```yaml
TimeoutError: Request timed out
```

**Solution:**

```bash
# Increase timeout in config
# Edit docs/maintenance/config.JSON
{
  "validation": {
    "link_timeout": 30,  // Increased from 10
    "max_concurrent_checks": 3  // Reduced from 5
  }
}

# Or exclude problematic domains
{
  "validation": {
    "ignore_patterns": [
      "localhost",
      "127.0.0.1",
      "*.internal.company.com"
    ]
  }
}
```

### Symptom: False broken link reports

**Cause:** Dynamic URLs or authentication requirements

**Solution:**

```bash
# Add to ignore patterns
# docs/maintenance/config.JSON
{
  "validation": {
    "ignore_patterns": [
      "https://github.com/user/repo/pull/*",
      "https://company.jira.com/browse/*",
      "https://internal.docs.company.com/*"
    ]
  }
}
```

### Symptom: Style validation too strict

**Error:**

```
Line too long (120 > 88 characters)
```

**Solution:**

```bash
# Adjust style rules
# docs/maintenance/config.JSON
{
  "style": {
    "max_line_length": 120,  // Increased from 88
    "list_consistency": false  // Disabled if causing issues
  }
}
```

## 🔧 Optimization Issues

### Symptom: Optimization doesn't apply changes

**Cause:** File permissions or dry-run mode

**Diagnosis:**

```bash
# Check file permissions
ls -la docs/README.md

# Check if dry-run is enabled
grep -A5 "dry_run" docs/maintenance/optimization.py
```

**Solution:**

```bash
# Fix permissions
chmod 644 docs/README.md

# Run without dry-run
PYTHONPATH=. python docs/maintenance/optimization.py

# Or run with explicit file
PYTHONPATH=. python docs/maintenance/optimization.py --file docs/README.md
```

### Symptom: Table of contents not generating

**Cause:** Insufficient headings or configuration

**Solution:**

```bash
# Check heading count
grep -c "^#" docs/README.md

# Adjust TOC settings
# docs/maintenance/config.JSON
{
  "optimization": {
    "toc_min_headings": 2,  // Reduced from 4
    "max_toc_depth": 4      // Increased from 3
  }
}
```

## 🔄 Synchronization Issues

### Symptom: Git operations fail

**Error:**

```yaml
GitCommandError: 'git commit' failed
```

**Solution:**

```bash
# Check git status
git status

# Configure git user (if needed)
git config user.name "Documentation Maintenance"
git config user.email "docs@internal.invalid"

# Check repository state
git log --oneline -5
```

### Symptom: Merge conflicts in documentation

**Cause:** Concurrent edits to same files

**Solution:**

```bash
# Check for conflicts
git status | grep "both modified"

# Resolve manually or use automated resolution
PYTHONPATH=. python docs/maintenance/sync.py --action resolve-conflicts

# Create backup before resolving
make docs
```

## 📊 Reporting Issues

### Symptom: Reports not generating

**Error:**

```yaml
FileNotFoundError: No audit report found
```

**Solution:**

```bash
# Ensure reports directory exists
mkdir -p docs/maintenance/reports

# Run audit first
make docs DOCS_PHASE=audit

# Then generate report
make docs
```

### Symptom: Dashboard not displaying correctly

**Cause:** Missing CSS or JavaScript

**Solution:**

```bash
# Check dashboard file
cat docs/maintenance/dashboard.html | head -20

# Regenerate dashboard
make docs

# Open in browser
firefox docs/maintenance/dashboard.html
```

## 🚨 Critical Issues

### Symptom: System completely broken

**Emergency Reset:**

```bash
# Complete system reset
make docs

# Reinstall dependencies
pip install -r docs/maintenance/requirements.txt

# Verify system integrity
python docs/maintenance/audit.py --test-system
```

### Symptom: Data corruption in reports

**Recovery:**

```bash
# Clear corrupted reports
rm -rf docs/maintenance/reports/*.json

# Restore from backup
make docs

# Regenerate reports
make docs
```

## 🔧 Advanced Troubleshooting

### Debug Mode

```bash
# Enable debug logging
export DOCS_DEBUG=true
export DOCS_LOG_LEVEL=DEBUG

# Run with verbose output
PYTHONPATH=. python docs/maintenance/audit.py --debug

# Check debug logs
tail -f docs/maintenance/logs/debug.log
```

### Performance Issues

```bash
# Profile execution time
time make docs

# Check for bottlenecks
PYTHONPATH=. python -c "
import cProfile
cProfile.run('from docs.maintenance.audit import DocumentationAuditor; a = DocumentationAuditor(); a.run_audit()')
"
```

### Memory Issues

```bash
# Monitor memory usage
PYTHONPATH=. python docs/maintenance/audit.py &
PID=$$!
ps aux | grep $$PID

# Kill if needed
kill $$PID
```

## 🆘 Getting Help

### Self-Diagnosis Checklist

- [ ] Python version ≥ 3.8
- [ ] All dependencies installed
- [ ] File permissions correct
- [ ] Git repository clean
- [ ] Configuration file valid

### Diagnostic Commands

```bash
# System information
python --version
pip list | grep -E "(requests|markdown|frontmatter)"

# Repository status
git status --porcelain
git log --oneline -5

# File system check
find docs/ -name "*.md" | wc -l
ls -la docs/maintenance/

# Network connectivity
curl -I https://github.com
```

### Log Analysis

```bash
# Check recent errors
grep -r "ERROR\|CRITICAL" docs/maintenance/logs/

# Analyze performance
grep "took" docs/maintenance/logs/*.log | tail -10

# Check for patterns
grep -c "failed\|error" docs/maintenance/logs/*.log
```

### Community Support

1. **Check Existing Issues**

   ```bash
   # Search in issue tracker
   gh issue list --search "maintenance framework"
   ```

2. **Gather Diagnostic Information**

   ```bash
   # Create diagnostic bundle
   tar -czf diagnostic_$(date +%Y%m%d).tar.gz \
     docs/maintenance/logs/ \
     docs/maintenance/config.JSON \
     docs/maintenance/reports/ \
     --exclude="*.cache"
   ```

3. **Report Template**

```yaml
Issue: [Brief description]
Steps to reproduce: [Commands executed]
Expected behavior: [What should happen]
Actual behavior: [What actually happens]
System info: [Python version, OS, etc.]
Logs: [Relevant log excerpts]
```

## 🚀 Preventive Maintenance

### Regular Tasks

```bash
# Weekly system health
0 9 * * 1 make docs

# Monthly deep analysis
0 10 1 * * make docs

# Daily backup
0 2 * * * make docs
```

### Configuration Validation

```bash
# Validate configuration
python -c "
import json
config = json.load(open('docs/maintenance/config.JSON'))
print('✅ Configuration valid')
"

# Check for deprecated settings
grep -r "deprecated\|obsolete" docs/maintenance/config.JSON
```

### Dependency Updates

```bash
# Update dependencies
pip install --upgrade -r docs/maintenance/requirements.txt

# Check for security vulnerabilities
pip audit

# Test after updates
make docs DOCS_PHASE=audit
```

## 📋 Recovery Procedures

### Data Recovery

```bash
# From automatic backup
make docs

# From git history
git checkout HEAD~1 -- docs/
git checkout <commit-hash> -- docs/maintenance/reports/

# From manual backup
tar -xzf docs/maintenance/backups/docs_backup_*.tar.gz
```

### Configuration Recovery

```bash
# Reset to defaults
cp docs/maintenance/config.default.json docs/maintenance/config.JSON

# Merge with custom settings
# Edit manually or use merge tool
```

### System Recovery

```bash
# Complete rebuild
make docs
make docs
make docs

# Verify recovery
make docs DOCS_PHASE=audit
```

---

**Remember**: Most issues can be resolved by checking logs, verifying configuration,
and ensuring dependencies are installed. For persistent problems,
gather diagnostic information and create a detailed issue report.
