"""Single source of truth for the fictional Riverfront Rally Weekend story.
Used by gen_docs.py (Word files) and build_site.py (Case File page)."""

CAST = [
    ("Dana Whitfield", "Director, Promotions & Marketing", "Owns the promo plan and the lock date.", "DW"),
    ("Jordan Pierce", "Sponsorship Account Manager", "Champion of the Big River Energy add-on.", "JP"),
    ("Elena Ortiz", "VP, Marketing", "Final marketing approver.", "EO"),
    ("Marcus Bell", "Manager, Ballpark Operations", "Gate capacity and staffing sign-off.", "MB"),
    ("Priya Raman", "Warehouse & Logistics Coordinator", "Owns deliveries and inventory.", "PR"),
    ("Sam Kowalski", "Fan Experience Lead", "Owns the fan email going to 180,000 fans.", "SK"),
    ("Tasha Greene", "Ticketing Analyst", "Tracks sales pacing and attendance history.", "TG"),
    ("Chris Ahn", "Finance Business Partner", "Owns the weekend P&L forecast.", "CA"),
    ("Ryan Castellano", "Partnerships, Big River Energy Co. (sponsor)", "External sponsor contact.", "RC"),
]

DOMAIN = "rallyclub.example"


def addr(name):
    if name == "Ryan Castellano":
        return "ryan.castellano@bigriverenergy.example"
    if name == "Promo Task Force":
        return f"rally-taskforce@{DOMAIN}"
    first, last = name.lower().split(" ", 1)
    return f"{first}.{last.replace(' ', '')}@{DOMAIN}"


