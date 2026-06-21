#!/usr/bin/env python3
import json, glob
d = {}
for f in glob.glob("*_dG.json"):
    j = json.load(open(f)); d[j["system"]] = j
if "wt" not in d:
    raise SystemExit("NO WT RESULT")
wt = d["wt"]["dG_bind"]
order = ["wt", "g12d", "g12c", "g12g", "q61h", "m67r"]
labels = {"wt":"G12V (crystal)", "g12d":"G12D", "g12c":"G12C",
          "g12g":"G12 (true WT)", "q61h":"Q61H", "m67r":"M67R (disruptor ctrl)"}
rows = []
print(f"{'system':22s} {'dG_bind':>9s} {'ddG_vs_G12V':>12s}")
for s in order:
    if s in d:
        ddg = round(d[s]["dG_bind"] - wt, 2)
        rows.append({"system":s, "label":labels[s], "dG_bind":d[s]["dG_bind"], "ddG":ddg})
        print(f"{labels[s]:22s} {d[s]['dG_bind']:9.2f} {ddg:12.2f}")
json.dump({"reference":"wt (G12V crystal)", "rows":rows,
  "method":"single-trajectory MM-GBSA (GBn2/igb8, mbondi3 radii), ff14SB + GAFF2; AM1-BCC GppNHp(4-), Gasteiger drug (cancels in relative ddG); 1.6 nm cutoff; single minimized snapshot, no entropy",
  "raw":d}, open("ddg_results.json","w"), indent=1)
print("wrote ddg_results.json")
