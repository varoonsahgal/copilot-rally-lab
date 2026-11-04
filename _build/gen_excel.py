"""
Generates all FICTIONAL Excel training workbooks for the
Riverfront Rally Weekend Copilot labs.

Run:  python _build/gen_excel.py
"""
import datetime as dt
import json
import random
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.formatting.rule import CellIsRule, DataBarRule

ROOT = Path(__file__).resolve().parents[1]
OUT1 = ROOT / "data" / "session-1"
OUT2 = ROOT / "data" / "session-2"
OUT1.mkdir(parents=True, exist_ok=True)
OUT2.mkdir(parents=True, exist_ok=True)

RED = "C6011F"
INK = "1B1B1F"
CREAM = "F7F3EA"
HDR_FONT = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
HDR_FILL = PatternFill("solid", fgColor=RED)
INK_FILL = PatternFill("solid", fgColor=INK)
CREAM_FILL = PatternFill("solid", fgColor=CREAM)
THIN = Side(style="thin", color="D9D4C7")
D = dt.date


def add_table(ws, name, headers, rows, widths=None, style="TableStyleLight1",
              number_formats=None, header_fill=HDR_FILL):
    ws.append(headers)
    for r in rows:
        ws.append(r)
    nrows = len(rows) + 1
    ref = f"A1:{get_column_letter(len(headers))}{nrows}"
    t = Table(displayName=name, ref=ref)
    t.tableStyleInfo = TableStyleInfo(name=style, showRowStripes=True)
    ws.add_table(t)
    for c in ws[1]:
        c.font = HDR_FONT
        c.fill = header_fill
        c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "A2"
    for i, h in enumerate(headers, start=1):
        w = (widths or {}).get(h, max(12, min(40, len(h) + 4)))
        ws.column_dimensions[get_column_letter(i)].width = w
    if number_formats:
        for h, fmt in number_formats.items():
            if h in headers:
                col = headers.index(h) + 1
                for r in range(2, nrows + 1):
                    ws.cell(row=r, column=col).number_format = fmt
    return t


def readme(ws, title, subtitle, lines):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 90
    for r in range(1, 60):
        for c in range(1, 5):
            ws.cell(row=r, column=c).fill = CREAM_FILL
    ws["B2"] = title
    ws["B2"].font = Font(name="Calibri", size=22, bold=True, color=RED)
    ws["B3"] = subtitle
    ws["B3"].font = Font(name="Calibri", size=12, italic=True, color="5A5A5A")
    ws["B4"] = "FICTIONAL TRAINING DATA - created for Microsoft 365 Copilot workshops. Not real team, sponsor or fan data."
    ws["B4"].font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    ws["B4"].fill = INK_FILL
    ws.merge_cells("B4:C4")
    r = 6
    for k, v in lines:
        ws.cell(row=r, column=2, value=k).font = Font(bold=True, color=INK)
        cell = ws.cell(row=r, column=3, value=v)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=r, column=2).alignment = Alignment(vertical="top")
        r += 1


# ---------------------------------------------------------------------------
# Shared reference data
# ---------------------------------------------------------------------------
ITEMS = [
    # sku, description, unit cost, case pack, vendor, lead time days
    ("MAG-SCHED27", "Magnet Schedule", 0.42, 250, "Fridgeline Promo Co.", 21),
    ("TWL-RR27", "Riverfront Rally Towel", 1.15, 100, "Banner Day Textiles", 28),
    ("BBH-RETRO27", "Retro Bobblehead", 6.40, 24, "Nod & Wobble Collectibles", 56),
    ("BAT-MINI27", "Kids Mini Bat", 2.85, 50, "Little Slugger Supply", 35),
    ("HAT-BKT27", "Sunday Bucket Hat", 4.10, 40, "Seventh Inning Headwear", 21),
    ("KEY-STAR27", "Stars & Stripes Keychain", 0.95, 200, "Fridgeline Promo Co.", 21),
]
COST = {i[0]: i[2] for i in ITEMS}
CASE = {i[0]: i[3] for i in ITEMS}

GATES = ["Home Plate Gate", "Riverside Gate", "Third Base Gate", "Right Field Gate", "Club Entrance"]