# Each email: id, date-time, from, to, cc, subject, body(list of paragraphs), tags (instructor-only)
EMAILS = [
    ("E01", "Mon May 10, 2027 9:02 AM", "Dana Whitfield", ["Promo Task Force"], [],
     "Riverfront Rally Weekend - kickoff & lock date",
     ["Team -",
      "Riverfront Rally Weekend (Fri 6/18 - Sun 6/20 vs. the Allegheny Ironmen) is officially on. Current lineup:",
      "- Friday: Riverfront Rally Towel (first 20,000 fans) + postgame fireworks, presented by Harbor City Mutual",
      "- Saturday: Retro Bobblehead (first 15,000 fans), presented by Riverbend Health Partners",
      "- Sunday (Father's Day): Kids Mini Bat (first 10,000 kids 14 & under), presented by Lakeside Fresh Market",
      "Promo lock date is Friday, June 4. After that, no new items.",
      "Reminder of our approval rule - any NEW or CHANGED giveaway needs all three: (1) a signed sponsor "
      "contract or amendment, (2) Elena's approval, and (3) Marcus's Ops capacity sign-off.",
      "Separately, Blue Chip Hardware's Magnet Schedule Night on Tue 6/15 is still on for now.",
      "- Dana"],
     ["Establishes the 3-part approval rule and the June 4 lock date."]),
    ("E02", "Tue May 18, 2027 10:15 AM", "Dana Whitfield", ["Priya Raman"], ["Marcus Bell"],
     "Magnet Schedule 6/15 - CANCELLED, moved to 7/13",
     ["Priya - Blue Chip Hardware has moved Magnet Schedule Night to July 13. Please cancel the 6/15 gate "
      "deliveries for PR-1039 and hold the stock in the warehouse.",
      "I've updated the Requests sheet to Cancelled.",
      "Thanks, Dana"],
     ["No reply from Priya. Magnets get delivered anyway on 6/14 (see E13)."]),
    ("E03", "Fri May 21, 2027 3:47 PM", "Jordan Pierce", ["Dana Whitfield"], ["Elena Ortiz"],
     "New opportunity: Big River Energy bucket hats for Sunday",
     ["Big River Energy wants in on Rally Weekend!",
      "Proposal: 5,000 bucket hats for Season Ticket Members on Sunday 6/20, handed out at the Home Plate Gate "
      "and Club Entrance, for a $25,000 sponsorship fee. Hats are $4.10/unit from Seventh Inning Headwear "
      "(about a 3-week lead time).",
      "Can we make this happen? They'd love an answer this week.",
      "Jordan"],
     ["Origin of the disputed giveaway."]),
    ("E04", "Mon May 24, 2027 8:31 AM", "Elena Ortiz", ["Jordan Pierce"], ["Dana Whitfield"],
     "RE: New opportunity: Big River Energy bucket hats for Sunday",
     ["Love this - a great partner to grow with.",
      "Looks good to me pending Marcus confirming Sunday gate capacity and the amendment coming back signed.",
      "Dana, please make sure this goes through the normal process before lock.",
      "Elena"],
     ["KEY EVIDENCE: Elena's approval is CONDITIONAL - not a final approval."]),
    ("E05", "Thu May 27, 2027 11:12 AM", "Jordan Pierce", ["Ryan Castellano"], ["Dana Whitfield"],
     "Bucket Hat Sunday - approved!",
     ["Ryan - great news: the bucket hat giveaway for Sunday 6/20 is approved on our side!",
      "Attached is Amendment #2 for your signature. We'll get the hats ordered as soon as it's back.",
      "Best, Jordan"],
     ["Overclaim: tells the sponsor it's approved. Conditions not met."]),
    ("E06", "Thu May 27, 2027 11:20 AM", "Jordan Pierce", ["Priya Raman"], [],
     "Please add PR-1057 - bucket hats Sunday",
     ["Priya - please add PR-1057: 5,000 Sunday Bucket Hats (HAT-BKT27), split Home Plate 2,500 / Club 2,500.",
      "Approved by Elena. I've already entered it in the allocations sheet as Approved.",
      "Thanks! Jordan"],
     ["Explains why the Requests sheet shows PR-1057 as Approved, 'approved by' J. Pierce."]),
    ("E07", "Thu May 27, 2027 2:05 PM", "Priya Raman", ["Jordan Pierce"], [],
     "RE: Please add PR-1057 - bucket hats Sunday",
     ["Happy to, but I need a PO before I can order anything.",
      "Seventh Inning Headwear is 21 days from PO, so we'd need the PO by May 28 to have hats here by 6/18. "
      "Who's issuing the PO?",
      "Priya"],
     ["No reply in thread. No PO was ever issued (see Inventory On Hand sheet)."]),
    ("E08", "Wed Jun 2, 2027 4:40 PM", "Marcus Bell", ["Jordan Pierce", "Dana Whitfield"], [],
     "Sunday gate capacity - bucket hats",
     ["I have NOT signed off on the bucket hats.",
      "Sunday we're already handing out mini bats at every gate. A second item at Home Plate and Club means six "
      "more gate staff and a separate Season Ticket Member scan lane. The staffing agency can't confirm until June 15.",
      "Please don't treat this as approved yet.",
      "Marcus"],
     ["Ops sign-off explicitly missing."]),
    ("E09", "Fri Jun 4, 2027 9:15 AM", "Dana Whitfield", ["Promo Task Force"], [],
     "LOCKED: Rally Weekend final promo list (Event Plan v3)",
     ["The promo list is locked: Friday towel + fireworks, Saturday bobblehead, Sunday mini bat. Event Plan v3 attached.",
      "Bucket hats are NOT in v3. Jordan - where are we on the amendment and Marcus's sign-off?",
      "Dana"],
     ["Lock date passes with bucket hats unresolved."]),
    ("E10", "Fri Jun 4, 2027 9:52 AM", "Jordan Pierce", ["Promo Task Force"], [],
     "RE: LOCKED: Rally Weekend final promo list (Event Plan v3)",
     ["Bucket hats are approved - Elena signed off on 5/24. The amendment is with BRE legal and should be back any day.",
      "Can we add it to v3?",
      "Jordan"],
     ["Restates conditional approval as final. Classic 'confident but wrong' claim."]),
    ("E11", "Wed Jun 9, 2027 1:18 PM", "Ryan Castellano", ["Jordan Pierce"], [],
     "RE: Bucket Hat Sunday - amendment redline",
     ["Jordan - our legal team returned the amendment with one change: we'd like hats at all five gates "
      "(10,000 hats) for the same $25,000.",
      "Let me know if that works and we'll sign right away.",
      "Ryan Castellano | Partnerships | Big River Energy Co."],
     ["Scope change! Doubles quantity, same fee. Not forwarded to Dana. Amendment still unsigned."]),
    ("E12", "Fri Jun 11, 2027 4:02 PM", "Priya Raman", ["Marcus Bell"], ["Dana Whitfield"],
     "Bobblehead delivery update",
     ["All Retro Bobblehead pallets are at the gates.",
      "Heads up: the Riverside pallet was crushed in transit (15 cases) and Third Base had water damage (10 cases). "
      "I logged the damaged units in the Deliveries file. The warehouse is now at zero bobbleheads.",
      "Priya"],
     ["Subtle: 25 cases x 24 = 600 unusable units. Nobody does the math. Sponsor guarantees 15,000."]),
    ("E13", "Mon Jun 14, 2027 7:55 AM", "Priya Raman", ["Marcus Bell"], [],
     "Magnet schedules delivered to gates",
     ["8,000 magnet schedules were delivered to Home Plate, Riverside, Third Base and Right Field this morning per the "
      "delivery schedule.",
      "Dock bays are tight - towels and bobbleheads are also staged.",
      "Priya"],
     ["Delivered against a CANCELLED request (PR-1039)."]),
    ("E14", "Mon Jun 14, 2027 8:30 AM", "Dana Whitfield", ["Priya Raman", "Marcus Bell"], [],
     "RE: Magnet schedules delivered to gates",
     ["Wait - the magnets were moved to July 13! I sent a cancellation on 5/18. Why are they at the gates?",
      "We need those bays for the weekend.",
      "Dana"],
     ["Confirms the cancellation was never actioned."]),
    ("E15", "Tue Jun 15, 2027 10:20 AM", "Sam Kowalski", ["Dana Whitfield", "Jordan Pierce"], [],
     "Fan email - 'Bucket Hat Sunday' go/no-go",
     ["Our Rally Weekend fan email (180,000 recipients) is scheduled for Thursday 6/17 at 10:00 AM.",
      "The draft from Sponsorship includes 'Bucket Hat Sunday for Season Ticket Members.' I need a go/no-go "
      "by Wednesday 5:00 PM or I'll pull the line.",
      "Sam"],
     ["Business deadline that forces a decision: Wed 6/16 5:00 PM."]),
    ("E16", "Tue Jun 15, 2027 3:05 PM", "Chris Ahn", ["Dana Whitfield"], [],
     "Rally Weekend P&L - BRE $25K?",
     ["The Rally Weekend forecast from Sponsorship shows $25K from Big River Energy as booked revenue. I don't see a "
      "signed amendment in the contract system. Should I keep it in or move it to pending?",
      "Also - any change to the bobblehead quantity? Riverbend's make-good clause is $8 per unit short.",
      "Chris"],
     ["Finance risk: revenue booked without a contract. Hints at the bobblehead shortfall."]),
]

