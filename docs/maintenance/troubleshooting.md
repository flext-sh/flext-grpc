# Documentation Maintenance Troubleshooting Guide

**Version**: 1.0.0 | **Last Updated**: 2025-10-10

Comprehensive troubleshooting guide for the FLEXT-gRPC Documentation Maintenance Framework.

## Quick Diagnosis

### System Health Check

```bash
# Quick health assessment
make docs-health

# Check for critical issues
make docs-notify-critical

# Verify system components
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

```
ModuleNotFoundError: No module named 'frontmatter'
```

**Solution:**

```bash
# Install missing dependencies
pip install -r docs/maintenance/requirements.txt

# Or install individually
pip install python-frontmatter requests beautifulsoup4 markdown

# Verify installation
python -c "import frontmatter, requests, markdown; print('✅ Dependencies installed')"
```

### Symptom: Audit reports low quality scores

**Cause:** Configuration thresholds too strict or content issues

**Diagnosis:**

```bash
# Check current configuration
cat docs/maintenance/config.json | jq '.audit.quality_thresholds'

# Run detailed audit
PYTHONPATH=. python docs/maintenance/audit.py --verbose
```

**Solution:**

```bash
# Adjust quality thresholds if needed
# Edit docs/maintenance/config.json
{
  "audit": {
    "quality_thresholds": {
      "excellent": 85,  // Lowered from 90
      "good": 75        // Lowered from 80
    }
  }
}

# Or fix content issues
make docs-fix
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

```
TimeoutError: Request timed out
```

**Solution:**

```bash
# Increase timeout in config
# Edit docs/maintenance/config.json
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
# docs/maintenance/config.json
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
# docs/maintenance/config.json
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
# docs/maintenance/config.json
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

```
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
make docs-backup
```

## 📊 Reporting Issues

### Symptom: Reports not generating

**Error:**

```
FileNotFoundError: No audit report found
```

**Solution:**

```bash
# Ensure reports directory exists
mkdir -p docs/maintenance/reports

# Run audit first
make docs-audit

# Then generate report
make docs-report
```

### Symptom: Dashboard not displaying correctly

**Cause:** Missing CSS or JavaScript

**Solution:**

```bash
# Check dashboard file
cat docs/maintenance/dashboard.html | head -20

# Regenerate dashboard
make docs-dashboard

# Open in browser
firefox docs/maintenance/dashboard.html
```

## 🚨 Critical Issues

### Symptom: System completely broken

**Emergency Reset:**

```bash
# Complete system reset
make docs-emergency-reset

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
make docs-restore

# Regenerate reports
make docs-maintenance
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
time make docs-maintenance

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
     docs/maintenance/config.json \
     docs/maintenance/reports/ \
     --exclude="*.cache"
   ```

3. **Report Template**

   ```
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
0 9 * * 1 make docs-weekly-audit

# Monthly deep analysis
0 10 1 * * make docs-monthly-analysis

# Daily backup
0 2 * * * make docs-backup
```

### Configuration Validation

```bash
# Validate configuration
python -c "
import json
config = json.load(open('docs/maintenance/config.json'))
print('✅ Configuration valid')
"

# Check for deprecated settings
grep -r "deprecated\|obsolete" docs/maintenance/config.json
```

### Dependency Updates

```bash
# Update dependencies
pip install --upgrade -r docs/maintenance/requirements.txt

# Check for security vulnerabilities
pip audit

# Test after updates
make docs-health
```

## 📋 Recovery Procedures

### Data Recovery

```bash
# From automatic backup
make docs-restore

# From git history
git checkout HEAD~1 -- docs/
git checkout <commit-hash> -- docs/maintenance/reports/

# From manual backup
tar -xzf docs/maintenance/backups/docs_backup_*.tar.gz
```

### Configuration Recovery

```bash
# Reset to defaults
cp docs/maintenance/config.default.json docs/maintenance/config.json

# Merge with custom settings
# Edit manually or use merge tool
```

### System Recovery

```bash
# Complete rebuild
make docs-emergency-reset
make docs-dev-setup
make docs-maintenance

# Verify recovery
make docs-health
```

---

**Remember**: Most issues can be resolved by checking logs, verifying configuration, and ensuring dependencies are installed. For persistent problems, gather diagnostic information and create a detailed issue report.
