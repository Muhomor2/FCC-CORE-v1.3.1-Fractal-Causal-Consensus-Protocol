import argparse
import os

from fcc_core.params import FCCParameters
from fcc_core.simulation import run_simulation, export_run

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--T", type=int, default=12, help="max level (steps)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default="", help="output json path")
    args = ap.parse_args()

    params = FCCParameters()
    states = run_simulation(args.T, params, seed=args.seed)

    os.makedirs("outputs", exist_ok=True)
    out_path = args.out or f"outputs/run_T{args.T}_seed{args.seed}.json"
    export_run(states, params, out_path)
    print(f"Wrote: {out_path}")

if __name__ == "__main__":
    main()