TRANSCRIPT_META = {
    "title": "Rally Weekend Ops Readiness Huddle",
    "when": "Tuesday, June 15, 2027 | 2:00 PM - 2:30 PM",
    "organizer": "Marcus Bell",
    "attendees": ["Marcus Bell", "Dana Whitfield", "Jordan Pierce", "Priya Raman", "Sam Kowalski", "Tasha Greene"],
    "absent": ["Elena Ortiz (declined)", "Chris Ahn (not invited)"],
}

TRANSCRIPT = [
    ("00:00:12", "Marcus Bell", "Okay, let's get going. The goal is a go or no-go on every Rally Weekend item. Friday first."),
    ("00:00:31", "Priya Raman", "Towels are at all five gates. Riverside might look short in the system - I think they scanned that pallet by the case."),
    ("00:00:58", "Marcus Bell", "Fireworks?"),
    ("00:01:05", "Dana Whitfield", "Skyburst confirmed. The permit is filed. Friday's good."),
    ("00:01:22", "Marcus Bell", "Saturday, bobbleheads."),
    ("00:01:30", "Priya Raman", "All pallets delivered. We had some damage on two pallets - I logged it. Honestly the system shows more than fifteen thousand delivered, so we should be covered."),
    ("00:01:52", "Dana Whitfield", "Great. Riverbend is our biggest sponsor this weekend, so let's not have any surprises."),
    ("00:02:10", "Marcus Bell", "Sunday. Mini bats are mostly out; Right Field has one more pallet coming."),
    ("00:02:25", "Priya Raman", "Yeah, the second Right Field pallet is on the schedule. I'd have to check the date."),
    ("00:02:40", "Marcus Bell", "Then the bucket hats."),
    ("00:02:44", "Jordan Pierce", "Those are approved. Elena signed off back in May, and Big River Energy is super excited."),
    ("00:02:58", "Marcus Bell", "I haven't signed off. I'm still waiting on the staffing agency for six extra gate staff. They said by tomorrow noon."),
    ("00:03:15", "Dana Whitfield", "And Elena's note said pending Ops and a signed amendment. Jordan, is the amendment signed?"),
    ("00:03:24", "Jordan Pierce", "It's basically done. Their legal had one small tweak."),
    ("00:03:31", "Priya Raman", "For the record, I don't have a PO for hats. Even if we order today, they won't be here by Sunday."),
    ("00:03:45", "Jordan Pierce", "Could we rush them?"),
    ("00:03:49", "Priya Raman", "I can ask Seventh Inning about expedited shipping, but no promises."),
    ("00:04:05", "Sam Kowalski", "The fan email goes out Thursday and it mentions Bucket Hat Sunday. I need an answer."),
    ("00:04:16", "Tasha Greene", "Also, Sunday sales are tracking about thirty-one thousand two hundred versus the thirty-three thousand in the plan. Saturday is pacing ahead."),
    ("00:04:33", "Marcus Bell", "Okay. So bucket hats - we treat them as pending. Actions: Jordan gets the signed amendment and clarifies the scope. I confirm staffing by tomorrow noon. Priya checks on expedited hats and sends a reconciliation of everything at the gates. Sam holds the bucket hat line in the email until we confirm."),
    ("00:04:58", "Jordan Pierce", "Sounds good. I'll tell Ryan we're close."),
    ("00:05:06", "Marcus Bell", "Thanks, everyone."),
]

