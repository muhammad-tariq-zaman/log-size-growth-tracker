"""Forecast when log files will hit a size limit.

Usage: python3 main.py sizes.csv [--limit-mb 1000]
CSV columns: file,date,size_mb (one row per observation).
Growth per day is (last - first) / days between first and last
observation. Forecast days to the limit from the last observation;
SHRINKING files and files already over the limit are reported as such.
"""
import argparse, csv, sys
from collections import defaultdict
from datetime import date, timedelta


def forecast(rows, limit_mb):
    by_file = defaultdict(list)
    for row in rows:
        by_file[row["file"].strip()].append(
            (date.fromisoformat(row["date"].strip()), float(row["size_mb"])))
    out = []
    for name, points in by_file.items():
        points.sort()
        first_date, first_size = points[0]
        last_date, last_size = points[-1]
        days = (last_date - first_date).days
        growth = (last_size - first_size) / days if days > 0 else 0.0
        if last_size >= limit_mb:
            out.append((name, growth, "OVER LIMIT"))
        elif growth <= 0:
            out.append((name, growth, "NOT GROWING"))
        else:
            eta = last_date + timedelta(days=int((limit_mb - last_size) / growth))
            out.append((name, growth, f"hits limit {eta.isoformat()}"))
    return sorted(out, key=lambda r: r[1], reverse=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--limit-mb", type=float, default=1000)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        for name, growth, verdict in forecast(list(csv.DictReader(f)), args.limit_mb):
            print(f"{name}: {growth:.1f} MB/day, {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
