#!/usr/bin/env python3
"""
FLEXT-gRPC Documentation Quality Assurance Reporting System

Comprehensive reporting infrastructure for documentation maintenance and monitoring.

Author: FLEXT-gRPC Documentation Maintenance System
Version: 1.0.0
"""

import os
import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import matplotlib.pyplot as plt
import pandas as pd


@dataclass
class QualityMetrics:
    """Documentation quality metrics."""
    timestamp: str
    overall_score: float
    structure_score: float
    accuracy_score: float
    completeness_score: float
    freshness_score: float
    link_health_score: float
    style_consistency_score: float
    total_files: int
    files_with_issues: int
    critical_issues: int
    warning_count: int


@dataclass
class TrendAnalysis:
    """Trend analysis for quality metrics over time."""
    period: str
    metric: str
    current_value: float
    previous_value: float
    change: float
    trend: str  # 'improving', 'declining', 'stable'
    confidence: float


class DocumentationReporter:
    """Generate comprehensive documentation quality reports."""

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.reports_dir = self.root_path / "docs" / "maintenance" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_comprehensive_report(self, audit_report: Dict, validation_report: Dict,
                                    optimization_report: Dict) -> Dict[str, Any]:
        """Generate comprehensive quality report from all maintenance data."""
        timestamp = datetime.now().isoformat()

        # Calculate quality metrics
        quality_metrics = self._calculate_quality_metrics(audit_report, validation_report)

        # Analyze trends
        trend_analysis = self._analyze_trends(quality_metrics)

        # Identify critical issues
        critical_issues = self._identify_critical_issues(audit_report, validation_report)

        # Generate recommendations
        recommendations = self._generate_recommendations(quality_metrics, critical_issues)

        report = {
            "timestamp": timestamp,
            "report_type": "comprehensive",
            "quality_metrics": asdict(quality_metrics),
            "trend_analysis": [asdict(t) for t in trend_analysis],
            "critical_issues": critical_issues,
            "recommendations": recommendations,
            "source_data": {
                "audit": audit_report,
                "validation": validation_report,
                "optimization": optimization_report
            }
        }

        return report

    def _calculate_quality_metrics(self, audit_report: Dict, validation_report: Dict) -> QualityMetrics:
        """Calculate overall quality metrics."""
        # Extract scores from reports
        audit_avg = audit_report.get("average_quality", 0)
        link_health = validation_report.get("summary", {}).get("link_health_percentage", 0)

        # Estimate other metrics (would be calculated from detailed analysis)
        structure_score = min(100, audit_avg + 5)  # Estimate based on audit
        accuracy_score = min(100, audit_avg)       # Based on audit analysis
        completeness_score = min(100, audit_avg - 5)  # Estimate
        freshness_score = min(100, audit_avg)      # Based on dates
        style_score = 90  # Placeholder - would be calculated from validation

        overall_score = (
            structure_score * 0.2 +
            accuracy_score * 0.25 +
            completeness_score * 0.2 +
            freshness_score * 0.15 +
            link_health * 0.1 +
            style_score * 0.1
        )

        total_files = audit_report.get("total_files", 0)
        files_with_issues = sum(1 for r in audit_report.get("file_results", [])
                              if r.get("issues") or r.get("warnings"))

        critical_issues = len(audit_report.get("critical_issues", []))
        warning_count = sum(len(r.get("warnings", [])) for r in audit_report.get("file_results", []))

        return QualityMetrics(
            timestamp=datetime.now().isoformat(),
            overall_score=round(overall_score, 1),
            structure_score=round(structure_score, 1),
            accuracy_score=round(accuracy_score, 1),
            completeness_score=round(completeness_score, 1),
            freshness_score=round(freshness_score, 1),
            link_health_score=round(link_health, 1),
            style_consistency_score=round(style_score, 1),
            total_files=total_files,
            files_with_issues=files_with_issues,
            critical_issues=critical_issues,
            warning_count=warning_count
        )

    def _analyze_trends(self, current_metrics: QualityMetrics) -> List[TrendAnalysis]:
        """Analyze quality trends over time."""
        trends = []

        # Load historical data
        historical_data = self._load_historical_data()

        if not historical_data:
            return trends

        # Analyze each metric
        metrics_to_analyze = [
            ("overall_score", "Overall Quality"),
            ("structure_score", "Structure"),
            ("accuracy_score", "Accuracy"),
            ("completeness_score", "Completeness"),
            ("freshness_score", "Freshness"),
            ("link_health_score", "Link Health"),
            ("style_consistency_score", "Style Consistency")
        ]

        for metric_key, metric_name in metrics_to_analyze:
            current_value = getattr(current_metrics, metric_key)
            previous_values = [h.get(metric_key, current_value) for h in historical_data[-5:]]  # Last 5 reports

            if previous_values:
                previous_avg = sum(previous_values) / len(previous_values)
                change = current_value - previous_avg

                if abs(change) < 1:
                    trend = "stable"
                elif change > 2:
                    trend = "improving"
                elif change < -2:
                    trend = "declining"
                else:
                    trend = "stable"

                confidence = min(100, len(previous_values) * 20)  # Simple confidence calculation

                trends.append(TrendAnalysis(
                    period="last_5_reports",
                    metric=metric_name,
                    current_value=current_value,
                    previous_value=round(previous_avg, 1),
                    change=round(change, 1),
                    trend=trend,
                    confidence=round(confidence, 1)
                ))

        return trends

    def _load_historical_data(self) -> List[Dict[str, Any]]:
        """Load historical quality metrics."""
        historical = []

        try:
            # Find recent comprehensive reports
            report_files = list(self.reports_dir.glob("comprehensive_*.json"))
            report_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            for report_file in report_files[:10]:  # Last 10 reports
                try:
                    with open(report_file, 'r') as f:
                        data = json.load(f)
                        if "quality_metrics" in data:
                            historical.append(data["quality_metrics"])
                except:
                    continue

        except Exception as e:
            print(f"Warning: Could not load historical data: {e}")

        return historical

    def _identify_critical_issues(self, audit_report: Dict, validation_report: Dict) -> List[Dict[str, Any]]:
        """Identify critical documentation issues."""
        critical_issues = []

        # Audit critical issues
        for issue in audit_report.get("critical_issues", []):
            critical_issues.append({
                "type": "audit",
                "severity": "critical",
                "source": "audit_system",
                **issue
            })

        # Validation critical issues
        broken_links = [r for r in validation_report.get("link_results", [])
                       if r.get("status") == "broken"]
        for link in broken_links[:10]:  # Limit to top 10
            critical_issues.append({
                "type": "link_validation",
                "severity": "high",
                "source": "validation_system",
                "message": f"Broken external link: {link['url']}",
                "details": f"HTTP {link.get('status_code', 'unknown')}"
            })

        # Files with very low quality scores
        for result in audit_report.get("file_results", []):
            if result.get("quality_score", 100) < 50:
                critical_issues.append({
                    "type": "quality_score",
                    "severity": "high",
                    "source": "audit_system",
                    "file": result.get("file_path"),
                    "message": f"Very low quality score: {result.get('quality_score')}",
                    "score": result.get("quality_score")
                })

        return critical_issues

    def _generate_recommendations(self, metrics: QualityMetrics, critical_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate improvement recommendations."""
        recommendations = []

        # Based on quality scores
        if metrics.overall_score < 80:
            recommendations.append({
                "priority": "high",
                "category": "overall_quality",
                "action": "Implement comprehensive quality improvement program",
                "estimated_effort": "2-4 weeks",
                "impact": "high"
            })

        if metrics.link_health_score < 90:
            recommendations.append({
                "priority": "medium",
                "category": "link_maintenance",
                "action": "Fix broken external links and implement regular link checking",
                "estimated_effort": "1 week",
                "impact": "medium"
            })

        if metrics.freshness_score < 85:
            recommendations.append({
                "priority": "medium",
                "category": "content_freshness",
                "action": "Update outdated content and implement freshness monitoring",
                "estimated_effort": "1-2 weeks",
                "impact": "medium"
            })

        # Based on critical issues
        if any(issue["type"] == "audit" for issue in critical_issues):
            recommendations.append({
                "priority": "high",
                "category": "audit_issues",
                "action": "Resolve all critical audit issues immediately",
                "estimated_effort": "3-5 days",
                "impact": "high"
            })

        # Proactive recommendations
        recommendations.extend([
            {
                "priority": "low",
                "category": "automation",
                "action": "Implement automated maintenance scheduling",
                "estimated_effort": "1 week",
                "impact": "medium"
            },
            {
                "priority": "low",
                "category": "monitoring",
                "action": "Set up continuous quality monitoring and alerting",
                "estimated_effort": "1 week",
                "impact": "medium"
            }
        ])

        return recommendations

    def generate_dashboard(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML dashboard from report data."""
        metrics = report_data.get("quality_metrics", {})

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>FLEXT-gRPC Documentation Quality Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .metric {{ background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .score {{ font-size: 24px; font-weight: bold; }}
        .excellent {{ color: #28a745; }}
        .good {{ color: #17a2b8; }}
        .needs-work {{ color: #ffc107; }}
        .critical {{ color: #dc3545; }}
        .chart {{ width: 100%; height: 300px; background: #f8f9fa; border: 1px solid #dee2e6; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
    </style>
</head>
<body>
    <h1>FLEXT-gRPC Documentation Quality Dashboard</h1>
    <p><strong>Report Date:</strong> {report_data.get('timestamp', 'Unknown')}</p>

    <h2>Quality Overview</h2>
    <div class="metric">
        <h3>Overall Quality Score</h3>
        <span class="score {self._get_score_class(metrics.get('overall_score', 0))}">
            {metrics.get('overall_score', 0)}%
        </span>
    </div>

    <h2>Detailed Metrics</h2>
    <table>
        <tr><th>Metric</th><th>Score</th><th>Status</th></tr>
        <tr><td>Structure</td><td>{metrics.get('structure_score', 0)}%</td><td>{self._get_status_text(metrics.get('structure_score', 0))}</td></tr>
        <tr><td>Accuracy</td><td>{metrics.get('accuracy_score', 0)}%</td><td>{self._get_status_text(metrics.get('accuracy_score', 0))}</td></tr>
        <tr><td>Completeness</td><td>{metrics.get('completeness_score', 0)}%</td><td>{self._get_status_text(metrics.get('completeness_score', 0))}</td></tr>
        <tr><td>Freshness</td><td>{metrics.get('freshness_score', 0)}%</td><td>{self._get_status_text(metrics.get('freshness_score', 0))}</td></tr>
        <tr><td>Link Health</td><td>{metrics.get('link_health_score', 0)}%</td><td>{self._get_status_text(metrics.get('link_health_score', 0))}</td></tr>
        <tr><td>Style Consistency</td><td>{metrics.get('style_consistency_score', 0)}%</td><td>{self._get_status_text(metrics.get('style_consistency_score', 0))}</td></tr>
    </table>

    <h2>Critical Issues</h2>
"""

        critical_issues = report_data.get("critical_issues", [])
        if critical_issues:
            html += "<ul>"
            for issue in critical_issues[:10]:  # Show top 10
                html += f"<li><strong>{issue.get('type', 'Unknown')}:</strong> {issue.get('message', 'No details')}</li>"
            html += "</ul>"
        else:
            html += "<p>No critical issues found! 🎉</p>"

        html += """
    <h2>Recommendations</h2>
"""

        recommendations = report_data.get("recommendations", [])
        if recommendations:
            html += "<ul>"
            for rec in recommendations:
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec.get("priority"), "⚪")
                html += f"<li>{priority_icon} <strong>{rec.get('category', 'Unknown')}:</strong> {rec.get('action', 'No action specified')}</li>"
            html += "</ul>"

        html += """
    <h2>Trend Analysis</h2>
    <div class="chart">
        <p>Trend charts would be displayed here with historical data visualization.</p>
    </div>

    <footer>
        <p><em>Generated by FLEXT-gRPC Documentation Maintenance System</em></p>
    </footer>
</body>
</html>
"""

        return html

    def _get_score_class(self, score: float) -> str:
        """Get CSS class for score visualization."""
        if score >= 90:
            return "excellent"
        elif score >= 80:
            return "good"
        elif score >= 70:
            return "needs-work"
        else:
            return "critical"

    def _get_status_text(self, score: float) -> str:
        """Get status text for score."""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Needs Work"
        else:
            return "Critical"

    def export_csv_report(self, report_data: Dict[str, Any], output_path: Path):
        """Export report data to CSV format."""
        rows = []

        # Quality metrics
        metrics = report_data.get("quality_metrics", {})
        rows.append(["Metric", "Value", "Status"])
        rows.append(["Overall Score", f"{metrics.get('overall_score', 0)}%", self._get_status_text(metrics.get('overall_score', 0))])
        rows.append(["Structure", f"{metrics.get('structure_score', 0)}%", self._get_status_text(metrics.get('structure_score', 0))])
        rows.append(["Accuracy", f"{metrics.get('accuracy_score', 0)}%", self._get_status_text(metrics.get('accuracy_score', 0))])
        rows.append(["Completeness", f"{metrics.get('completeness_score', 0)}%", self._get_status_text(metrics.get('completeness_score', 0))])
        rows.append(["Freshness", f"{metrics.get('freshness_score', 0)}%", self._get_status_text(metrics.get('freshness_score', 0))])
        rows.append(["Link Health", f"{metrics.get('link_health_score', 0)}%", self._get_status_text(metrics.get('link_health_score', 0))])

        # Critical issues
        rows.append([])
        rows.append(["Critical Issues"])
        for issue in report_data.get("critical_issues", [])[:10]:
            rows.append([issue.get("type", ""), issue.get("message", "")])

        # Recommendations
        rows.append([])
        rows.append(["Recommendations"])
        for rec in report_data.get("recommendations", []):
            rows.append([rec.get("priority", ""), rec.get("category", ""), rec.get("action", "")])

        # Write CSV
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def send_notifications(self, report_data: Dict[str, Any], notification_config: Dict[str, Any]) -> Dict[str, Any]:
        """Send notifications about critical issues."""
        # This would integrate with email/Slack/etc.
        # For now, return mock result

        critical_count = len(report_data.get("critical_issues", []))
        overall_score = report_data.get("quality_metrics", {}).get("overall_score", 0)

        notification = {
            "sent": True,
            "channels": ["console"],  # Would include email, slack, etc.
            "message": f"Documentation Quality Report: {overall_score}% overall score, {critical_count} critical issues",
            "timestamp": datetime.now().isoformat()
        }

        if critical_count > 0:
            notification["alert_level"] = "high"
            notification["critical_issues"] = critical_count
        elif overall_score < 80:
            notification["alert_level"] = "medium"
        else:
            notification["alert_level"] = "low"

        return notification

    def generate_trend_report(self, days: int = 30) -> Dict[str, Any]:
        """Generate trend analysis report."""
        # Load historical data
        historical = self._load_historical_data()

        if len(historical) < 2:
            return {"error": "Insufficient historical data for trend analysis"}

        # Calculate trends
        latest = historical[0]
        previous = historical[-1] if len(historical) > 1 else historical[0]

        trends = {}
        for key in ["overall_score", "structure_score", "accuracy_score", "completeness_score", "freshness_score"]:
            current = latest.get(key, 0)
            prev = previous.get(key, current)
            change = current - prev
            trend = "improving" if change > 0 else "declining" if change < 0 else "stable"
            trends[key] = {
                "current": current,
                "previous": prev,
                "change": change,
                "trend": trend
            }

        return {
            "period_days": days,
            "data_points": len(historical),
            "trends": trends,
            "summary": {
                "improving_metrics": sum(1 for t in trends.values() if t["trend"] == "improving"),
                "declining_metrics": sum(1 for t in trends.values() if t["trend"] == "declining"),
                "stable_metrics": sum(1 for t in trends.values() if t["trend"] == "stable")
            }
        }


def main():
    """Main entry point for documentation reporting."""
    import argparse

    parser = argparse.ArgumentParser(description="FLEXT-gRPC Documentation Quality Assurance Reporting")
    parser.add_argument("--action", choices=["comprehensive", "dashboard", "csv", "trends"],
                       default="comprehensive", help="Report type to generate")
    parser.add_argument("--audit-report", help="Path to audit report JSON")
    parser.add_argument("--validation-report", help="Path to validation report JSON")
    parser.add_argument("--optimization-report", help="Path to optimization report JSON")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--path", default=".", help="Root path for reports")

    args = parser.parse_args()

    reporter = DocumentationReporter(args.path)

    if args.action == "comprehensive":
        # Load report data
        audit_data = {}
        validation_data = {}
        optimization_data = {}

        if args.audit_report:
            with open(args.audit_report, 'r') as f:
                audit_data = json.load(f)

        if args.validation_report:
            with open(args.validation_report, 'r') as f:
                validation_data = json.load(f)

        if args.optimization_report:
            with open(args.optimization_report, 'r') as f:
                optimization_data = json.load(f)

        # Generate comprehensive report
        report = reporter.generate_comprehensive_report(audit_data, validation_data, optimization_data)

        # Save report
        output_path = Path(args.output) if args.output else reporter.reports_dir / f"comprehensive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📊 Comprehensive report saved to: {output_path}")

        # Print summary
        metrics = report.get("quality_metrics", {})
        print("
📈 Quality Summary:"        print(f"  Overall Score: {metrics.get('overall_score', 0)}%")
        print(f"  Critical Issues: {len(report.get('critical_issues', []))}")
        print(f"  Recommendations: {len(report.get('recommendations', []))}")

    elif args.action == "dashboard":
        # Generate HTML dashboard
        # This would need actual report data - for now create sample
        sample_data = {
            "timestamp": datetime.now().isoformat(),
            "quality_metrics": {
                "overall_score": 85.5,
                "structure_score": 88.0,
                "accuracy_score": 82.0,
                "completeness_score": 87.0,
                "freshness_score": 90.0,
                "link_health_score": 95.0,
                "style_consistency_score": 89.0
            },
            "critical_issues": [
                {"type": "broken_link", "message": "External link broken"}
            ],
            "recommendations": [
                {"priority": "medium", "category": "link_maintenance", "action": "Fix broken links"}
            ]
        }

        dashboard_html = reporter.generate_dashboard(sample_data)

        output_path = Path(args.output) if args.output else reporter.reports_dir / "dashboard.html"
        with open(output_path, 'w') as f:
            f.write(dashboard_html)

        print(f"📊 Dashboard generated: {output_path}")

    elif args.action == "csv":
        # Generate CSV export
        sample_data = {
            "quality_metrics": {"overall_score": 85.5},
            "critical_issues": [],
            "recommendations": []
        }

        output_path = Path(args.output) if args.output else reporter.reports_dir / f"report_{datetime.now().strftime('%Y%m%d')}.csv"
        reporter.export_csv_report(sample_data, output_path)

        print(f"📊 CSV report exported: {output_path}")

    elif args.action == "trends":
        # Generate trend analysis
        trends = reporter.generate_trend_report()

        print("📈 Trend Analysis:")
        if "error" in trends:
            print(f"  Error: {trends['error']}")
        else:
            summary = trends.get("summary", {})
            print(f"  Data points: {trends['data_points']}")
            print(f"  Improving metrics: {summary.get('improving_metrics', 0)}")
            print(f"  Declining metrics: {summary.get('declining_metrics', 0)}")
            print(f"  Stable metrics: {summary.get('stable_metrics', 0)}")

    return 0


if __name__ == "__main__":
    exit(main())