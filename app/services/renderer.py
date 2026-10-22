from flask import render_template, render_template_string

from . import report_layout


def sample_context():
    return {
        "patient_name": "Sample Patient",
        "mrn": "00000000",
        "rows": [
            {"analyte": "Glucose", "value": 5.1, "unit": "mmol/L", "flag": "N"},
            {"analyte": "Potassium", "value": 5.4, "unit": "mmol/L", "flag": "H"},
        ],
    }


def render_stored(body, context):
    return render_template_string(body, **context)


def report_html(report, rows):
    return render_template(
        "report_pdf.html",
        report=report,
        rows=rows,
        sections=report_layout.build_sections(report, rows),
    )
