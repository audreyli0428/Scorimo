import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


def run_drift_report():
    reference = pd.read_csv("monitoring/reference_data.csv")
    current = pd.read_csv("data/processed/listings_clean.csv")

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)
    report.save_html("monitoring/drift_report.html")
    print("Drift report saved → open monitoring/drift_report.html")


if __name__ == "__main__":
    run_drift_report()