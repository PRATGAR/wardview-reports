import csv
import os
import subprocess

from flask import current_app

from .. import storage
from ..repos import results as results_repo
from . import renderer


def output_path(report):
    return os.path.join(current_app.config["EXPORT_DIR"], report["export_name"] + ".pdf")


def write_html(report):
    rows = results_repo.for_patient(report["patient_id"])
    path = storage.new_export_path("html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(renderer.report_html(report, rows))
    return path


def write_csv(report, rows):
    path = storage.new_export_path("csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["analyte", "value", "unit", "flag"])
        for row in rows:
            writer.writerow([row["analyte"], row["value"], row["unit"], row["flag"]])
    return path


def _invoke_tool(command):
    timeout = current_app.config["TOOL_TIMEOUT_SECONDS"]
    return subprocess.run(command, shell=True, check=True, timeout=timeout)


def build_pdf(report):
    html_path = write_html(report)
    out_path = output_path(report)
    tool = current_app.config["PDF_TOOL"]
    _invoke_tool(f"{tool} --quiet {html_path} {out_path}")
    return out_path