REQUESTS = [
    # id, game date, game label, promotion, sku, item, sponsor, requested, approved,
    # fulfillment type, status, requested by, approved by, approval date, notes
    ("PR-1039", D(2027, 6, 15), "Tue 6/15 vs Lakeshore Lumberjacks", "Magnet Schedule Night", "MAG-SCHED27",
     "Magnet Schedule", "Blue Chip Hardware", 10000, 10000, "Warehouse", "Cancelled", "D. Whitfield",
     "E. Ortiz", D(2027, 4, 2), "Sponsor moved promotion to 7/13. Cancelled 5/18 - see email."),
    ("PR-1041", D(2027, 6, 18), "Fri 6/18 vs Allegheny Ironmen", "Rally Towel + Fireworks Friday", "TWL-RR27",
     "Riverfront Rally Towel", "Harbor City Mutual", 20000, 20000, "Warehouse", "Approved", "D. Whitfield",
     "E. Ortiz", D(2027, 4, 9), "First 20,000 fans."),
    ("PR-1043", D(2027, 6, 19), "Sat 6/19 vs Allegheny Ironmen", "Retro Bobblehead Night", "BBH-RETRO27",
     "Retro Bobblehead", "Riverbend Health Partners", 15000, 15000, "Warehouse", "Approved", "D. Whitfield",
     "E. Ortiz", D(2027, 3, 12), "First 15,000 fans. Sponsor contract guarantees 15,000 distributed."),
    ("PR-1048", D(2027, 6, 20), "Sun 6/20 vs Allegheny Ironmen", "Father's Day Family Sunday", "BAT-MINI27",
     "Kids Mini Bat", "Lakeside Fresh Market", 10000, 10000, "Warehouse", "Approved", "S. Kowalski",
     "E. Ortiz", D(2027, 4, 16), "First 10,000 kids 14 & under."),
    ("PR-1052", D(2027, 6, 18), "Fri 6/18 vs Allegheny Ironmen", "Postgame Fireworks", "SVC-FWK",
     "Fireworks Show (vendor service)", "Harbor City Mutual", 1, 1, "Vendor Service", "Approved", "D. Whitfield",
     "E. Ortiz", D(2027, 4, 9), "Vendor: Skyburst Pyrotechnics. No warehouse delivery expected."),
    ("PR-1057", D(2027, 6, 20), "Sun 6/20 vs Allegheny Ironmen", "Season Ticket Member Bucket Hat", "HAT-BKT27",
     "Sunday Bucket Hat", "Big River Energy Co.", 5000, 5000, "Warehouse", "Approved", "J. Pierce",
     "J. Pierce (per E. Ortiz email)", D(2027, 5, 27), "Added late. Season Ticket Members only - Home Plate & Club."),
    ("PR-1060", D(2027, 7, 2), "Fri 7/2 vs Capital Statesmen", "Stars & Stripes Keychain", "KEY-STAR27",
     "Stars & Stripes Keychain", "Harbor City Mutual", 12000, 12000, "Warehouse", "Approved", "D. Whitfield",
     "E. Ortiz", D(2027, 5, 3), "July promotion - ships to Central Warehouse, not gates."),
]

SPLITS = {
    "PR-1039": [3000, 2000, 2000, 2000, 1000],
    "PR-1041": [6000, 4000, 4000, 4000, 2000],
    "PR-1043": [4500, 3000, 3000, 3000, 1500],
    "PR-1048": [3000, 2000, 2000, 2000, 1000],
    "PR-1057": [2500, 0, 0, 0, 2500],
}

