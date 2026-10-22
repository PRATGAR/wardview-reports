from statistics import fmean


def group_by_analyte(rows):
    grouped = {}
    for row in rows:
        if row["value"] is None:
            continue
        grouped.setdefault(row["analyte"], []).append(row)
    return grouped


def describe(values):
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": round(fmean(values), 3),
        "last": values[-1],
        "delta": round(values[-1] - values[0], 3),
    }


def direction(delta, tolerance=0.05):
    if delta > tolerance:
        return "rising"
    if delta < -tolerance:
        return "falling"
    return "stable"


def compute_trends(rows):
    trends = {}
    for analyte, entries in group_by_analyte(rows).items():
        values = [e["value"] for e in entries]
        stats = describe(values)
        stats["direction"] = direction(stats["delta"])
        stats["unit"] = entries[-1]["unit"]
        trends[analyte] = stats
    return trends


def critical_analytes(rows):
    seen = []
    for row in rows:
        if row["flag"] == "C" and row["analyte"] not in seen:
            seen.append(row["analyte"])
    return seen
