---
name: camping-trip-planner
description: Plan camping trips through a staged needs interview, source-verified campsite comparisons, weather and meal planning, and optional mobile HTML or PDF trip guides. Use for choosing and organizing a camping trip, not autonomous booking or payment.
---

# Camping trip planner

Turn the user's constraints into a practical, evidence-backed camping plan. Generalize to their region, group, trip length, equipment, budget, and requested number of campsites or meals; do not silently reuse a previous trip's defaults.

## 1. Establish the brief

Read [references/questionnaire.md](references/questionnaire.md). Use its canonical staged questions, skipping answers already supplied. Ask only the next relevant small batch, not the whole form at once. Resolve blockers (dates, destination/starting area, group, budget unit, driving cap) before ranking bookable options. Keep unanswered optional preferences explicit. Do not infer the trip's calendar dates or time zone from a device UTC offset.

## 2. Research and compare

Read [references/research.md](references/research.md). Research at least the requested number of distinct matching campsites, or clearly explain the evidenced shortfall without inventing candidates. Prefer official operators, government information, and actual booking pages. Cite the source for each decision-relevant claim. Distinguish an advertised rate from a dated quote and a live inventory check from a reservation.

Use tools that are actually available. If browsing, live inventory, mapping, rendering, hosting, or persistent storage is unavailable, explain the affected limitation and offer an honest lower-capability output. Never fabricate a tool run, live availability, synchronized favorite, image, or exact journey time. Do not depend on undocumented booking-provider endpoints.

## 3. Build the trip plan

Present the best fits and trade-offs, then the user's selected itinerary if a choice is made. Show per-night and whole-stay costs, inclusions/exclusions, date-specific availability, journey estimates and source/check timestamps. Keep unknowns visible. Tie safety and cancellation contingencies to current official forecasts and campsite terms rather than promising safe conditions.

Plan meals only when requested. Respect allergies, dietary restrictions, cooking equipment, refrigeration/cold chain, group portions, and travel-day timing. Generate exactly the agreed count in each meal category; 90 meals is an optional requested configuration, never a default. Separate a menu-idea bank from meals actually scheduled. Include a shopping/prep list only at the requested scope.

## 4. Deliver and verify

For HTML, PDF, photos, layouts, or favorites read [references/delivery.md](references/delivery.md). A concise chat comparison is sufficient if no artifact is wanted. Before delivering, check counts, date/night arithmetic, cost units, conditional discounts, source links, freshness and uncertain fields. The optional [references/plan.schema.json](references/plan.schema.json) and synthetic [references/example-plan.json](references/example-plan.json) provide a portable structured core; run `python scripts/validate_plan.py PLAN.json` and `python scripts/test_validate_plan.py` when using it. Structural validation is not source verification.

## Authority boundaries

Research and draft within the request. Do not book, pay, contact operators, submit personal details, or publish/share more broadly without the user's direction and required confirmation. Obtain explicit permission before making a guide or favorites service public; a request for an HTML/PDF file is not permission to publish it. Keep personal trip details and source photos out of public source repositories. Never label a role/name selector as authentication.
