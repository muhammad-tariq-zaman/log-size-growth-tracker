# log-size-growth-tracker

Estimate growth per day for each log file from dated size observations and forecast the date it hits a size limit — fastest-growing first.

## How to run

```sh
python3 main.py sizes.csv --limit-mb 1000
```

## Example output

```
app.log: 10.0 MB/day, hits limit 2027-02-09
debug.log: 0.0 MB/day, NOT GROWING
```

Standard library only. Run the tests with `python3 -m unittest discover`.
