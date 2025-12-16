import argparse
import json
import os

import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="path to outputs/*.json")
    ap.add_argument("--outdir", default="outputs")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    series = payload["series"]
    t = [row["t"] for row in series]
    Eg = [row["E_geom"] for row in series]
    Eh = [row["E_heal"] for row in series]
    Ee = [row["E_entropy"] for row in series]
    d = [row["defects_count"] for row in series]

    os.makedirs(args.outdir, exist_ok=True)

    plt.figure()
    plt.plot(t, Eg, label="E_geom")
    plt.plot(t, Eh, label="E_heal")
    plt.plot(t, Ee, label="E_entropy")
    plt.xlabel("t")
    plt.ylabel("Energy")
    plt.legend()
    plt.grid(True)
    out1 = os.path.join(args.outdir, "energy_evolution.png")
    plt.savefig(out1, dpi=150)

    plt.figure()
    plt.plot(t, d)
    plt.xlabel("t")
    plt.ylabel("defects_count")
    plt.grid(True)
    out2 = os.path.join(args.outdir, "defects_count.png")
    plt.savefig(out2, dpi=150)

    # normalized defects diagnostic (δ_t / 20^t)
    norm = []
    for row in series:
        tt = row["t"]
        if tt <= 0:
            norm.append(0.0)
        else:
            norm.append(row["defects_count"] / (20.0 ** tt))
    plt.figure()
    plt.plot(t[1:], norm[1:])
    plt.xlabel("t")
    plt.ylabel("δ_t / 20^t")
    plt.grid(True)
    out3 = os.path.join(args.outdir, "normalized_defects.png")
    plt.savefig(out3, dpi=150)

    print("Wrote plots:")
    print(" -", out1)
    print(" -", out2)
    print(" -", out3)

if __name__ == "__main__":
    main()
