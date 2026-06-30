#!/usr/bin/env python3
"""Render ddg_results.json as a light-theme inline SVG bar chart.
ddG relative to the G12V crystal; auto-scales; colors by tolerated (|ddG| small) vs
destabilizing (large +). Writes ddg.svg."""
import json, os
HERE=os.path.dirname(os.path.abspath(__file__))
DDG=os.path.join(HERE, "..")   # canonical results/chart live in demos/kras-glue/ddg/
R=json.load(open(os.path.join(DDG,"ddg_results.json")))
rows=[r for r in R["rows"] if r["system"]!="wt"]   # wt is the 0 reference
P=dict(ink="#161b26",muted="#5c6675",faint="#8a94a6",grid="#e9ecf2",frame="#d7dce6",
       zero="#9aa3b2",tol="#15a34a",bad="#dc2626",warn="#d97706")
W,H=720,420; ML,MR,MT,MB=70,20,54,90; PW,PH=W-ML-MR,H-MT-MB
vals=[r["ddG"] for r in rows] or [0]
lo=min(0,min(vals)); hi=max(0,max(vals)); pad=max(2.0,(hi-lo)*0.15); lo-=pad; hi+=pad
def Y(v): return MT+(hi-v)/(hi-lo)*PH
n=len(rows); bw=PW/max(1,n)*0.62
TOL=2.5  # |ddG| below this = "tolerated" band (kcal/mol), generous for single-snapshot
s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif" role="img" aria-label="MM-GBSA ddG of KRAS mutations relative to the G12V crystal">']
# tolerated band
yb1,yb2=Y(TOL),Y(-TOL)
s.append(f'<rect x="{ML}" y="{yb1:.1f}" width="{PW}" height="{yb2-yb1:.1f}" fill="{P["tol"]}" opacity="0.07"/>')
s.append(f'<text x="{ML+6}" y="{yb1-4:.1f}" fill="{P["tol"]}" font-size="10.5">tolerated window (|&#916;&#916;G| &lt; {TOL:.0f})</text>')
# y gridlines
import math
step=max(1,round((hi-lo)/6))
g=math.floor(lo/step)*step
while g<=hi:
    y=Y(g); s.append(f'<line x1="{ML}" y1="{y:.1f}" x2="{ML+PW}" y2="{y:.1f}" stroke="{P["grid"]}" stroke-width="1"/>')
    s.append(f'<text x="{ML-8}" y="{y+3:.1f}" fill="{P["faint"]}" font-size="11" text-anchor="end">{g:+d}</text>'); g+=step
s.append(f'<line x1="{ML}" y1="{Y(0):.1f}" x2="{ML+PW}" y2="{Y(0):.1f}" stroke="{P["zero"]}" stroke-width="1.4"/>')
s.append(f'<rect x="{ML}" y="{MT}" width="{PW}" height="{PH}" fill="none" stroke="{P["frame"]}" stroke-width="1.2"/>')
for i,r in enumerate(rows):
    cx=ML+(i+0.5)*PW/n; v=r["ddG"]; y0=Y(0); y1=Y(v)
    col=P["bad"] if v>TOL else (P["warn"] if v<-TOL else P["tol"])
    top=min(y0,y1); hgt=abs(y1-y0)
    s.append(f'<rect x="{cx-bw/2:.1f}" y="{top:.1f}" width="{bw:.1f}" height="{hgt:.1f}" rx="3" fill="{col}" opacity="0.85"/>')
    s.append(f'<text x="{cx:.1f}" y="{(top-6) if v>=0 else (top+hgt+14):.1f}" fill="{col}" font-size="11.5" font-weight="700" text-anchor="middle">{v:+.1f}</text>')
    lab=r["label"].replace(" (disruptor ctrl)","").replace(" (crystal)","").replace(" (true WT)","")
    s.append(f'<text x="{cx:.1f}" y="{MT+PH+20:.1f}" fill="{P["muted"]}" font-size="11.5" font-weight="600" text-anchor="middle">{lab}</text>')
    sub="disruptor ctrl" if r["system"]=="m67r" else ("true WT" if r["system"]=="g12g" else "pan-RAS")
    s.append(f'<text x="{cx:.1f}" y="{MT+PH+34:.1f}" fill="{P["faint"]}" font-size="9.5" text-anchor="middle">{sub}</text>')
s.append(f'<text x="16" y="{MT+PH/2:.1f}" fill="{P["muted"]}" font-size="12" text-anchor="middle" transform="rotate(-90 16 {MT+PH/2:.1f})">&#916;&#916;G binding vs G12V (kcal/mol)</text>')
s.append(f'<text x="{ML}" y="{MT-30}" fill="{P["ink"]}" font-size="13.5" font-weight="700">MM-GBSA mutation scan: pan-RAS mutations tolerated, disruptor destabilizing</text>')
s.append(f'<text x="{ML}" y="{MT-15}" fill="{P["muted"]}" font-size="11">single-trajectory MM-GBSA (GBn2) on the daraxonrasib&#183;CypA&#183;KRAS&#183;GppNHp&#183;Mg scaffold &#183; ddG vs the G12V crystal</text>')
s.append('</svg>')
open(os.path.join(DDG,"ddg.svg"),"w").write("\n".join(s))
print("wrote ddg.svg")