# ---------------------------------------------------------------------------
# Workbook 1: Promotional Allocations & Requests (Marketing / Sponsorship)
# ---------------------------------------------------------------------------
def build_allocations(with_deliveries=False):
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    readme(ws, "Promotional Allocations & Requests",
           "June Homestand 2027 - Marketing & Sponsorship master list (export of 6/16/2027 8:05 AM)",
           [
               ("Owner", "Promotions & Marketing (Dana Whitfield). Sponsorship adds sponsor-funded requests."),
               ("Requests", "One row per promotional request. Status is entered by the requester."),
               ("Gate Allocations", "How each approved request is split across the five ballpark gates."),
               ("Item Master", "SKU reference: unit cost, case pack and vendor lead time."),
               ("Sponsor Commitments", "What we promised each sponsor - guaranteed quantities and make-good clauses."),
               ("Matching key", "Request ID (PR-####) + Gate. Warehouse records SHOULD use the same Request ID."),
               ("Approval policy", "A new or changed giveaway needs: (1) signed sponsor amendment, (2) VP Marketing "
                                   "approval, (3) Ballpark Operations capacity sign-off. Promo lock date: June 4, 2027."),
               ("Companion file", "Warehouse_Fulfillment_Deliveries.xlsx (Warehouse & Logistics)."),
           ])

    ws = wb.create_sheet("Requests")
    headers = ["Request ID", "Game Date", "Game", "Promotion", "SKU", "Item", "Sponsor", "Requested Qty",
               "Approved Qty", "Unit Cost", "Est. Item Cost", "Fulfillment Type", "Status", "Requested By",
               "Approved By", "Approval Date", "Notes"]
    rows = []
    for r in REQUESTS:
        rid, gd, game, promo, sku, item, sponsor, req, appr, ftype, status, rb, ab, ad, notes = r
        unit = COST.get(sku, 65000.0 if sku == "SVC-FWK" else 0)
        rows.append([rid, gd, game, promo, sku, item, sponsor, req, appr, unit, round(unit * appr, 2),
                     ftype, status, rb, ab, ad, notes])
    add_table(ws, "tblRequests", headers, rows,
              widths={"Game": 32, "Promotion": 32, "Item": 28, "Sponsor": 26, "Notes": 60, "Approved By": 28,
                      "Fulfillment Type": 16},
              number_formats={"Game Date": "ddd m/d/yyyy", "Approval Date": "m/d/yyyy",
                              "Requested Qty": "#,##0", "Approved Qty": "#,##0",
                              "Unit Cost": "$#,##0.00", "Est. Item Cost": "$#,##0"})

    ws = wb.create_sheet("Gate Allocations")
    headers = ["Allocation ID", "Request ID", "Game Date", "SKU", "Item", "Gate", "Allocated Qty",
               "Gate Staff Assigned", "Distribution Window"]
    rows = []
    req = {r[0]: r for r in REQUESTS}
    for rid, split in SPLITS.items():
        r = req[rid]
        n = 1
        for gate, q in zip(GATES, split):
            if q == 0:
                continue
            staff = max(2, round(q / 1250))
            if rid == "PR-1057":
                staff = 0  # never staffed - pending Ops sign-off
            window = "Gates open +45 min" if rid != "PR-1057" else "TBD"
            rows.append([f"AL-{rid[3:]}-{n:02d}", rid, r[1], r[4], r[5], gate, q, staff, window])
            n += 1
    rows.append(["AL-1060-01", "PR-1060", D(2027, 7, 2), "KEY-STAR27", "Stars & Stripes Keychain",
                 "Central Warehouse (pre-stage)", 12000, 0, "N/A - July"])
    add_table(ws, "tblGateAllocations", headers, rows,
              widths={"Item": 28, "Gate": 28, "Distribution Window": 22},
              number_formats={"Game Date": "ddd m/d/yyyy", "Allocated Qty": "#,##0"})

    ws = wb.create_sheet("Item Master")
    headers = ["SKU", "Description", "Unit Cost", "Case Pack (units per case)", "Vendor", "Vendor Lead Time (days)"]
    rows = [list(i) for i in ITEMS]
    add_table(ws, "tblItems", headers, rows, widths={"Description": 28, "Vendor": 28},
              number_formats={"Unit Cost": "$#,##0.00"})

    ws = wb.create_sheet("Sponsor Commitments")
    headers = ["Sponsor", "Promotion", "Game Date", "Contract Status", "Sponsorship Fee", "Guaranteed Qty",
               "Make-Good Clause", "Logo Approval", "Contact"]
    rows = [
        ["Harbor City Mutual", "Rally Towel + Fireworks Friday", D(2027, 6, 18), "Signed 3/30/2027", 60000, 20000,
         "If fewer than 20,000 towels distributed: $3 credit per unit short.", "Approved 4/22", "Lena Hargrove"],
        ["Riverbend Health Partners", "Retro Bobblehead Night", D(2027, 6, 19), "Signed 2/26/2027", 110000, 15000,
         "If fewer than 15,000 bobbleheads distributed: $8 credit per unit short OR replacement promotion night.",
         "Approved 3/18", "Dr. Marcus Feld"],
        ["Lakeside Fresh Market", "Father's Day Family Sunday", D(2027, 6, 20), "Signed 4/8/2027", 45000, 10000,
         "If fewer than 10,000 mini bats distributed: $2 credit per unit short.", "Approved 4/30", "Angela Brooks"],
        ["Big River Energy Co.", "Season Ticket Member Bucket Hat", D(2027, 6, 20),
         "Amendment #2 - NOT countersigned (sponsor redline 6/9)", 25000, 5000,
         "Proposed: sponsor redline requests 10,000 hats at all gates for same fee.", "Not submitted",
         "Ryan Castellano"],
        ["Blue Chip Hardware", "Magnet Schedule Night", D(2027, 6, 15), "Moved to 7/13 (letter 5/18)", 18000, 10000,
         "N/A for 6/15 - promotion moved.", "Approved 3/02", "Tom Rinaldi"],
    ]
    add_table(ws, "tblSponsors", headers, rows,
              widths={"Sponsor": 26, "Promotion": 32, "Contract Status": 40, "Make-Good Clause": 70,
                      "Logo Approval": 16, "Contact": 18},
              number_formats={"Game Date": "ddd m/d/yyyy", "Sponsorship Fee": "$#,##0", "Guaranteed Qty": "#,##0"})
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")

    if with_deliveries:
        ws = wb.create_sheet("Deliveries")
        headers = ["Delivery ID", "Delivery Date", "Request Ref", "SKU", "Item", "Destination", "Qty", "UOM",
                   "Damaged Qty", "Received By", "Status", "Notes"]
        add_table(ws, "tblDeliveries", headers, [list(d) for d in DELIVERIES],
                  widths={"Item": 26, "Destination": 22, "Notes": 44, "Request Ref": 14},
                  number_formats={"Delivery Date": "m/d/yyyy", "Qty": "#,##0", "Damaged Qty": "#,##0"}, header_fill=INK_FILL)
        wb["README"]["B3"] = "STARTER WORKBOOK for Inning 4 Part B - allocations plus the warehouse Deliveries table (tblDeliveries)"
        wb.save(OUT1 / "Rally_Reconciliation_start.xlsx")
        return
    wb.save(OUT1 / "Promo_Allocations_Requests.xlsx")


