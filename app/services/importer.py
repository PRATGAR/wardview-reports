import csv

from lxml import etree

from .. import storage, xmlcfg
from ..repos import results as results_repo
from . import reference_ranges, unit_conversion


def _to_float(raw):
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def read_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for record in reader:
            analyte = (record.get("analyte") or "").strip()
            if not analyte:
                continue
            value, unit = unit_conversion.convert(
                analyte, _to_float(record.get("value")), record.get("unit")
            )
            rows.append(
                {
                    "analyte": analyte,
                    "value": value,
                    "unit": (unit or "").strip(),
                    "flag": reference_ranges.flag_for(analyte, value),
                }
            )
    return rows


def parse_payload(raw, profile):
    parser = xmlcfg.build_parser(profile)
    return etree.fromstring(raw, parser)


def extract_results(root):
    rows = []
    for node in root.iter("result"):
        analyte = (node.findtext("analyte") or "").strip()
        if not analyte:
            continue
        value, unit = unit_conversion.convert(
            analyte, _to_float(node.findtext("value")), node.findtext("unit")
        )
        rows.append(
            {
                "analyte": analyte,
                "value": value,
                "unit": (unit or "").strip(),
                "flag": reference_ranges.flag_for(analyte, value),
            }
        )
    return rows


def import_xml(order_id, raw, profile, source_name):
    root = parse_payload(raw, profile)
    rows = extract_results(root)
    stored_as = storage.save_bytes(raw)
    return results_repo.add_many(order_id, rows, source_name, stored_as)