# Deliberately flawed auto-recap. (claim, is_correct, correction)
RECAP = [
    ("Friday: Rally Towels delivered to all gates; fireworks confirmed. Ready.", True, "Supported by transcript 00:00:31-00:01:05."),
    ("Saturday: Bobbleheads delivered - more than 15,000 on hand. Ready.", False,
     "Transcript says 'some damage' and 'the system shows more than fifteen thousand.' The system total includes a duplicate row and 600 damaged units: usable = 14,400."),
    ("Sunday: Mini bats delivered; one Right Field pallet remaining.", True, "Supported - but the pallet date was never checked (it's 6/21, after the game)."),
    ("Bucket hat giveaway approved by Elena (Jordan Pierce).", False,
     "Marcus explicitly said 'we treat them as pending' at 00:04:33. Elena's 5/24 approval was conditional."),
    ("Action - Jordan: finalize the BRE amendment.", True, "Also: 'clarify the scope' - the sponsor redline changed 5,000 to 10,000 hats."),
    ("Action - Marcus: confirm staffing by Wed 6/16 noon.", True, "Supported at 00:04:33."),
    ("Action - Priya: expedite hats and send gate reconciliation.", True, "Supported - though 'check on' expediting is not the same as 'expedite.'"),
    ("Action - Sam: send the fan email Thursday as planned.", False,
     "Marcus said Sam HOLDS the bucket hat line until confirmed. The recap reverses the decision."),
]

