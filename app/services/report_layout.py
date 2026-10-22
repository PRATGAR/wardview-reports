from . import formatting, reference_ranges, trends


def build_sections(report, rows):
    flags = reference_ranges.summarise_flags(rows)
    sections = [
        {
            "heading": "Overview",
            "lines": [
                f"{len(rows)} result(s) included",
                f"{flags['C']} critical, {flags['H']} high, {flags['L']} low",
            ],
        }
    ]
    critical = trends.critical_analytes(rows)
    if critical:
        sections.append(
            {
                "heading": "Critical values",
                "lines": [f"{name}: {formatting.describe_flag('C')}" for name in critical],
            }
        )
    series = trends.compute_trends(rows)
    if series:
        sections.append(
            {
                "heading": "Trends",
                "lines": [
                    f"{name}: {stats['direction']} ({formatting.format_value(stats['last'], stats['unit'])})"
                    for name, stats in sorted(series.items())
                ],
            }
        )
    return sections
