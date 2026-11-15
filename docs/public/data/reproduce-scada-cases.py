"""Prepare the Aventa and ENGIE CSVs from their published source files."""

import argparse
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd


def prepare_aventa(source, output):
    fields = {
        "wind_speed": "wind_ms",
        "generator_speed": "generator_rpm",
        "power_output": "power_kw",
        "blade_pitch_deg": "pitch_deg",
    }
    data = pd.read_parquet(source, columns=["datetime", *fields])
    time = pd.to_datetime(data.pop("datetime"), utc=True)
    data = data.rename(columns=fields).set_index(time).sort_index()
    date_range = (data.index >= "2025-06-04") & (data.index < "2025-06-11")
    valid = np.isfinite(data).all(axis=1) & data.wind_ms.ge(0) & data.generator_rpm.ge(0)
    groups = data.loc[date_range & valid].resample("min")
    minute_means = groups.mean().loc[groups.size().ge(55)]
    minute_means.to_csv(
        output, index_label="time_utc", date_format="%Y-%m-%dT%H:%M:%SZ", float_format="%.5f"
    )
    print(f"Aventa retained minute windows: {len(minute_means)}")


def prepare_engie(source, output):
    fields = {
        "Wind_turbine_name": "turbine",
        "Ba_avg": "pitch_deg",
        "P_avg": "power_kw",
        "Ws_avg": "wind_ms",
    }
    with ZipFile(source) as archive, archive.open("la-haute-borne-data-2014-2015.csv") as raw:
        data = pd.read_csv(raw, usecols=["Date_time", *fields]).rename(columns=fields)
    data = data.loc[data.turbine.eq("R80711")].copy()
    data["time_utc"] = pd.to_datetime(data.pop("Date_time"), utc=True)
    data = data.set_index("time_utc").sort_index().loc["2014-02-01":"2014-03-31", list(fields.values())]

    # Identical projected observations may share a key. Keep one such observation.
    data = data.reset_index().drop_duplicates()
    conflicts = data["time_utc"].duplicated(keep=False)
    print(f"ENGIE conflict keys: {data.loc[conflicts, 'time_utc'].nunique()}")
    data = data.loc[~conflicts].set_index("time_utc")
    data["generating_sample"] = (
        np.isfinite(data[["wind_ms", "power_kw", "pitch_deg"]]).all(axis=1) & data.power_kw.gt(0)
    )
    data.to_csv(output, float_format="%.5f")
    print(f"ENGIE retained rows: {len(data)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aventa", type=Path, help="OST_Aventa.parquet")
    parser.add_argument("--engie", type=Path, help="OpenOA la_haute_borne.zip")
    parser.add_argument("--output-dir", type=Path, default=Path("reproduced-data"))
    args = parser.parse_args()
    if args.aventa is None and args.engie is None:
        parser.error("provide --aventa, --engie, or both")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.aventa:
        prepare_aventa(args.aventa, args.output_dir / "aventa-linked-scatter.csv")
    if args.engie:
        prepare_engie(args.engie, args.output_dir / "engie-r80711-2014-02-03.csv")
