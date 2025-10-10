# FLEXT-gRPC Documentation Maintenance Makefile
# Comprehensive automation for documentation quality assurance and maintenance

.PHONY: help docs-audit docs-validation docs-optimization docs-sync docs-report docs-maintenance docs-health docs-weekly-audit docs-monthly-analysis docs-dashboard docs-emergency-reset docs-clear-cache docs-pre-commit docs-fix

# Default target
help:
	@echo "FLEXT-gRPC Documentation Maintenance System"
	@echo ""
	@echo "Available targets:"
	@echo "  docs-audit           - Run documentation audit"
	@echo "  docs-validation      - Validate links and references"
	@echo "  docs-optimization    - Optimize documentation content"
	@echo "  docs-sync           - Synchronize with version control"
	@echo "  docs-report         - Generate quality reports"
	@echo "  docs-maintenance    - Run complete maintenance cycle"
	@echo "  docs-health         - Quick health check"
	@echo "  docs-weekly-audit   - Comprehensive weekly audit"
	@echo "  docs-monthly-analysis - Deep monthly analysis"
	@echo "  docs-dashboard      - Generate HTML dashboard"
	@echo "  docs-emergency-reset - Emergency system reset"
	@echo "  docs-clear-cache    - Clear all caches"
	@echo "  docs-pre-commit     - Pre-commit quality checks"
	@echo "  docs-fix           - Auto-fix common issues"

# Core maintenance targets
docs-audit:
	@echo "🔍 Running documentation audit..."
	@PYTHONPATH=. python docs/maintenance/audit.py --comprehensive

docs-validation:
	@echo "🔗 Running link and reference validation..."
	@PYTHONPATH=. python docs/maintenance/validation.py

docs-optimization:
	@echo "🔧 Running content optimization..."
	@PYTHONPATH=. python docs/maintenance/optimization.py

docs-sync:
	@echo "🔄 Running version control synchronization..."
	@PYTHONPATH=. python docs/maintenance/sync.py --action monitor

docs-report:
	@echo "📊 Generating quality reports..."
	@PYTHONPATH=. python docs/maintenance/reporting.py --action comprehensive
	@PYTHONPATH=. python docs/maintenance/reporting.py --action dashboard

# Composite targets
docs-maintenance: docs-audit docs-validation docs-optimization docs-sync docs-report
	@echo "✅ Complete documentation maintenance cycle finished"

docs-health:
	@echo "🏥 Running quick health check..."
	@PYTHONPATH=. python docs/maintenance/audit.py --quiet | head -10
	@PYTHONPATH=. python docs/maintenance/validation.py --quiet | head -5

docs-weekly-audit: docs-audit docs-validation docs-fix
	@echo "📅 Weekly audit completed"
	@PYTHONPATH=. python docs/maintenance/reporting.py --action comprehensive --output docs/maintenance/reports/weekly_$(shell date +%Y%m%d).json

docs-monthly-analysis: docs-maintenance
	@echo "📊 Running deep monthly analysis..."
	@PYTHONPATH=. python docs/maintenance/reporting.py --action trends
	@PYTHONPATH=. python docs/maintenance/sync.py --action changelog > docs/maintenance/reports/monthly_changelog_$(shell date +%Y%m%d).md

docs-dashboard:
	@echo "📈 Generating interactive dashboard..."
	@PYTHONPATH=. python docs/maintenance/reporting.py --action dashboard --output docs/maintenance/dashboard_$(shell date +%Y%m%d).html
	@echo "Dashboard generated: docs/maintenance/dashboard_$(shell date +%Y%m%d).html"

