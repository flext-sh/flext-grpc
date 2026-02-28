#!/usr/bin/env python3
"""FLEXT-gRPC Architecture Documentation Validation.

Validates architecture documentation for completeness, consistency, and accuracy.
"""

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

from flext_grpc import t


class ArchitectureValidator:
    """Validates architecture documentation completeness and consistency."""

    # Quality score thresholds
    EXCELLENT_QUALITY_SCORE = 95
    GOOD_QUALITY_SCORE = 80
    ACCEPTABLE_QUALITY_SCORE = 60
    CRITICAL_QUALITY_SCORE = 40

    # Validation constants
    MIN_ADR_FILES = 3

    def __init__(self, root_path: str = ".") -> None:
        """Initialize the architecture documentation validator.

        Args:
            root_path: Root path for documentation validation.

        """
        self.root_path = Path(root_path)
        self.issues: list[dict[str, t.GeneralValueType]] = []
        self.warnings: list[dict[str, t.GeneralValueType]] = []
        self.recommendations: list[dict[str, t.GeneralValueType]] = []

    def validate_all(self) -> dict[str, t.GeneralValueType]:
        """Run all validation checks."""
        # Reset collections
        self.issues = []
        self.warnings = []
        self.recommendations = []

        # Run validation checks
        self._validate_c4_model_completeness()
        self._validate_adr_completeness()
        self._validate_diagram_consistency()
        self._validate_cross_references()
        self._validate_content_freshness()
        self._validate_technical_accuracy()

        # Generate summary
        summary = self._generate_summary()

        # Print results
        self._print_results(summary)

        return {
            "summary": summary,
            "issues": self.issues,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
        }

    def _validate_c4_model_completeness(self) -> None:
        """Validate C4 model documentation completeness."""
        c4_dir = self.root_path / "docs" / "architecture" / "c4-model"

        required_files = ["context.md", "containers.md", "components.md", "code.md"]

        missing_files = [
            file for file in required_files if not (c4_dir / file).exists()
        ]

        if missing_files:
            self.issues.append({
                "type": "c4_model_incomplete",
                "severity": "high",
                "message": f"C4 model missing required views: {', '.join(missing_files)}",
                "files": missing_files,
            })

        # Check content completeness
        context_file = c4_dir / "context.md"
        if context_file.exists():
            content = context_file.read_text()

            required_sections = [
                "System Context Diagram",
                "System Scope and Boundaries",
                "External Interfaces",
                "Stakeholders and User Personas",
            ]

            for section in required_sections:
                if section not in content:
                    self.warnings.append({
                        "type": "c4_context_incomplete",
                        "severity": "medium",
                        "message": f"C4 context view missing section: {section}",
                        "file": str(context_file),
                    })

    def _validate_adr_completeness(self) -> None:
        """Validate ADR documentation completeness."""
        adr_dir = self.root_path / "docs" / "architecture" / "adrs"

        if not adr_dir.exists():
            self.issues.append({
                "type": "adr_system_missing",
                "severity": "high",
                "message": "Architecture Decision Records system not found",
            })
            return

        readme_file = adr_dir / "README.md"
        if not readme_file.exists():
            self.issues.append({
                "type": "adr_readme_missing",
                "severity": "high",
                "message": "ADR README documentation missing",
            })

        # Check for ADR files
        adr_files = list(adr_dir.glob("adr-*.md"))

        # Check for ADR files
        adr_files = list(adr_dir.glob("adr-*.md"))
        if len(adr_files) < self.MIN_ADR_FILES:
            self.warnings.append({
                "type": "few_adrs",
                "severity": "medium",
                "message": f"Only {len(adr_files)} ADRs found, recommend at least 3 for major architectural decisions",
            })

        # Validate ADR format
        for adr_file in adr_files:
            content = adr_file.read_text()

            required_fields = [
                "## Status",
                "## Context",
                "## Decision",
                "## Consequences",
            ]

            missing_fields = [
                field for field in required_fields if field not in content
            ]

            if missing_fields:
                self.warnings.append({
                    "type": "adr_format_incomplete",
                    "severity": "medium",
                    "message": f"ADR {adr_file.name} missing required fields: {', '.join(missing_fields)}",
                    "file": str(adr_file),
                })

    def _validate_diagram_consistency(self) -> None:
        """Validate diagram consistency and completeness."""
        diagrams_dir = self.root_path / "docs" / "architecture" / "diagrams"

        required_diagrams = [
            "context.puml",
            "containers.puml",
            "components.puml",
            "deployment.puml",
        ]

        missing_diagrams = [
            diagram
            for diagram in required_diagrams
            if not (diagrams_dir / diagram).exists()
        ]

        if missing_diagrams:
            self.issues.append({
                "type": "diagrams_missing",
                "severity": "high",
                "message": f"Required architecture diagrams missing: {', '.join(missing_diagrams)}",
            })

        # Check if generation script exists
        gen_script = (
            self.root_path / "docs" / "architecture" / "tools" / "generate-diagrams.sh"
        )
        if not gen_script.exists():
            self.warnings.append({
                "type": "generation_script_missing",
                "severity": "medium",
                "message": "Diagram generation automation script missing",
            })

    def _validate_cross_references(self) -> None:
        """Validate cross-references between documentation."""
        # Check if documentation properly references other sections
        architecture_md = self.root_path / "docs" / "architecture.md"
        if architecture_md.exists():
            content = architecture_md.read_text()

            # Should reference the new architecture documentation
            if "c4-model" not in content or "adrs" not in content:
                self.warnings.append({
                    "type": "cross_references_missing",
                    "severity": "low",
                    "message": "Architecture documentation should reference C4 model and ADRs",
                })

    def _validate_content_freshness(self) -> None:
        """Validate documentation freshness."""
        # Check how old the documentation is
        architecture_files = [
            "docs/architecture.md",
            "docs/architecture/c4-model/context.md",
            "docs/architecture/adrs/README.md",
        ]

        max_age_days = 90  # Documentation should be reviewed every 3 months

        for file_path in architecture_files:
            full_path = self.root_path / file_path
            if full_path.exists():
                mtime = datetime.fromtimestamp(full_path.stat().st_mtime, tz=UTC)
                age_days = (datetime.now(UTC) - mtime).days

                if age_days > max_age_days:
                    self.warnings.append({
                        "type": "documentation_stale",
                        "severity": "low",
                        "message": f"Documentation file {file_path} is {age_days} days old (review recommended)",
                        "file": file_path,
                        "age_days": age_days,
                    })

    def _validate_technical_accuracy(self) -> None:
        """Validate technical accuracy of documentation."""
        # Check version consistency
        version_pattern = r"Version.*(\d+\.\d+\.\d+)"

        files_to_check = [
            "docs/architecture.md",
            "docs/architecture/c4-model/context.md",
            "README.md",
        ]

        versions: dict[str, str] = {}
        for file_path in files_to_check:
            full_path = self.root_path / file_path
            if full_path.exists():
                content = full_path.read_text()
                match = re.search(version_pattern, content, re.IGNORECASE)
                if match:
                    versions[file_path] = match.group(1)

        # Check if versions are consistent
        if len(set(versions.values())) > 1:
            self.warnings.append({
                "type": "version_inconsistency",
                "severity": "medium",
                "message": f"Version numbers inconsistent across files: {versions}",
            })

        # Check for known technical inaccuracies
        architecture_md = self.root_path / "docs" / "architecture.md"
        if architecture_md.exists():
            content = architecture_md.read_text()

            # Check if current technical details are accurate
            if "Test Coverage: 35%" in content:
                self.warnings.append({
                    "type": "outdated_metrics",
                    "severity": "medium",
                    "message": "Architecture documentation contains outdated test coverage metrics",
                })

    def _generate_summary(self) -> dict[str, t.GeneralValueType]:
        """Generate validation summary."""
        total_issues = len(self.issues)
        total_warnings = len(self.warnings)
        total_recommendations = len(self.recommendations)

        # Calculate quality score
        base_score = 100
        issue_penalty = total_issues * 15
        warning_penalty = total_warnings * 5

        quality_score = max(0, base_score - issue_penalty - warning_penalty)

        # Determine overall status
        if quality_score >= ArchitectureValidator.EXCELLENT_QUALITY_SCORE:
            status = "excellent"
        elif quality_score >= ArchitectureValidator.GOOD_QUALITY_SCORE:
            status = "good"
        elif quality_score >= ArchitectureValidator.ACCEPTABLE_QUALITY_SCORE:
            status = "needs_work"
        else:
            status = "critical"

        return {
            "quality_score": quality_score,
            "status": status,
            "total_issues": total_issues,
            "total_warnings": total_warnings,
            "total_recommendations": total_recommendations,
            "timestamp": datetime.now(UTC).isoformat(),
        }

    def _print_results(self, summary: dict[str, t.GeneralValueType]) -> None:
        """Print validation results."""
        # Reserved for future summary display functionality
        _ = summary  # Reserved for future use

        if self.issues:
            for _issue in self.issues[:3]:  # Show first 3
                pass

        if self.warnings:
            for _warning in self.warnings[:3]:  # Show first 3
                pass

        if self.recommendations:
            for _rec in self.recommendations[:3]:  # Show first 3
                pass


def save_report(
    results: dict[str, t.GeneralValueType],
    output_path: Path | None = None,
) -> None:
    """Save validation report to file."""
    if output_path is None:
        timestamp: str = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        reports_dir: Path = Path("docs/architecture/tools/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        output_path = reports_dir / f"validation_{timestamp}.json"

    with Path(output_path).open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)


def main() -> None:
    """Main entry point for documentation validation."""
    parser = argparse.ArgumentParser(
        description="FLEXT-gRPC Architecture Documentation Validation",
    )
    parser.add_argument("--path", default=".", help="Root path to validate")
    parser.add_argument("--output", help="Output path for report")
    parser.add_argument("--quiet", action="store_true", help="Suppress detailed output")

    args = parser.parse_args()

    # Create validator
    validator = ArchitectureValidator(args.path)

    # Run validation
    results = validator.validate_all()

    # Save report
    output_path = Path(args.output) if args.output else None

    save_report(results, output_path)

    # Exit with appropriate code
    summary = results["summary"]
    if isinstance(summary, dict) and (
        summary.get("status") == "critical"
        or int(str(summary.get("quality_score", 0)))
        < ArchitectureValidator.CRITICAL_QUALITY_SCORE
    ):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
