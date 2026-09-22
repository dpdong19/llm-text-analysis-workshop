"""Compare a classification run against the instructor reference set.

Usage:
    python compare.py                          # defaults below
    python compare.py --results output/results.jsonl \
                      --reference reference_set_final.csv \
                      --data data/airline_reviews_sample_50.csv

Only reviews covered by the reference set are compared. Reviews in the
reference but missing from your results are reported as NOT CLASSIFIED.

The reference is the instructors' adjudicated annotation — a comparison
baseline, not ground truth. A difference is a discussion starter, not
an error.
"""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

SNIPPET_LEN = 80


def load_reference(path):
    """reference CSV (long format) -> {review_id: {topic: sentiment}}"""
    ref = defaultdict(dict)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ref[row["review_id"]][row["topic"]] = row["sentiment"]
    return dict(ref)


def load_results(path):
    """results.jsonl -> {review_id: {topic: sentiment}}"""
    runs = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            runs[rec["review_id"]] = {
                a["topic"]: a["sentiment"] for a in rec["aspects"]
            }
    return runs


def load_snippets(path):
    """review_id -> first SNIPPET_LEN chars of the review text"""
    snippets = {}
    if not Path(path).exists():
        return snippets
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            text = " ".join(row["review_text"].split())
            snippets[row["review_id"]] = (
                text[:SNIPPET_LEN] + ("…" if len(text) > SNIPPET_LEN else "")
            )
    return snippets


def compare_review(ref_aspects, run_aspects):
    """Return list of (kind, topic, detail) differences. Empty = agree."""
    diffs = []
    for topic, ref_sent in sorted(ref_aspects.items()):
        if topic not in run_aspects:
            diffs.append(("MISSING", topic, f"reference: {ref_sent} — your run did not tag this"))
        elif run_aspects[topic] != ref_sent:
            diffs.append(("SENTIMENT", topic, f"reference: {ref_sent}, your run: {run_aspects[topic]}"))
    for topic, run_sent in sorted(run_aspects.items()):
        if topic not in ref_aspects:
            diffs.append(("EXTRA", topic, f"your run: {run_sent} — the reference does not tag this"))
    return diffs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", default="output/results.jsonl")
    parser.add_argument("--reference", default="reference_set_final.csv")
    parser.add_argument("--data", default="data/airline_reviews_sample_50.csv")
    args = parser.parse_args()

    reference = load_reference(args.reference)
    results = load_results(args.results)
    snippets = load_snippets(args.data)

    n_agree = n_differ = n_missing = 0
    differing = []
    csv_rows = []

    print(f"Comparing against reference set: {len(reference)} reviews\n")

    for review_id in sorted(reference):
        if review_id not in results:
            n_missing += 1
            csv_rows.append([review_id, "NOT CLASSIFIED", "", "", "", ""])
            print(f"{review_id}  NOT CLASSIFIED (no record in your results)")
            continue

        diffs = compare_review(reference[review_id], results[review_id])
        if not diffs:
            n_agree += 1
            csv_rows.append([review_id, "AGREE", "", "", "", ""])
            print(f"{review_id}  AGREE")
        else:
            n_differ += 1
            differing.append(review_id)
            print(f"{review_id}  DIFFERS from reference")
            if review_id in snippets:
                print(f'    "{snippets[review_id]}"')
            for kind, topic, detail in diffs:
                ref_sent = reference[review_id].get(topic, "")
                run_sent = results[review_id].get(topic, "")
                csv_rows.append([review_id, "DIFFERS", kind, topic, ref_sent, run_sent])
                print(f"    {kind}: {topic}")
                print(f"      → {detail}")
        print()

    # Write CSV for easy viewing in Excel
    csv_path = Path("output") / "comparison.csv"
    csv_path.parent.mkdir(exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["review_id", "status", "diff_type", "topic", "reference_sentiment", "your_sentiment"])
        writer.writerows(csv_rows)

    print("-" * 60)
    print(
        f"Summary: {n_agree} of {len(reference)} match the instructor reference; "
        f"{n_differ} differ"
        + (f"; {n_missing} not classified" if n_missing else "")
        + "."
    )
    if differing:
        print(f"Differing reviews: {', '.join(differing)}")
        print("Bring the differences to discussion.")
    print(f"\nDetailed comparison saved to {csv_path} (open in Excel).")
    print(
        "\nNote: the reference is the instructors' adjudicated annotation —\n"
        "it is a comparison baseline, not ground truth. A difference is a\n"
        "discussion starter, not an error."
    )


if __name__ == "__main__":
    main()