# ---------------------------------------------------------------------------
# Workbook 2: Warehouse Fulfillment & Deliveries (Logistics system export)
# ---------------------------------------------------------------------------
DELIVERIES = [
    # id, date, request ref (as typed), sku (as typed), item, destination, qty, uom, damaged, received by, status, notes
    ("DLV-2201", D(2027, 6, 14), "PR-1039", "MAG-SCHED27", "Magnet Schedule", "Home Plate Gate", 3000, "EA", 0, "T. Okafor", "Delivered", ""),
    ("DLV-2202", D(2027, 6, 14), "PR1039", "MAG-SCHED27", "Magnet Schedule", "Riverside Gate", 2000, "EA", 0, "T. Okafor", "Delivered", ""),
    ("DLV-2203", D(2027, 6, 14), "PR-1039", "MAG-SCHED27", "Magnet Schedule", "Third Base Gate", 2000, "EA", 0, "T. Okafor", "Delivered", ""),
    ("DLV-2204", D(2027, 6, 14), "PR-1039", "MAG-SCHED27", "Magnet Schedule", "Right Field Gate", 1000, "EA", 0, "T. Okafor", "Delivered", "Partial - remainder in warehouse"),
    ("DLV-2210", D(2027, 6, 10), "PR-1041", "TWL-RR27", "Rally Towel", "Home Plate Gate", 3000, "EA", 0, "M. Velasquez", "Delivered", ""),
    ("DLV-2211", D(2027, 6, 10), "PR-1041", "TWL-RR27", "Rally Towel", "Home Plate Gate", 3050, "EA", 0, "M. Velasquez", "Delivered", "Vendor overage"),
    ("DLV-2212", D(2027, 6, 10), "PR-1041", "TWL-RR27", "Rally Towel", "Riverside Gate", 40, "CS", 0, "M. Velasquez", "Delivered", ""),
    ("DLV-2213", D(2027, 6, 10), "PR-1041", "TWL-RR27", "Rally Towel", "Third Base Gate", 4000, "EA", 0, "M. Velasquez", "Delivered", ""),
    ("DLV-2214", D(2027, 6, 11), "pr-1041", "TWL-RR27", "Rally Towel", "Right Field Gate", 2000, "EA", 0, "M. Velasquez", "Delivered", ""),
    ("DLV-2215", D(2027, 6, 11), "PR-1041", "TWL-RR27", "Rally Towel", "Right Field Gate", 2000, "EA", 0, "M. Velasquez", "Delivered", ""),
    ("DLV-2216", D(2027, 6, 11), "PR-1041", "TWL-RR-27", "Rally Towel", "Club Entrance", 2000, "EA", 0, "J. Whitaker", "Delivered", ""),
    ("DLV-2220", D(2027, 6, 11), "PR-1043", "BBH-RETRO27", "Retro Bobblehead", "Home Plate Gate", 2100, "EA", 0, "T. Okafor", "Delivered", ""),
    ("DLV-2221", D(2027, 6, 11), "PR-1043", "BBH-RETRO27", "Retro Bobblehead", "Home Plate Gate", 1200, "EA", 0, "T. Okafor", "Delivered", ""),
    ("DLV-2222", D(2027, 6, 11), "PR-1043", "BBH-RETRO27", "Retro Bobblehead", "Home Plate Gate", 1200, "EA", 0, "T. Okafor", "Delivered", ""),
    ("DLV-2223", D(2027, 6, 11), "PR-1043", "BBH-RETRO-27", "Retro Bobblehead", "Riverside Gate", 3000, "EA", 360, "M. Velasquez", "Delivered", "Pallet crushed in transit - 15 cs damaged"),
    ("DLV-2224", D(2027, 6, 12), "pr-1043", "BBH-RETRO27", "Retro Bobblehead", "Third Base Gate", 3000, "EA", 240, "M. Velasquez", "Delivered", "Water damage - 10 cs"),
    ("DLV-2222", D(2027, 6, 11), "PR1043 ", "BBH-RETRO27", "Retro Bobblehead", "Home Plate Gate", 1200, "EA", 0, "T. Okafor", "Delivered", "Re-scanned at dock"),
    ("DLV-2225", D(2027, 6, 12), "1043", "BBHRETRO27", "Retro Bobblehead", "Right Field Gate", 3000, "EA", 0, "J. Whitaker", "Delivered", ""),
    ("DLV-2226", D(2027, 6, 12), "PR-1043 ", "BBH-RETRO27", "Retro Bobblehead", "Club Entrance", 1500, "EA", 0, "J. Whitaker", "Delivered", ""),
    ("DLV-2230", D(2027, 6, 15), "PR-1048", "BAT-MINI27", "Kids Mini Bat", "Home Plate Gate", 3000, "EA", 0, "T. Okafor", "Delivered", ""),
    ("DLV-2231", D(2027, 6, 15), "PR-1048", "BAT-MINI27", "Kids Mini Bat", "Riverside Gate", 2000, "EA", 0, "T. Okafor", "Delivered", ""),
    ("DLV-2232", D(2027, 6, 15), "PR-1048", "BAT-MINI27", "Kids Mini Bat", "Third Base Gate", 2000, "EA", 0, "M. Velasquez", "Delivered", ""),
    ("DLV-2233", D(2027, 6, 16), "PR-1048", "BAT-MINI27", "Kids Mini Bat", "Right Field Gate", 1000, "EA", 0, "J. Whitaker", "Delivered", ""),
    ("DLV-2234", D(2027, 6, 21), "PR-1048", "BAT-MINI27", "Kids Mini Bat", "Right Field Gate", 1000, "EA", 0, "", "Scheduled", "Second pallet"),
    ("DLV-2235", D(2027, 6, 16), "PR-1048", "BAT-MINI27", "Kids Mini Bat", "Club Entrance", 950, "EA", 0, "J. Whitaker", "Delivered", "Short ship - vendor backorder 50"),
    ("DLV-2240", D(2027, 6, 14), "PR-1060", "KEY-STAR27", "Stars & Stripes Keychain", "Central Warehouse", 6000, "EA", 0, "P. Raman", "Received", "July promo - pre-stage"),
    ("DLV-2241", D(2027, 6, 15), "PR-1060", "KEY-STAR27", "Stars & Stripes Keychain", "Central Warehouse", 6000, "EA", 0, "P. Raman", "Received", "July promo - pre-stage"),
]


