#!/usr/bin/env python3
import copy
import json
import unittest
from pathlib import Path
from validate_plan import validate

SAMPLE = json.loads((Path(__file__).resolve().parents[1] / 'references/example-plan.json').read_text())


class ValidationTests(unittest.TestCase):
    def reject(self, mutate):
        plan = copy.deepcopy(SAMPLE)
        mutate(plan)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            validate(plan)

    def test_valid(self):
        self.assertTrue(validate(SAMPLE))

    def test_nights(self):
        self.reject(lambda p: p['trip'].update(nights=3))

    def test_rate_count(self):
        self.reject(lambda p: p['campsites'][0]['quote'].update(nightly_rates=[100]))

    def test_total(self):
        self.reject(lambda p: p['campsites'][0]['quote'].update(total=100))

    def test_half_price_not_whole_stay(self):
        self.reject(lambda p: p['campsites'][0]['quote']['discount'].update(amount=100))

    def test_unverified_discount(self):
        self.reject(lambda p: p['campsites'][0]['quote']['discount'].update(eligibility_verified=False))

    def test_unknown_not_reserved(self):
        self.reject(lambda p: p['campsites'][0]['availability'].update(status='reserved'))

    def test_available_needs_timestamp(self):
        self.reject(lambda p: p['campsites'][0]['availability'].update(checked_at='2026-10-27T10:00:00'))

    def test_wrong_inventory_dates(self):
        self.reject(lambda p: p['campsites'][0]['availability'].update(arrival='2030-06-02'))

    def test_count_shortfall(self):
        self.reject(lambda p: p.update(requested_campsites=2))

    def test_meal_count(self):
        self.reject(lambda p: p['meal_ideas']['requested'].update(breakfast=90))

    def test_duplicate(self):
        self.reject(lambda p: p['campsites'].append(copy.deepcopy(p['campsites'][0])))

    def test_fractional_discount_rounding(self):
        plan = copy.deepcopy(SAMPLE)
        quote = plan['campsites'][0]['quote']
        quote.update(nightly_rates=[19.99, 19.99], subtotal=39.98, total=45.98)
        quote['discount'].update(eligible_amount=19.99, fraction=0.2, amount=4.00)
        self.assertTrue(validate(plan))

    def test_unknown_quote_allowed(self):
        plan = copy.deepcopy(SAMPLE)
        plan['campsites'][0]['quote'] = None
        plan['campsites'][0]['availability'] = {'status': 'unknown', 'arrival': '2030-06-01', 'departure': '2030-06-03'}
        self.assertTrue(validate(plan))


if __name__ == '__main__':
    unittest.main()
