from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from clinic.forms import AppointmentForm
from clinic.utils.map_embed import is_allowed_map_embed_url, normalize_map_embed, resolve_map_embed_src
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


class MapEmbedUtilsTests(SimpleTestCase):
    IFRAME = (
        '<iframe src="https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d2540.35'
        '!2d30.51162307654055!3d50.4531663871682!2m3!1f0!2f0!3f0!3m2!1i1024!2i768'
        '!4f13.1!3m2!1m1!2s!5e0!3m2!1sru!2sua!4v1783347305093!5m2!1sru!2sua" '
        'width="600" height="450" style="border:0;" allowfullscreen="" '
        'loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>'
    )
    SRC = (
        'https://www.google.com/maps/embed?pb=!1m17!1m12!1m3!1d2540.35'
        '!2d30.51162307654055!3d50.4531663871682!2m3!1f0!2f0!3f0!3m2!1i1024!2i768'
        '!4f13.1!3m2!1m1!2s!5e0!3m2!1sru!2sua!4v1783347305093!5m2!1sru!2sua'
    )

    def test_extracts_src_from_iframe(self):
        self.assertEqual(normalize_map_embed(self.IFRAME), self.SRC)

    def test_passes_through_embed_url(self):
        self.assertEqual(normalize_map_embed(self.SRC), self.SRC)

    def test_empty_value(self):
        self.assertEqual(normalize_map_embed(''), '')
        self.assertEqual(normalize_map_embed('   '), '')

    def test_invalid_iframe_without_src(self):
        self.assertEqual(normalize_map_embed('<iframe width="600"></iframe>'), '')

    def test_allowed_google_embed_url(self):
        self.assertTrue(is_allowed_map_embed_url(self.SRC))

    def test_rejects_non_google_url(self):
        self.assertFalse(is_allowed_map_embed_url('https://example.com/maps/embed'))

    def test_resolve_prefers_embed_over_coordinates(self):
        src = resolve_map_embed_src(self.IFRAME, lat='50.1', lng='30.2', address='Київ')
        self.assertEqual(src, self.SRC)
