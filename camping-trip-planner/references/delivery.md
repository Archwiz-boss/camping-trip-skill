# Artifact, imagery and favorites delivery

## Mobile HTML

Use the user's requested language, currency and units. Provide a responsive layout with a compact comparison and readable campsite cards. Include date/day/night labels, per-night versus whole-stay costs and assumptions, dated weather icons plus text/units, actual photos/layouts when sourced, facility unknowns, availability confidence, source/check timestamps, and direct booking links. Separate trip-day forecast from general campsite descriptions. Clearly label an offline static file and any feature that needs a network connection.

Check a narrow mobile viewport and a desktop viewport, keyboard navigation, meaningful image alt text, link targets and long names/prices. Ensure readable contrast and no horizontal overflow. Escape untrusted source text in generated HTML. Avoid embedding secrets, account identifiers, unnecessary location detail or private URLs in artifacts/public repositories.

## Photos and layouts

Use genuine sourced photos, not generated depictions passed off as the campsite. Confirm provenance and permission for the intended reuse; attribution alone does not confer reuse rights. Prefer permissible official media, user-authorized images, or links to source galleries if copying rights are unclear. Respect limitations on hotlinking. Label image location/caption and source, and distinguish a nearby landscape from the actual site. Do not fetch private source photos into a public source package.

Use an official layout/map when available and permissible. Mark unpublished labels, missing facilities, absent scale, unclear legends and old versions explicitly. Do not invent bathroom locations, paths or exact distances from an unlabeled/unscaled drawing. An illustrative sketch must say “illustrative, not to scale, not an official site map”; it cannot be used as verified access evidence. If photos/layouts cannot be retrieved, retain labeled unavailable placeholders or source-gallery links rather than fabricated images.

## Favorites and publication

Choose the smallest architecture matching the user's agreed sharing needs:
- Single-device private favorites: local storage is acceptable if clearly labeled device/browser-local and potentially cleared.
- Cross-device/shared favorites: use an available persistent server-side data store, explicit stable participant identities, shared trip/item IDs, read/write access rules and synchronization semantics. Validate two independent sessions, refresh persistence, and visibility rules. A selector for “Person 1/2” is not authentication or authorization.
- If no backend is available, do not ship local storage as “shared.” Offer a clearly labeled local prototype or an export/import workflow and explain that neither is live synchronization.

Public deployment requires explicit permission even if the guide was requested as HTML. Confirm destination, intended audience and personal data disclosure before deploying. Keep private sharing private; do not solve a private-sharing failure by publishing publicly. Do not collect unrelated personal information. Do not contact participants or send invitations without direction.

## PDF and final checks

If requested, generate PDF using an available renderer, then render every page to images and inspect readability, clipping, page breaks, photo quality, comparison tables and totals. Check that links remain clickable and lead to intended sources/bookings; never claim link testing without doing it. If no rendering/inspection capability exists, disclose unverified layout and offer the source file rather than claiming QA passed. A PDF has static favorites and stale-at-export inventory/weather, not live app behavior.

Before handoff run arithmetic/date/count checks, inspect all requested artifact types, and show “information checked” and “exported” timestamps with timezones. Note which availability/weather/prices must be rechecked before travel/payment. Distinguish a completed guide from an incomplete draft when required data or capabilities are missing. Never imply that producing a guide books a campsite.