EVENT_PLAN = {
    "title": "Riverfront Rally Weekend - Event Plan v3",
    "subtitle": "LOCKED June 4, 2027 | Owner: Dana Whitfield, Promotions & Marketing",
    "games": [
        ("Fri 6/18", "7:10 PM", "5:40 PM", "Riverfront Rally Towel (first 20,000 fans) + postgame fireworks", "Harbor City Mutual"),
        ("Sat 6/19", "4:10 PM", "2:40 PM", "Retro Bobblehead (first 15,000 fans)", "Riverbend Health Partners"),
        ("Sun 6/20", "1:40 PM", "12:10 PM", "Kids Mini Bat (first 10,000 kids 14 & under) - distributed at gate entry", "Lakeside Fresh Market"),
    ],
    "distribution": [
        ("Home Plate Gate", "6,000", "4,500", "3,000"),
        ("Riverside Gate", "4,000", "3,000", "2,000"),
        ("Third Base Gate", "4,000", "3,000", "2,000"),
        ("Right Field Gate", "4,000", "3,000", "2,000"),
        ("Club Entrance", "2,000", "1,500", "1,000"),
        ("TOTAL", "20,000", "15,000", "10,000"),
    ],
    "key_dates": [
        ("Fri Jun 4", "Promo lock date - no new items after this date"),
        ("Wed Jun 16, 12:00 PM", "Final gate reconciliation due (Warehouse)"),
        ("Wed Jun 16, 5:00 PM", "Fan email content final (Fan Experience)"),
        ("Thu Jun 17, 10:00 AM", "Rally Weekend fan email sends to 180,000 fans"),
        ("48 hrs before gates", "All giveaway pallets at gates (Ops standard)"),
    ],
    "staffing": "Giveaway staff: 1 per 1,250 items per gate (minimum 2 per gate). Total giveaway staff: Fri 16, Sat 12, Sun 10.",
    "revisions": [
        ("v1", "May 10", "Initial plan: towel, fireworks, bobblehead, mini bat."),
        ("v2", "May 25", "Added 'Sunday Bucket Hat - Big River Energy (TBD, pending approvals)'."),
        ("v3", "Jun 4", "LOCKED. Bucket hat removed - approvals incomplete at lock. To be re-added only if all three approvals are met."),
    ],
}

SPONSORS = [
    ("Harbor City Mutual", "Rally Towel + Fireworks Friday (Fri 6/18)", "Signed 3/30/2027", "$60,000", "20,000 towels",
     "$3 credit per towel short of 20,000", ["Logo on towel (approved 4/22)", "2 PA reads", "Fireworks 'presented by' video board slate"]),
    ("Riverbend Health Partners", "Retro Bobblehead Night (Sat 6/19)", "Signed 2/26/2027", "$110,000", "15,000 bobbleheads distributed",
     "$8 credit per bobblehead short of 15,000 OR a replacement promotion night (sponsor's choice)",
     ["Logo on box (approved 3/18)", "Pregame first-pitch for sponsor guest", "Concourse table at Home Plate Gate"]),
    ("Lakeside Fresh Market", "Father's Day Family Sunday (Sun 6/20)", "Signed 4/8/2027", "$45,000", "10,000 mini bats to kids 14 & under",
     "$2 credit per bat short of 10,000", ["Logo on bat sleeve (approved 4/30)", "Kids Run the Bases presented-by", "1 PA read"]),
    ("Big River Energy Co.", "Season Ticket Member Bucket Hat (Sun 6/20) - PROPOSED", "Amendment #2 NOT countersigned. Sponsor redline 6/9 asks for 10,000 hats at all gates.",
     "$25,000 (proposed)", "5,000 hats (our draft) vs 10,000 (sponsor redline)", "Not agreed",
     ["Logo artwork not yet submitted", "Requires 21-day production lead time"]),
    ("Blue Chip Hardware", "Magnet Schedule Night - MOVED from 6/15 to 7/13", "Change letter signed 5/18", "$18,000", "10,000 magnets on 7/13",
     "N/A for June", ["Stock should be held in warehouse until 7/13"]),
]

