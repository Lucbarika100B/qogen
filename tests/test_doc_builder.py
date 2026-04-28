from pathlib import Path
from qogen.doc_builder import build_one_pager


def test_builds_docx(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    out = build_one_pager(
        product_name="Acme Sentinel",
        tagline="Watch your data without moving it",
        features=[
            "Zero data movement",
            "Real-time scans",
            "Compliance-first design",
        ],
        audience="Mid-market security teams",
        body_copy=(
            "Acme Sentinel monitors sensitive data in place, eliminating "
            "the risk of duplication or transit exposure."
        ),
    )
    assert Path(out).exists()
    assert Path(out).stat().st_size > 0