def build_warehouse():
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    readme(ws, "Warehouse Fulfillment & Deliveries",
           "Logistics system export - pulled 6/16/2027 7:40 AM by Priya Raman",
           [
               ("Owner", "Warehouse & Logistics (Priya Raman)."),
               ("Deliveries", "One row per pallet delivered (or scheduled) to a gate or warehouse location. "
                              "Request Ref is typed manually by dock staff when the pallet is scanned."),
               ("Inventory On Hand", "Remaining stock in the central warehouse as of this export."),
               ("UOM", "EA = each (single unit). CS = case. See Item Master in the allocations file for case packs."),
               ("Damaged Qty", "Units received damaged and NOT usable for distribution. Included in Qty."),
               ("Known issue", "Dock scanners sometimes create a second row when a pallet is re-scanned."),
               ("Companion file", "Promo_Allocations_Requests.xlsx (Promotions & Marketing)."),
           ])

    ws = wb.create_sheet("Deliveries")
    headers = ["Delivery ID", "Delivery Date", "Request Ref", "SKU", "Item", "Destination", "Qty", "UOM",
               "Damaged Qty", "Received By", "Status", "Notes"]
    rows = [list(d) for d in DELIVERIES]
    add_table(ws, "tblDeliveries", headers, rows,
              widths={"Item": 26, "Destination": 22, "Notes": 44, "Request Ref": 14},
              number_formats={"Delivery Date": "m/d/yyyy", "Qty": "#,##0", "Damaged Qty": "#,##0"},
              header_fill=INK_FILL)

    ws = wb.create_sheet("Inventory On Hand")
    headers = ["SKU", "Item", "On Hand (EA)", "Reserved (EA)", "Open PO #", "PO Qty", "PO ETA", "Notes"]
    rows = [
        ["MAG-SCHED27", "Magnet Schedule", 2000, 0, "", None, None, "Remainder of PR-1039 order"],
        ["TWL-RR27", "Rally Towel", 500, 0, "", None, None, "Vendor overage spares"],
        ["BBH-RETRO27", "Retro Bobblehead", 0, 0, "", None, None, "All units shipped to gates"],
        ["BAT-MINI27", "Kids Mini Bat", 1000, 1000, "PO-77812", 50, D(2027, 6, 24), "1,000 reserved for DLV-2234; 50 on vendor backorder"],
        ["HAT-BKT27", "Sunday Bucket Hat", 0, 0, "", None, None, "No PO on file"],
        ["KEY-STAR27", "Stars & Stripes Keychain", 12000, 12000, "", None, None, "July promo"],
    ]
    add_table(ws, "tblInventory", headers, rows, widths={"Item": 26, "Notes": 50},
              number_formats={"On Hand (EA)": "#,##0", "Reserved (EA)": "#,##0", "PO Qty": "#,##0",
                              "PO ETA": "m/d/yyyy"},
              header_fill=INK_FILL)
    wb.save(OUT1 / "Warehouse_Fulfillment_Deliveries.xlsx")


# ---------------------------------------------------------------------------
# Workbook 3: Promotion & Attendance History (two fictional seasons)
# ---------------------------------------------------------------------------
OPPONENTS = [
    ("Allegheny Ironmen", "Division Rival"), ("Lakeshore Lumberjacks", "Division Rival"),
    ("Prairie Thunder", "Division Rival"), ("Gateway Pioneers", "Division Rival"),
    ("Atlantic Clippers", "Marquee"), ("Golden Coast Comets", "Marquee"),
    ("Bayou Gators", "Standard"), ("Capital Statesmen", "Standard"), ("Gulf Coast Pelicans", "Standard"),
    ("Rocky Ridge Miners", "Standard"), ("Twin Rivers Otters", "Standard"), ("Desert Coyotes", "Standard"),
    ("Northwoods Moose", "Standard"), ("Harborview Herons", "Standard"),
]
CAPACITY = 42000


def season_dates(year, rng):
    """Build ~81 home dates as series of 3-4 games between road trips."""
    dates = []
    d = D(year, 3, 30)
    home = True
    while len(dates) < 81 and d < D(year, 9, 29):
        n = rng.choice([3, 4, 4]) if home else rng.choice([3, 4, 4, 5])
        if home:
            opp = rng.choice(OPPONENTS)
            for _ in range(n):
                if len(dates) < 81:
                    dates.append((d, opp))
                d += dt.timedelta(days=1)
        else:
            d += dt.timedelta(days=n)
        if rng.random() < 0.12:
            d += dt.timedelta(days=1)  # off day
        home = not home
    return dates