OPS_RULES = [
    ("Approvals", "A new or changed giveaway requires ALL THREE: signed sponsor contract/amendment, written VP Marketing approval, and Ballpark Operations capacity sign-off. Conditional approvals ('pending X') are not approvals until X is met."),
    ("Lock date", "No giveaway may be added after the promo lock date (June 4 for Rally Weekend) without a written exception from the VP Marketing and the Ops Manager."),
    ("Delivery cutoff", "All giveaway pallets must be at their gates at least 48 hours before gates open. Late deliveries are an exception."),
    ("Units of measure", "Deliveries must be recorded in EA (each). If a pallet is scanned in CS (cases), convert using the Item Master case pack before reconciling."),
    ("Damaged goods", "Damaged units are NOT distributable. Distributable Qty = Qty - Damaged Qty."),
    ("Reconciliation tolerance", "Per gate, distributable quantity within +/-1% of allocation = MATCH. Outside 1% = EXCEPTION requiring an owner and a fix."),
    ("Duplicates", "Dock scanners can create a second row when a pallet is re-scanned. A repeated Delivery ID is a duplicate, even if other fields differ slightly."),
    ("Vendor services", "Fireworks and entertainment are vendor services - no warehouse delivery is expected."),
    ("Staffing", "1 giveaway staffer per 1,250 items per gate, minimum 2 per gate. A gate distributing two items needs +3 staff."),
    ("Dock capacity", "Each gate has 4 pallet bays. Items for cancelled or future promotions must stay in the Central Warehouse."),
    ("Case packs", "MAG-SCHED27 = 250/cs | TWL-RR27 = 100/cs | BBH-RETRO27 = 24/cs | BAT-MINI27 = 50/cs | HAT-BKT27 = 40/cs"),
]

# ----------------------------------------------------------------------------------
# Session 2 materials
# ----------------------------------------------------------------------------------
PLOT_TWIST = {
    "title": "PLOT TWIST - Four changes overnight",
    "from": "Elena Ortiz, VP Marketing",
    "to": "Rally Weekend Task Force",
    "when": "Thursday, June 17, 2027 | 7:45 AM",
    "intro": "Thank you for yesterday's readiness assessment - it was exactly what we needed. Unfortunately the situation has moved overnight. I need a revised recommendation by 3:00 PM today.",
    "changes": [
        ("1. Sunday weather", "The forecast now shows a 60% chance of thunderstorms Sunday afternoon. Ticketing has revised Sunday's expected attendance from 33,000 to 28,500 (conservative 25,000 / optimistic 31,000). Saturday continues to pace ahead of plan (expected 41,000)."),
        ("2. Big River Energy signed - on THEIR terms", "Ryan Castellano signed Amendment #2 last night, but only the redlined version: 10,000 bucket hats at ALL five gates for the same $25,000. Seventh Inning Headwear can rush 10,000 hats by Saturday night at $5.35 per hat ($53,500). Sunday would need 9 extra gate staff ($2,400)."),
        ("3. Bobblehead replacements", "Nod & Wobble can air-freight 600 replacement Retro Bobbleheads at $9.50 each plus $2,400 freight ($8,100 total), arriving Friday 6/18. Riverbend's make-good is $8 per bobblehead short ($4,800) - or a replacement promotion night, at the sponsor's choice."),
        ("4. Fireworks surcharge", "Skyburst Pyrotechnics has added a $6,500 fuel and permit surcharge."),
    ],
    "ask": [
        "Does the weekend still meet the $2.4M net contribution objective?",
        "Should we accept the Big River Energy deal as signed, counter-offer, or decline?",
        "Should we air-freight replacement bobbleheads or offer the make-good?",
        "What must change in the fan email that is scheduled for 10:00 AM today?",
    ],
}