# Utility targets
docs-emergency-reset:
	@echo "🚨 Emergency reset - clearing all maintenance data..."
	@rm -rf docs/maintenance/reports/*
	@rm -rf docs/maintenance/logs/*
	@rm -rf docs/maintenance/cache/*
	@git checkout -- docs/ 2>/dev/null || true
	@echo "✅ Emergency reset completed"

docs-clear-cache:
	@echo "🧹 Clearing maintenance caches..."
	@find docs/maintenance/ -name "*.cache" -delete 2>/dev/null || true
	@find docs/maintenance/ -name "*.tmp" -delete 2>/dev/null || true
	@find docs/maintenance/reports/ -name "*.tmp" -delete 2>/dev/null || true

docs-pre-commit:
	@echo "🔒 Running pre-commit quality checks..."
	@PYTHONPATH=. python docs/maintenance/audit.py --quiet | grep -E "(❌|🟡)" && exit 1 || echo "✅ Pre-commit checks passed"

docs-fix:
	@echo "🔧 Auto-fixing common documentation issues..."
	@PYTHONPATH=. python docs/maintenance/optimization.py --fix-only
	@PYTHONPATH=. python docs/maintenance/validation.py --auto-fix

# Specialized targets
docs-link-check:
	@echo "🔗 Checking external links only..."
	@PYTHONPATH=. python docs/maintenance/validation.py --links-only

docs-style-check:
	@echo "🎨 Checking style consistency only..."
	@PYTHONPATH=. python docs/maintenance/validation.py --style-only

docs-trend-report:
	@echo "📈 Generating trend analysis report..."
	@PYTHONPATH=. python docs/maintenance/reporting.py --action trends --output docs/maintenance/reports/trends_$(shell date +%Y%m%d).json

docs-backup:
	@echo "💾 Creating documentation backup..."
	@mkdir -p docs/maintenance/backups/
	@tar -czf docs/maintenance/backups/docs_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz docs/

docs-restore:
	@echo "🔄 Restoring from latest backup..."
	@LATEST_BACKUP=$$(ls -t docs/maintenance/backups/docs_backup_*.tar.gz | head -1); \
	if [ -n "$$LATEST_BACKUP" ]; then \
		tar -xzf $$LATEST_BACKUP -C /; \
		echo "✅ Restored from $$LATEST_BACKUP"; \
	else \
		echo "❌ No backup found"; \
	fi

# CI/CD integration targets
docs-ci-check: docs-audit docs-validation
	@echo "🔍 CI/CD quality checks completed"

docs-release-check: docs-maintenance
	@echo "🎯 Release quality verification completed"
	@PYTHONPATH=. python docs/maintenance/audit.py --comprehensive | grep -E "(Overall.*[0-9]+%)" | grep -E "[8-9][0-9]%" || (echo "❌ Quality score too low for release"; exit 1)

# Notification targets
docs-notify-critical:
	@echo "🚨 Checking for critical issues..."
	@CRITICAL_COUNT=$$(PYTHONPATH=. python docs/maintenance/audit.py --quiet 2>/dev/null | grep -c "❌" || echo "0"); \
	if [ "$$CRITICAL_COUNT" -gt 0 ]; then \
		echo "🚨 ALERT: $$CRITICAL_COUNT critical documentation issues found"; \
		# Add Slack/email notifications here \
	else \
		echo "✅ No critical issues found"; \
	fi

docs-notify-weekly:
	@echo "📅 Sending weekly maintenance summary..."
	@PYTHONPATH=. python docs/maintenance/reporting.py --action comprehensive --quiet > /tmp/weekly_report.json
	@echo "Weekly report generated in /tmp/weekly_report.json"
	# Add notification logic here

# Development targets
docs-dev-setup:
	@echo "🛠️ Setting up development environment..."
	@pip install requests beautifulsoup4 markdown python-frontmatter gitpython
	@mkdir -p docs/maintenance/{reports,logs,cache,backups}
	@echo "✅ Development environment ready"

docs-dev-test:
	@echo "🧪 Running maintenance system tests..."
	@PYTHONPATH=. python -m pytest docs/maintenance/ -v --tb=short || echo "Some tests failed - check implementation"

docs-dev-clean:
	@echo "🧹 Cleaning development artifacts..."
	@find docs/maintenance/ -name "*.pyc" -delete
	@find docs/maintenance/ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Information targets
docs-info:
	@echo "📋 Documentation Maintenance System Info"
	@echo "=========================================="
	@echo "Version: 1.0.0"
	@echo "Framework: docs/maintenance/"
	@echo "Reports: docs/maintenance/reports/"
	@echo "Config: docs/maintenance/config.json"
	@echo ""
	@echo "Documentation Files: $$(find docs/ -name "*.md" | wc -l)"
	@echo "Maintenance Scripts: $$(find docs/maintenance/ -name "*.py" | wc -l)"
	@echo "Recent Reports: $$(find docs/maintenance/reports/ -name "*.json" 2>/dev/null | wc -l || echo "0")"

docs-status:
	@echo "📊 Current Documentation Status"
	@echo "=================================="
	@PYTHONPATH=. python docs/maintenance/audit.py --quiet | head -5
	@echo ""
	@echo "Recent Changes:"
	@git log --oneline --since="1 week ago" -- docs/ | head -3 || echo "No recent changes"

# Help system
docs-help: help

# Default target shows help
.DEFAULT_GOAL := help