def build_history():
    rng = random.Random(2027)
    rows = []
    gid = 1
    promo_catalog = {
        "Bobblehead": ["Retro Pitcher Bobblehead", "Mascot Bobblehead", "Hall of Fame Bobblehead",
                       "Rookie Bobblehead", "Legends Bobblehead"],
        "Fireworks": ["Fireworks Friday"],
        "Apparel Giveaway": ["Replica Jersey", "Rally Cap", "Visor Day", "Hoodie Night", "Bucket Hat"],
        "Novelty Giveaway": ["Magnet Schedule", "Rally Towel", "Kids Mini Bat", "Pennant", "Keychain", "Tote Bag"],
        "Theme Night": ["Pups in the Park", "Faith & Family", "College Night", "Heritage Night", "Star Wars-style Space Night"],
        "Value Night": ["$2 Hot Dog Night", "Family 4-Pack Tuesday", "Student Night"],
    }
    sponsors = ["Harbor City Mutual", "Riverbend Health Partners", "Lakeside Fresh Market", "Blue Chip Hardware",
                "Big River Energy Co.", "Lakeview Credit Union", "Smokehouse Provisions", "Millbrook Motors"]
    effect = {"None": 0, "Bobblehead": 5600, "Fireworks": 6400, "Apparel Giveaway": 3100,
              "Novelty Giveaway": 1300, "Theme Night": 900, "Value Night": 3300}
    unit_cost = {"Bobblehead": 6.2, "Apparel Giveaway": 4.6, "Novelty Giveaway": 1.4}
    for year in (2025, 2026):
        dates = season_dates(year, rng)
        win_pct = 0.47 if year == 2025 else 0.53
        for i, (d, (opp, tier)) in enumerate(dates):
            dow = d.strftime("%a")
            if dow in ("Sat",):
                start = rng.choice(["4:10 PM", "7:15 PM"])
            elif dow == "Sun":
                start = "1:40 PM"
            elif dow in ("Wed", "Thu") and rng.random() < 0.35:
                start = "12:35 PM"
            else:
                start = "6:40 PM" if d.month in (4, 5, 9) else "7:10 PM"
            daynight = "Day" if start.startswith(("12", "1:", "4:")) else "Night"
            # Promotion assignment by day of week
            r = rng.random()
            if dow == "Fri":
                ptype = "Fireworks" if r < 0.7 else ("Apparel Giveaway" if r < 0.85 else "None")
            elif dow == "Sat":
                ptype = "Bobblehead" if r < 0.45 else ("Apparel Giveaway" if r < 0.75 else ("Theme Night" if r < 0.9 else "None"))
            elif dow == "Sun":
                ptype = "Novelty Giveaway" if r < 0.5 else ("Theme Night" if r < 0.7 else "None")
            elif dow == "Tue":
                ptype = "Value Night" if r < 0.6 else "None"
            else:
                ptype = "None" if r < 0.55 else ("Theme Night" if r < 0.75 else ("Novelty Giveaway" if r < 0.9 else "Value Night"))
            pname = "" if ptype == "None" else rng.choice(promo_catalog[ptype])
            sponsor = "" if ptype in ("None", "Value Night") else rng.choice(sponsors)
            gqty = {"Bobblehead": 15000, "Apparel Giveaway": rng.choice([10000, 15000, 20000]),
                    "Novelty Giveaway": rng.choice([10000, 15000, 20000])}.get(ptype, 0)
            gcost = round(gqty * unit_cost.get(ptype, 0) * rng.uniform(0.92, 1.08), 0) if gqty else 0
            if ptype == "Fireworks":
                gcost = round(rng.uniform(58000, 66000), -2)
            # Weather
            month = d.month
            base_temp = {3: 52, 4: 60, 5: 70, 6: 80, 7: 85, 8: 84, 9: 76}[month]
            temp = int(round(base_temp + rng.gauss(0, 6) + (4 if daynight == "Day" else 0)))
            wr = rng.random()
            weather = "Rain Delay" if wr < 0.07 else ("Light Rain" if wr < 0.15 else ("Cloudy" if wr < 0.42 else "Clear"))
            # Attendance model
            base = 23500 + (1200 if year == 2026 else 0)
            dow_eff = {"Mon": -2500, "Tue": -1800, "Wed": -1500, "Thu": -800, "Fri": 5200, "Sat": 7800, "Sun": 3600}[dow]
            day_weekday = -2600 if (daynight == "Day" and dow in ("Mon", "Tue", "Wed", "Thu")) else 0
            tier_eff = {"Division Rival": 2400, "Marquee": 3300, "Standard": 0}[tier]
            month_eff = {3: 9000, 4: -2200, 5: -500, 6: 1800, 7: 2600, 8: 900, 9: -1500}[month]
            if month == 3:  # Opening Day
                pname, ptype = "Opening Day", "Theme Night"
            temp_eff = -2600 if temp < 55 else (-1700 if temp > 92 else 0)
            weather_eff = {"Rain Delay": -3600, "Light Rain": -1900, "Cloudy": -300, "Clear": 400}[weather]
            race = int((win_pct - 0.5) * 30000) + (1500 if (year == 2026 and month >= 8) else 0)
            sold = base + dow_eff + day_weekday + tier_eff + month_eff + temp_eff + int(effect[ptype] * rng.uniform(0.8, 1.2)) \
                + race + int(rng.gauss(0, 1700))
            sold = max(9500, min(CAPACITY, sold))
            noshow = 0.10 + (0.07 if weather == "Rain Delay" else 0.04 if weather == "Light Rain" else 0) \
                + (0.04 if ptype == "Value Night" else 0) - (0.04 if ptype in ("Bobblehead", "Fireworks") else 0) \
                + (0.02 if dow in ("Mon", "Tue", "Wed") else 0) + rng.uniform(-0.02, 0.02)
            scanned = int(sold * (1 - noshow))
            conc_pc = 17.40 + (1.2 if daynight == "Night" else 0) + (1.6 if ptype == "Fireworks" else 0) \
                - (4.8 if ptype == "Value Night" else 0) + (0.9 if temp > 85 else 0) + rng.gauss(0, 0.9)
            merch_pc = 4.10 + (1.9 if ptype == "Bobblehead" else 0) + (0.8 if tier == "Marquee" else 0) \
                + (0.6 if ptype == "Apparel Giveaway" else 0) + rng.gauss(0, 0.5)
            rows.append([f"G{year}-{i + 1:03d}", d, year, dow, start, daynight, opp, tier, ptype, pname,
                         sponsor, gqty, gcost, temp, weather, sold, scanned, None, None, None,
                         round(conc_pc, 2), round(merch_pc, 2)])
            gid += 1

    # Planted data quality issues (documented in instructor key)
    # 1) Typo outlier: an extra digit on tickets sold
    typo_idx = next(i for i, r in enumerate(rows) if r[2] == 2026 and r[8] == "Novelty Giveaway" and r[3] == "Sun")
    true_val = rows[typo_idx][15]
    rows[typo_idx][15] = int(str(true_val)[:2] + "0" + str(true_val)[2:])  # e.g. 31245 -> 310245
    # 2) Duplicate game row
    dup_idx = next(i for i, r in enumerate(rows) if r[2] == 2025 and r[8] == "Bobblehead")
    rows.insert(dup_idx + 1, list(rows[dup_idx]))
    if typo_idx > dup_idx:
        typo_idx += 1
    # 3) Missing scanned attendance (scanner outage)
    miss_idx = next(i for i, r in enumerate(rows) if r[2] == 2026 and r[3] == "Wed" and i > 120)
    rows[miss_idx][16] = None

    final = []
    for r in rows:
        sold, scanned, cpc, mpc = r[15], r[16], r[20], r[21]
        noshow = None if scanned is None else round(1 - scanned / sold, 4)
        conc = None if scanned is None else round(scanned * cpc, 0)
        merch = None if scanned is None else round(scanned * mpc, 0)
        final.append(r[:17] + [noshow, conc, merch] + r[20:])

    headers = ["Game ID", "Date", "Season", "Day", "Start Time", "Day/Night", "Opponent", "Opponent Tier",
               "Promotion Type", "Promotion", "Sponsor", "Giveaway Qty", "Promo Cost", "Temp (F)", "Weather",
               "Tickets Sold", "Scanned Attendance", "No-Show Rate", "Concessions Revenue", "Merch Revenue",
               "Concessions Per Cap", "Merch Per Cap"]
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    readme(ws, "Promotion & Attendance History", "2025-2026 home games (fictional) - Ticketing & Analytics export",
           [
               ("Owner", "Ticketing Analytics (Tasha Greene)."),
               ("Game Log", "One row per home game. Tickets Sold = distributed tickets; Scanned = fans through the gates."),
               ("No-Show Rate", "1 - Scanned / Sold."),
               ("Per Cap", "Revenue divided by scanned attendance."),
               ("Capacity", f"Ballpark capacity used in this dataset: {CAPACITY:,}."),
               ("Data quality", "This is a raw export. It has NOT been cleaned. Validate before you trust a total."),
               ("Use in labs", "Session 1 Lab 4 (trends & outliers) and Session 2 (attendance projections)."),
           ])
    ws = wb.create_sheet("Game Log")
    add_table(ws, "tblGames", headers, final,
              widths={"Opponent": 22, "Opponent Tier": 15, "Promotion Type": 18, "Promotion": 28, "Sponsor": 24},
              number_formats={"Date": "ddd m/d/yyyy", "Giveaway Qty": "#,##0", "Promo Cost": "$#,##0",
                              "Tickets Sold": "#,##0", "Scanned Attendance": "#,##0", "No-Show Rate": "0.0%",
                              "Concessions Revenue": "$#,##0", "Merch Revenue": "$#,##0",
                              "Concessions Per Cap": "$#,##0.00", "Merch Per Cap": "$#,##0.00"})
    wb.save(OUT1 / "Promo_Attendance_History_2025_2026.xlsx")
    return headers, final, typo_idx, dup_idx, miss_idx, true_val


