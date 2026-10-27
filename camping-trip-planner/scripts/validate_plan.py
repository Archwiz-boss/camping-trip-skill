#!/usr/bin/env python3
"""Validate the portable plan core. No network requests; not source verification."""
import argparse
import json
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class PlanError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise PlanError(message)


def money(value):
    require(isinstance(value, (int, float)) and not isinstance(value, bool), 'money must be a JSON number')
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise PlanError('invalid money') from exc
    require(result.is_finite() and result >= 0, 'money must be finite and nonnegative')
    return result


def stamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(result.utcoffset() is not None, 'timestamp must include timezone')
    return result


def url(value):
    from urllib.parse import urlsplit
    parsed = urlsplit(value)
    require(parsed.scheme in ('https', 'http') and bool(parsed.hostname), 'source must be an HTTP(S) URL')


def count(value):
    require(type(value) is int and value >= 0, 'count must be a nonnegative integer')
    return value


def validate(plan):
    require(isinstance(plan, dict), 'plan must be an object')
    require(plan['schema_version'] == '1.0', 'unsupported schema_version')
    require(type(plan['synthetic']) is bool, 'synthetic must be boolean')
    trip = plan['trip']
    require(isinstance(trip['destination'], str) and trip['destination'].strip(), 'destination is required')
    ZoneInfo(trip['timezone'])
    arrival, departure = date.fromisoformat(trip['arrival']), date.fromisoformat(trip['departure'])
    nights = (departure - arrival).days
    require(nights > 0 and count(trip['nights']) == nights, 'date/night mismatch')
    require(len(trip['currency']) == 3 and trip['currency'].isupper() and trip['currency'].isalpha(), 'currency needs three uppercase letters')
    requested = count(plan['requested_campsites'])
    require(requested > 0, 'request at least one campsite')
    sites = plan['campsites']
    require(isinstance(sites, list), 'campsites must be an array')
    require(len({s['id'] for s in sites}) == len(sites), 'duplicate campsite ID')
    if len(sites) < requested:
        require(isinstance(plan.get('shortfall_reason'), str) and plan['shortfall_reason'].strip(), 'shortfall must be explained')
    for site in sites:
        require(bool(site['id']) and bool(site['name']), 'campsite ID/name required')
        url(site['booking_url'])
        availability = site['availability']
        require(availability['status'] in {'available', 'unavailable', 'unknown', 'request_required'}, 'invalid availability status')
        require(availability['arrival'] == trip['arrival'] and availability['departure'] == trip['departure'], 'availability dates differ from trip')
        if availability['status'] != 'unknown':
            stamp(availability['checked_at'])
            url(availability['source_url'])
            require(bool(availability['scope']), 'availability scope required')
        quote = site.get('quote')
        if quote is None:
            continue  # No price is not a zero-price offer.
        require(quote['currency'] == trip['currency'], 'mixed currencies need conversion outside core')
        digits = count(quote['minor_unit_digits'])
        require(digits <= 4, 'minor_unit_digits must be between 0 and 4')
        quantum = Decimal(1).scaleb(-digits)
        require(bool(quote['scope']), 'quote party/unit scope required')
        stamp(quote['checked_at'])
        url(quote['source_url'])
        require(quote['arrival'] == trip['arrival'] and quote['departure'] == trip['departure'], 'quote dates differ from trip')
        rates = quote['nightly_rates']
        require(len(rates) == nights, 'nightly rate count differs from nights')
        subtotal = sum((money(v) for v in rates), Decimal(0))
        require(money(quote['subtotal']) == subtotal, 'subtotal arithmetic mismatch')
        discount = quote['discount']
        amount, eligible, fraction = money(discount['amount']), money(discount['eligible_amount']), money(discount['fraction'])
        require(fraction <= 1 and eligible <= subtotal, 'invalid discount base/fraction')
        require(amount == (eligible * fraction).quantize(quantum, rounding=ROUND_HALF_UP), 'discount arithmetic mismatch')
        require(type(discount['eligibility_verified']) is bool, 'discount eligibility must be boolean')
        if amount:
            require(discount['eligibility_verified'] and bool(discount['conditions']), 'applied discount requires verified conditions')
        require(money(quote['total']) == subtotal - amount + money(quote['known_fees']), 'whole-stay total arithmetic mismatch')
        require(isinstance(quote['excluded_or_unknown_fees'], list), 'unknown fees must be explicit array')
    meals = plan.get('meal_ideas')
    if meals is not None:
        require(set(meals['requested']) == set(meals['items']), 'meal categories differ')
        for category, expected in meals['requested'].items():
            require(isinstance(meals['items'][category], list), 'meal ideas must be arrays')
            require(len(meals['items'][category]) == count(expected), f'meal count mismatch: {category}')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding='utf-8'))
        validate(plan)
    except (ValueError, KeyError, TypeError, OSError, ZoneInfoNotFoundError) as exc:
        parser.exit(1, f'INVALID: {exc}\n')
    print('VALID core; independently verify sources, live data, and artifact rendering.')


if __name__ == '__main__':
    main()
