"""
Report generation for OSINT analysis results.
Generates JSON and HTML reports with findings.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from jinja2 import Template


class ReportGenerator:
    """Generate analysis reports in various formats."""

    def __init__(self, output_dir: str = './output/reports'):
        """
        Initialize report generator.

        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_json_report(
        self,
        keyword: str,
        posts: List[Dict],
        distribution: Dict,
        platform_sentiment: Dict[str, Dict],
        average_sentiment: Dict,
        top_positive: List[Dict],
        top_negative: List[Dict]
    ) -> str:
        """
        Generate a JSON report with all analysis data.

        Args:
            keyword: Search keyword
            posts: All analyzed posts
            distribution: Overall sentiment distribution
            platform_sentiment: Sentiment by platform
            average_sentiment: Average sentiment scores
            top_positive: Top positive posts
            top_negative: Top negative posts

        Returns:
            Path to the generated JSON file
        """
        report = {
            'metadata': {
                'keyword': keyword,
                'generated_at': datetime.now().isoformat(),
                'total_posts': len(posts),
                'platforms': list(platform_sentiment.keys())
            },
            'sentiment_distribution': distribution,
            'platform_sentiment': platform_sentiment,
            'average_sentiment': average_sentiment,
            'top_posts': {
                'positive': top_positive,
                'negative': top_negative
            },
            'all_posts': posts
        }

        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"osint_report_{keyword.replace(' ', '_')}_{timestamp}.json"
        filepath = self.output_dir / filename

        # Write JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def generate_html_report(
        self,
        keyword: str,
        posts: List[Dict],
        distribution: Dict,
        platform_sentiment: Dict[str, Dict],
        average_sentiment: Dict,
        top_positive: List[Dict],
        top_negative: List[Dict]
    ) -> str:
        """
        Generate an HTML report with visualizations.

        Args:
            keyword: Search keyword
            posts: All analyzed posts
            distribution: Overall sentiment distribution
            platform_sentiment: Sentiment by platform
            average_sentiment: Average sentiment scores
            top_positive: Top positive posts
            top_negative: Top negative posts

        Returns:
            Path to the generated HTML file
        """
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Analysis Report - {{ keyword }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .metadata {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section {
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }
        .metric {
            display: inline-block;
            margin: 10px 20px 10px 0;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }
        .metric-label {
            color: #666;
            font-size: 0.9em;
        }
        .positive { color: #4CAF50; }
        .negative { color: #F44336; }
        .neutral { color: #9E9E9E; }
        .post-card {
            background: #f9f9f9;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }
        .post-platform {
            font-weight: bold;
            color: #667eea;
            text-transform: uppercase;
            font-size: 0.85em;
        }
        .post-text {
            margin: 10px 0;
            color: #333;
        }
        .post-meta {
            font-size: 0.9em;
            color: #666;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #667eea;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }
        a {
            color: #667eea;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 OSINT Analysis Report</h1>
        <p style="font-size: 1.2em; margin: 10px 0 0 0;">Keyword: "{{ keyword }}"</p>
    </div>

    <div class="metadata">
        <strong>Generated:</strong> {{ generated_at }}<br>
        <strong>Total Posts Analyzed:</strong> {{ total_posts }}<br>
        <strong>Platforms:</strong> {{ platforms }}
    </div>

    <div class="section">
        <h2>📊 Sentiment Overview</h2>
        <div class="metric">
            <span class="metric-value positive">{{ distribution.positive }}</span>
            <span class="metric-label">Positive ({{ distribution.positive_pct }}%)</span>
        </div>
        <div class="metric">
            <span class="metric-value negative">{{ distribution.negative }}</span>
            <span class="metric-label">Negative ({{ distribution.negative_pct }}%)</span>
        </div>
        <div class="metric">
            <span class="metric-value neutral">{{ distribution.neutral }}</span>
            <span class="metric-label">Neutral ({{ distribution.neutral_pct }}%)</span>
        </div>
    </div>

    <div class="section">
        <h2>📈 Average Sentiment Scores</h2>
        <p><strong>Overall Sentiment:</strong> <span class="{{ average_sentiment.overall_sentiment }}">{{ average_sentiment.overall_sentiment|upper }}</span></p>
        <p><strong>Average Polarity:</strong> {{ average_sentiment.avg_polarity }} <em>(range: -1 to 1)</em></p>
        <p><strong>Average Subjectivity:</strong> {{ average_sentiment.avg_subjectivity }} <em>(range: 0 to 1)</em></p>
    </div>

    <div class="section">
        <h2>🌐 Platform Breakdown</h2>
        <table>
            <thead>
                <tr>
                    <th>Platform</th>
                    <th>Total Posts</th>
                    <th>Positive</th>
                    <th>Negative</th>
                    <th>Neutral</th>
                </tr>
            </thead>
            <tbody>
                {% for platform, data in platform_sentiment.items() %}
                <tr>
                    <td><strong>{{ platform|capitalize }}</strong></td>
                    <td>{{ data.total }}</td>
                    <td class="positive">{{ data.positive }} ({{ data.positive_pct }}%)</td>
                    <td class="negative">{{ data.negative }} ({{ data.negative_pct }}%)</td>
                    <td class="neutral">{{ data.neutral }} ({{ data.neutral_pct }}%)</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>✨ Top Positive Posts</h2>
        {% for post in top_positive %}
        <div class="post-card">
            <div class="post-platform">{{ post.platform }}</div>
            <div class="post-text">{{ post.title or post.text[:200] }}...</div>
            <div class="post-meta">
                Polarity: <strong class="positive">{{ post.sentiment_analysis.polarity }}</strong> |
                <a href="{{ post.url }}" target="_blank">View Post</a>
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="section">
        <h2>⚠️ Top Negative Posts</h2>
        {% for post in top_negative %}
        <div class="post-card">
            <div class="post-platform">{{ post.platform }}</div>
            <div class="post-text">{{ post.title or post.text[:200] }}...</div>
            <div class="post-meta">
                Polarity: <strong class="negative">{{ post.sentiment_analysis.polarity }}</strong> |
                <a href="{{ post.url }}" target="_blank">View Post</a>
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="footer">
        <p>Generated by Social Media OSINT Analyzer</p>
        <p>This report contains publicly available information collected for analysis purposes.</p>
    </div>
</body>
</html>
"""

        template = Template(html_template)

        # Prepare data for template
        context = {
            'keyword': keyword,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_posts': len(posts),
            'platforms': ', '.join(platform_sentiment.keys()),
            'distribution': distribution,
            'average_sentiment': average_sentiment,
            'platform_sentiment': platform_sentiment,
            'top_positive': top_positive[:5],
            'top_negative': top_negative[:5]
        }

        # Render HTML
        html_content = template.render(**context)

        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"osint_report_{keyword.replace(' ', '_')}_{timestamp}.html"
        filepath = self.output_dir / filename

        # Write HTML file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(filepath)

    def generate_text_summary(
        self,
        keyword: str,
        distribution: Dict,
        average_sentiment: Dict,
        platform_sentiment: Dict[str, Dict]
    ) -> str:
        """
        Generate a text summary of the analysis.

        Args:
            keyword: Search keyword
            distribution: Sentiment distribution
            average_sentiment: Average sentiment scores
            platform_sentiment: Sentiment by platform

        Returns:
            Formatted text summary
        """
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║         SOCIAL MEDIA OSINT ANALYSIS SUMMARY                  ║
╚══════════════════════════════════════════════════════════════╝

Keyword: "{keyword}"
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

───────────────────────────────────────────────────────────────
OVERALL SENTIMENT DISTRIBUTION
───────────────────────────────────────────────────────────────
Total Posts: {distribution['total']}
✅ Positive: {distribution['positive']} ({distribution['positive_pct']}%)
❌ Negative: {distribution['negative']} ({distribution['negative_pct']}%)
⚪ Neutral:  {distribution['neutral']} ({distribution['neutral_pct']}%)

───────────────────────────────────────────────────────────────
AVERAGE SENTIMENT SCORES
───────────────────────────────────────────────────────────────
Overall Sentiment: {average_sentiment['overall_sentiment'].upper()}
Average Polarity: {average_sentiment['avg_polarity']} (range: -1 to 1)
Average Subjectivity: {average_sentiment['avg_subjectivity']} (range: 0 to 1)

───────────────────────────────────────────────────────────────
PLATFORM BREAKDOWN
───────────────────────────────────────────────────────────────
"""

        for platform, data in platform_sentiment.items():
            summary += f"""
{platform.upper()}:
  Total: {data['total']} posts
  ✅ Positive: {data['positive']} ({data['positive_pct']}%)
  ❌ Negative: {data['negative']} ({data['negative_pct']}%)
  ⚪ Neutral:  {data['neutral']} ({data['neutral_pct']}%)
"""

        summary += """
───────────────────────────────────────────────────────────────
Report generated by Social Media OSINT Analyzer
───────────────────────────────────────────────────────────────
"""

        return summary.strip()