# ---------------------------------------------------------------------------
# Workbook 4 (Session 2): Rally Weekend Budget Model
# ---------------------------------------------------------------------------
BUDGET = {
    "games": [
        # label, date, conservative, expected, optimistic attendance
        ("Fri 6/18 - Rally Towel + Fireworks", D(2027, 6, 18), 33500, 36500, 39500),
        ("Sat 6/19 - Retro Bobblehead Night", D(2027, 6, 19), 36500, 39800, 42000),
        ("Sun 6/20 - Father's Day Family Sunday", D(2027, 6, 20), 30000, 33000, 36000),
    ],
    "margin_per_attendee": 34.00,
    "variable_opex_per_attendee": 7.00,
    "fixed_opex_per_game": 135000,
    "promo_costs": [
        ("Rally Towels (20,000 x $1.15)", 23000),
        ("Retro Bobbleheads (15,000 x $6.40)", 96000),
        ("Kids Mini Bats (10,000 x $2.85)", 28500),
        ("Fireworks show (Skyburst Pyrotechnics)", 65000),
        ("In-park entertainment & marketing", 45000),
    ],
    "sponsorship": [
        ("Harbor City Mutual", 60000),
        ("Riverbend Health Partners", 110000),
        ("Lakeside Fresh Market", 45000),
    ],
    "objective": 2400000,
}


def build_budget():
    b = BUDGET
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    readme(ws, "Riverfront Rally Weekend - Budget Model", "Finance working file (Chris Ahn) - v4, 6/14/2027",
           [
               ("Purpose", "Inputs for the Game-Day Promotion Simulator lab (Session 2, Lab 4)."),
               ("Net contribution", "Attendance x (Margin per attendee - Variable opex per attendee) + Sponsorship "
                                    "- Promotional costs - Fixed operating costs."),
               ("Break-even attendance", "(Promotional costs + Fixed operating costs - Sponsorship) / "
                                         "(Margin per attendee - Variable opex per attendee)."),
               ("Financial objective", f"Weekend net contribution of at least ${b['objective']:,}."),
               ("Not included", "Big River Energy bucket hat ($25,000 fee / $20,500 cost) - pending contract."),
           ])

    ws = wb.create_sheet("Attendance Scenarios")
    headers = ["Game", "Date", "Conservative", "Expected", "Optimistic"]
    rows = [[g[0], g[1], g[2], g[3], g[4]] for g in b["games"]]
    add_table(ws, "tblScenarios", headers, rows, widths={"Game": 40},
              number_formats={"Date": "ddd m/d/yyyy", "Conservative": "#,##0", "Expected": "#,##0", "Optimistic": "#,##0"})
    n = len(rows) + 1
    ws.cell(row=n + 1, column=1, value="Weekend total").font = Font(bold=True)
    for col in "CDE":
        c = ws[f"{col}{n + 1}"]
        c.value = f"=SUM({col}2:{col}{n})"
        c.number_format = "#,##0"
        c.font = Font(bold=True)

    ws = wb.create_sheet("Unit Economics")
    headers = ["Assumption", "Value", "Notes"]
    rows = [
        ["Margin per attendee", b["margin_per_attendee"], "Ticket + concessions + merch net margin (blended)"],
        ["Variable operating cost per attendee", b["variable_opex_per_attendee"], "Cleaning, guest services, utilities"],
        ["Fixed operating cost per game", b["fixed_opex_per_game"], "Security, gate staff, game-day crew"],
        ["Games in weekend", 3, ""],
        ["Financial objective (weekend net)", b["objective"], "Set by leadership 5/3"],
    ]
    add_table(ws, "tblUnitEconomics", headers, rows, widths={"Assumption": 38, "Value": 14, "Notes": 50},
              number_formats={"Value": "$#,##0.00"})
    ws["B5"].number_format = "0"

    ws = wb.create_sheet("Promo Costs")
    headers = ["Line Item", "Cost"]
    add_table(ws, "tblPromoCosts", headers, [list(x) for x in b["promo_costs"]], widths={"Line Item": 44},
              number_formats={"Cost": "$#,##0"})
    n = len(b["promo_costs"]) + 1
    ws.cell(row=n + 1, column=1, value="Total promotional cost").font = Font(bold=True)
    ws[f"B{n + 1}"] = f"=SUM(B2:B{n})"
    ws[f"B{n + 1}"].number_format = "$#,##0"
    ws[f"B{n + 1}"].font = Font(bold=True)

    ws = wb.create_sheet("Sponsorship")
    headers = ["Sponsor", "Contribution", "Status"]
    rows = [[s, v, "Contracted"] for s, v in b["sponsorship"]]
    rows.append(["Big River Energy Co.", 25000, "PENDING - amendment unsigned (excluded from total)"])
    add_table(ws, "tblSponsorship", headers, rows, widths={"Sponsor": 30, "Status": 50},
              number_formats={"Contribution": "$#,##0"})
    ws["A7"] = "Contracted total"
    ws["A7"].font = Font(bold=True)
    ws["B7"] = '=SUMIFS(tblSponsorship[Contribution],tblSponsorship[Status],"Contracted")'
    ws["B7"].number_format = "$#,##0"
    ws["B7"].font = Font(bold=True)
    wb.save(OUT2 / "Rally_Weekend_Budget_Model.xlsx")


