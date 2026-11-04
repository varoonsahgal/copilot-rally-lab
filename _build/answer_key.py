"""Compute reconciliation answer key from the generated workbooks."""
import json, re
from pathlib import Path
from openpyxl import load_workbook
ROOT = Path(__file__).resolve().parents[1]
a = load_workbook(ROOT/"data/session-1/Promo_Allocations_Requests.xlsx", data_only=True)
w = load_workbook(ROOT/"data/session-1/Warehouse_Fulfillment_Deliveries.xlsx", data_only=True)
def rows(ws):
    it = ws.iter_rows(values_only=True); h = next(it); return [dict(zip(h, r)) for r in it]
alloc = rows(a["Gate Allocations"]); req = {r["Request ID"]: r for r in rows(a["Requests"])}
items = {r["SKU"]: r for r in rows(a["Item Master"])}
dl = rows(w["Deliveries"])
def norm_req(x):
    d = re.sub(r"[^0-9]", "", str(x)); return f"PR-{d}"
def norm_sku(x):
    s = re.sub(r"[^A-Z0-9]", "", str(x).upper())
    for k in items:
        if re.sub(r"[^A-Z0-9]", "", k) == s: return k
    return s
naive = {}; seen=set(); clean = {}; dmg = {}; late = {}
for d in dl:
    k_raw = (d["Request Ref"], d["Destination"])
    naive[k_raw] = naive.get(k_raw, 0) + d["Qty"]
    if d["Delivery ID"] in seen: continue
    seen.add(d["Delivery ID"])
    sku = norm_sku(d["SKU"]); q = d["Qty"] * (items[sku]["Case Pack (units per case)"] if d["UOM"]=="CS" else 1)
    k = (norm_req(d["Request Ref"]), d["Destination"])
    if str(d["Delivery Date"])[:10] > str(req[k[0]]["Game Date"])[:10]:
        late[k] = late.get(k,0)+q; continue
    clean[k] = clean.get(k, 0) + q; dmg[k] = dmg.get(k, 0) + (d["Damaged Qty"] or 0)
out = []
for al in alloc:
    k = (al["Request ID"], al["Gate"])
    exact = naive.get(k, 0)
    delivered = clean.get(k, 0); dist = delivered - dmg.get(k, 0)
    var = dist - al["Allocated Qty"]
    out.append(dict(req=k[0], gate=k[1], status=req[k[0]]["Status"], allocated=al["Allocated Qty"], naive_exact=exact,
                    delivered_clean=delivered, damaged=dmg.get(k,0), distributable=dist, late=late.get(k,0), variance=var,
                    pct=round(var/al["Allocated Qty"]*100,1)))
for o in out: print(o)
tot = {}
for o in out:
    t = tot.setdefault(o["req"], dict(allocated=0, distributable=0, damaged=0, delivered=0, late=0))
    t["allocated"]+=o["allocated"]; t["distributable"]+=o["distributable"]; t["damaged"]+=o["damaged"]; t["delivered"]+=o["delivered_clean"]; t["late"]+=o["late"]
print(json.dumps(tot, indent=1))
# naive total by sku (sum Qty column by SKU text contains)
nv = {}
for d in dl:
    nv[norm_sku(d["SKU"])] = nv.get(norm_sku(d["SKU"]),0)+d["Qty"]
print("naive Qty sum by normalized SKU", nv)