CHECKLIST = [
    ("A. Contracts & approvals", [
        "Sponsor contract or amendment is fully signed by BOTH parties, and its scope matches our plan.",
        "VP Marketing approval is written and unconditional (or every stated condition has been met).",
        "Ballpark Operations has signed off on gate capacity and staffing.",
        "The item was in the plan before the promo lock date, or a written exception exists.",
    ]),
    ("B. Inventory & fulfillment", [
        "Distributable quantity (Qty - Damaged, in EA) at each gate is within +/-1% of allocation.",
        "All pallets are at the gates at least 48 hours before gates open.",
        "No deliveries exist for cancelled or out-of-scope requests.",
        "No duplicate delivery records remain in the reconciliation.",
    ]),
    ("C. Staffing & distribution", [
        "Giveaway staff meet the standard (1 per 1,250 items per gate, minimum 2; +3 for dual-item gates).",
        "Distribution method follows Event Standards (e.g., bat-style items at exit).",
        "An accessible distribution lane exists at every gate.",
    ]),
    ("D. Fan communications", [
        "No fan-facing message mentions an item that has not met section A.",
        "Eligibility rules (first N fans, age limits, STM-only) are stated clearly.",
    ]),
    ("E. Finance", [
        "Sponsorship revenue is counted only when the contract is signed.",
        "Make-good exposure is calculated for any shortfall against guaranteed quantities.",
        "Weekend forecast still meets the financial objective, or a gap-closing plan exists.",
    ]),
    ("F. Ratings", [
        "GREEN = all checks met with evidence. YELLOW = one or more checks unverified but a credible owner and date exist. RED = a check has failed or cannot be met before gates open.",
    ]),
]

STANDARDS = [
    ("Giveaway eligibility", "Giveaways go to the first N ticketed fans scanned at the gate - one per scanned ticket. Age-restricted items (e.g., kids 14 & under) require visual confirmation by gate staff."),
    ("Bat-style items", "For fan safety, bat-style giveaways of any size are distributed upon EXIT after the final out, never at gate entry."),
    ("Accessibility", "Every gate must have an accessible distribution lane, and guest services may hold items for fans using mobility services."),
    ("Rain policy", "If a game is postponed before gates open, giveaways move to the makeup date. If gates have opened, distributed items are not replaced."),
    ("Season Ticket Member exclusives", "STM-only items require a separate scan lane and a STM-only signage kit at each participating gate."),
    ("Announcements", "No promotion may be announced to fans until it passes the Promotional Readiness Checklist section A."),
    ("Sponsor make-goods", "Any shortfall against a guaranteed quantity must be reported to the sponsor within 24 hours of the event, with the make-good option."),
]

FINDINGS_S1 = [
    ("Bucket hats (PR-1057)", "RED", "Not approved. Elena's 5/24 approval was conditional; Ops never signed off; amendment unsigned at lock (sponsor redline changed scope to 10,000). No PO, zero inventory. Requests sheet shows 'Approved' entered by Sponsorship."),
    ("Retro Bobbleheads (PR-1043)", "RED", "System total 16,200 includes a duplicate row (DLV-2222, 1,200). True delivered 15,000, of which 600 damaged: 14,400 distributable vs 15,000 guaranteed. Make-good exposure $4,800. Warehouse stock: 0."),
    ("Kids Mini Bats (PR-1048)", "YELLOW", "Right Field second pallet (1,000) scheduled 6/21 - after the 6/20 game. 1,000 units sit in the warehouse, so this is fixable by rescheduling. Club Entrance short 50 (vendor backorder)."),
    ("Magnet Schedules (PR-1039)", "YELLOW", "8,000 magnets delivered to gates against a cancelled request. Occupying dock bays needed for weekend pallets. Must be returned to the Central Warehouse for 7/13."),
    ("Rally Towels (PR-1041)", "GREEN", "All gates within tolerance once Riverside's 40 CS is converted to 4,000 EA. Home Plate +50 (0.8%) is within tolerance. ID variants (pr-1041, TWL-RR-27) are reliable matches after normalizing."),
    ("Fireworks (PR-1052)", "GREEN", "Vendor service - no warehouse delivery expected. Not an exception."),
    ("Meeting recap", "WARNING", "The auto-generated recap of the 6/15 huddle contains three errors: bobbleheads 'more than 15,000', bucket hats 'approved', and the fan email 'send as planned'."),
    ("Finance", "YELLOW", "$25,000 BRE revenue is booked in the forecast without a signed contract."),
]
