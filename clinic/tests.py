from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from clinic.forms import AppointmentForm
from clinic.utils.phone_validation import is_valid_ua_phone, normalize_ua_phone


class PhoneValidationUtilsTests(SimpleTestCase):
    def test_valid_mobile_compact(self):
        self.assertTrue(is_valid_ua_phone('0671234567'))
        self.assertEqual(normalize_ua_phone('0671234567'), '+38 (067) 123-45-67')

    def test_valid_mobile_international(self):
        self.assertTrue(is_valid_ua_phone('+380671234567'))
        self.assertEqual(normalize_ua_phone('+380671234567'), '+38 (067) 123-45-67')

    def test_valid_formatted(self):
        self.assertEqual(
            normalize_ua_phone('+38 (067) 123-45-67'),
            '+38 (067) 123-45-67',
        )

    def test_valid_landline(self):
        self.assertTrue(is_valid_ua_phone('0441234567'))
        self.assertEqual(normalize_ua_phone('0441234567'), '+38 (044) 123-45-67')

    def test_invalid_short_number(self):
        self.assertFalse(is_valid_ua_phone('06712345'))

    def test_invalid_operator_prefix(self):
        self.assertFalse(is_valid_ua_phone('0171234567'))


class AppointmentFormPhoneTests(SimpleTestCase):
    def test_form_normalizes_phone(self):
        form = AppointmentForm()
        form.cleaned_data = {'phone': '0671234567'}
        self.assertEqual(form.clean_phone(), '+38 (067) 123-45-67')

    def test_form_rejects_invalid_phone(self):
        form = AppointmentForm()
        form.cleaned_data = {'phone': '123'}
        with self.assertRaises(ValidationError):
            form.clean_phone()
