#!/usr/bin/env python3
"""Render perturb/funnel.json as a self-contained inline SVG energy funnel.
Emits perturb/funnel.svg."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
f = json.load(open(os.path.join(HERE, "funnel.json")))
dec, env, nat, chai = f["decoys"], f["envelope"], f["native"], f["chai"]

# light-theme palette
P = dict(ink="#161b26", muted="#5c6675", faint="#8a94a6", grid="#e9ecf2",
         frame="#d7dce6", zero="#b7bfca", favzone="#15a34a", clashzone="#dc2626",
         favdot="#15a34a", clashdot="#9aa3b2", env="#0ea5e9",
         nat="#15a34a", natsub="#15803d", chai="#d97706", chaisub="#b45309",
         offscale="#dc2626")

W, H = 760, 460
ML, MR, MT, MB = 64, 18, 48, 56
PW, PH = W-ML-MR, H-MT-MB
RMAX = 32.0
EMAX, EMIN = 60.0, -30.0     # clip window (severe clashes go off the top)
def X(r): return ML + min(r, RMAX)/RMAX*PW
def Y(e):
    e = max(EMIN, min(EMAX, e)); return MT + (EMAX-e)/(EMAX-EMIN)*PH

s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
     f'font-family="ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif" '
     f'role="img" aria-label="Interface-energy funnel: the crystal pose is the global minimum at -25 kcal/mol; '
     f'the Chai-1 prediction sits 23 angstrom away at +53 kcal/mol in a clashing regime, flagged by its own ipTM 0.63">']
# zones
s.append(f'<rect x="{ML}" y="{Y(EMAX):.1f}" width="{PW}" height="{Y(0)-Y(EMAX):.1f}" fill="{P["clashzone"]}" opacity="0.05"/>')
s.append(f'<rect x="{ML}" y="{Y(0):.1f}" width="{PW}" height="{Y(EMIN)-Y(0):.1f}" fill="{P["favzone"]}" opacity="0.07"/>')
# gridlines + y labels
for e in (60,40,20,0,-20):
    y=Y(e); s.append(f'<line x1="{ML}" y1="{y:.1f}" x2="{ML+PW}" y2="{y:.1f}" stroke="{P["grid"]}" stroke-width="1"/>')
    s.append(f'<text x="{ML-8}" y="{y+3:.1f}" fill="{P["faint"]}" font-size="11" text-anchor="end">{e:+d}</text>')
# x ticks
for r in (0,5,10,15,20,25,30):
    x=X(r); s.append(f'<line x1="{x:.1f}" y1="{MT+PH}" x2="{x:.1f}" y2="{MT+PH+4}" stroke="{P["frame"]}" stroke-width="1"/>')
    s.append(f'<text x="{x:.1f}" y="{MT+PH+18}" fill="{P["faint"]}" font-size="11" text-anchor="middle">{r}</text>')
# frame
s.append(f'<rect x="{ML}" y="{MT}" width="{PW}" height="{PH}" fill="none" stroke="{P["frame"]}" stroke-width="1.2"/>')
# E=0 reference
s.append(f'<line x1="{ML}" y1="{Y(0):.1f}" x2="{ML+PW}" y2="{Y(0):.1f}" stroke="{P["zero"]}" stroke-width="1.2" stroke-dasharray="5 4"/>')
s.append(f'<text x="{ML+PW-6}" y="{Y(0)-6:.1f}" fill="{P["faint"]}" font-size="10.5" text-anchor="end">no net interface (E = 0)</text>')
# decoy cloud
off=0
for d in dec:
    r,e = d["rmsd"], d["e"]
    if r==0 and abs(e-nat["e"])<1e-6: continue
    if e>EMAX:
        off+=1; s.append(f'<path d="M {X(r):.1f} {MT+3} l 3 5 l -6 0 z" fill="{P["offscale"]}" opacity="0.16"/>')
    else:
        col = P["favdot"] if e<0 else P["clashdot"]
        op  = 0.55 if e<0 else 0.4
        s.append(f'<circle cx="{X(r):.1f}" cy="{Y(e):.1f}" r="2.4" fill="{col}" opacity="{op}"/>')
# funnel envelope
pts=" ".join(f"{X(p['rmsd']):.1f},{Y(p['e']):.1f}" for p in env if p["rmsd"]<=RMAX)
s.append(f'<polyline points="{pts}" fill="none" stroke="{P["env"]}" stroke-width="2.4"/>')
s.append(f'<text x="{X(7):.1f}" y="{Y(-9):.1f}" fill="{P["env"]}" font-size="10.5" font-weight="600">min-energy envelope</text>')
# Chai-1 prediction marker
cx,cy=X(chai["rmsd"]),Y(chai["e"])
s.append(f'<path d="M {cx:.1f} {cy-8:.1f} l 8 8 l -8 8 l -8 -8 z" fill="{P["chai"]}" stroke="#fff" stroke-width="1.5"/>')
s.append(f'<text x="{cx-12:.1f}" y="{cy-12:.1f}" fill="{P["chai"]}" font-size="12" font-weight="700" text-anchor="end">Chai-1 prediction</text>')
s.append(f'<text x="{cx-12:.1f}" y="{cy+2:.1f}" fill="{P["chaisub"]}" font-size="10.5" text-anchor="end">23 &#197; off &#183; +53 kcal/mol &#183; ipTM 0.63</text>')
# native crystal pose star
nx,ny=X(0),Y(nat["e"])
star=" ".join(f"{nx+9*math.cos(a):.1f},{ny+9*math.sin(a):.1f} {nx+3.8*math.cos(a+math.pi/5):.1f},{ny+3.8*math.sin(a+math.pi/5):.1f}"
              for a in [(-90+72*k)*math.pi/180 for k in range(5)])
s.append(f'<polygon points="{star}" fill="{P["nat"]}" stroke="#fff" stroke-width="1.1"/>')
s.append(f'<text x="{nx+14:.1f}" y="{ny-6:.1f}" fill="{P["nat"]}" font-size="12" font-weight="700">crystal pose</text>')
s.append(f'<text x="{nx+14:.1f}" y="{ny+8:.1f}" fill="{P["natsub"]}" font-size="10.5">&#8722;25 kcal/mol &#183; global minimum</text>')
# axis titles
s.append(f'<text x="{ML+PW/2:.1f}" y="{H-8}" fill="{P["muted"]}" font-size="12" text-anchor="middle">KRAS displacement from crystal pose (C&#945; RMSD, &#197;)</text>')
s.append(f'<text x="16" y="{MT+PH/2:.1f}" fill="{P["muted"]}" font-size="12" text-anchor="middle" transform="rotate(-90 16 {MT+PH/2:.1f})">interface energy (kcal/mol)</text>')
s.append(f'<text x="{ML}" y="{MT-18}" fill="{P["ink"]}" font-size="13.5" font-weight="700">Stop predicting, start scoring: the crystal pose is the energy minimum</text>')
s.append(f'<text x="{ML}" y="{MT-4}" fill="{P["muted"]}" font-size="11">{f["stats"]["n_decoys"]} rigid-body KRAS decoys &#183; soft van der Waals interface energy &#183; CypA&#183;drug composite held fixed</text>')
s.append('</svg>')
open(os.path.join(HERE,"funnel.svg"),"w").write("\n".join(s))
print("wrote funnel.svg", len("\n".join(s)), "chars; off-scale clash decoys:", off)