def summary_stats(headers, rows, typo_idx, dup_idx, miss_idx, true_val):
    """Compute answer-key insights from the clean data."""
    import statistics as st
    H = {h: i for i, h in enumerate(headers)}
    # clean: drop duplicate, fix typo, exclude missing scanned for scanned stats
    clean = [r for i, r in enumerate(rows) if i != dup_idx + 1]
    stats = {}
    by = {}
    for r in clean:
        sold = r[H["Tickets Sold"]]
        if sold > 100000:
            sold = true_val
        by.setdefault(r[H["Promotion Type"]], []).append(sold)
    stats["avg_sold_by_promo"] = {k: round(st.mean(v)) for k, v in by.items()}
    stats["count_by_promo"] = {k: len(v) for k, v in by.items()}
    # Saturday only comparison
    sat = {}
    for r in clean:
        if r[H["Day"]] == "Sat":
            sold = r[H["Tickets Sold"]]
            sat.setdefault(r[H["Promotion Type"]], []).append(sold)
    stats["sat_avg_by_promo"] = {k: round(st.mean(v)) for k, v in sat.items()}
    fri = {}
    for r in clean:
        if r[H["Day"]] == "Fri":
            fri.setdefault(r[H["Promotion Type"]], []).append(r[H["Tickets Sold"]])
    stats["fri_avg_by_promo"] = {k: round(st.mean(v)) for k, v in fri.items()}
    sun = {}
    for r in clean:
        if r[H["Day"]] == "Sun":
            s = r[H["Tickets Sold"]]
            if s > 100000:
                s = true_val
            sun.setdefault(r[H["Promotion Type"]], []).append(s)
    stats["sun_avg_by_promo"] = {k: round(st.mean(v)) for k, v in sun.items()}
    ns = {}
    for r in clean:
        if r[H["No-Show Rate"]] is not None and r[H["Tickets Sold"]] < 100000:
            ns.setdefault(r[H["Weather"]], []).append(r[H["No-Show Rate"]])
    stats["noshow_by_weather"] = {k: round(st.mean(v), 4) for k, v in ns.items()}
    mpc = {}
    for r in clean:
        mpc.setdefault(r[H["Promotion Type"]], []).append(r[H["Merch Per Cap"]])
    stats["merch_pc_by_promo"] = {k: round(st.mean(v), 2) for k, v in mpc.items()}
    season = {}
    for r in clean:
        s = r[H["Tickets Sold"]]
        if s > 100000:
            s = true_val
        season.setdefault(r[H["Season"]], []).append(s)
    stats["season_avg"] = {k: round(st.mean(v)) for k, v in season.items()}
    stats["season_total"] = {k: sum(v) for k, v in season.items()}
    stats["raw_rows"] = len(rows)
    stats["typo"] = {"game": rows[typo_idx][0], "date": str(rows[typo_idx][1]), "shown": rows[typo_idx][15], "true": true_val}
    stats["dup"] = {"game": rows[dup_idx][0], "date": str(rows[dup_idx][1])}
    stats["missing"] = {"game": rows[miss_idx][0], "date": str(rows[miss_idx][1])}
    raw2026 = sum(r[H["Tickets Sold"]] for r in rows if r[2] == 2026)
    stats["raw_total_2026"] = raw2026
    stats["sellouts"] = sum(1 for r in clean if r[H["Tickets Sold"]] == CAPACITY)
    return stats


if __name__ == "__main__":
    build_allocations()
    build_allocations(with_deliveries=True)
    build_warehouse()
    h, rows, ti, di, mi, tv = build_history()
    build_budget()
    stats = summary_stats(h, rows, ti, di, mi, tv)
    (ROOT / "_build" / "history_stats.json").write_text(json.dumps(stats, indent=2, default=str))
    print(json.dumps(stats, indent=2, default=str))
