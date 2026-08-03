from django.test import TestCase

from .admin import ReservationAdmin, ReservationTableTypeDetailInline


class ReservationAdminTests(TestCase):
    def test_reservation_admin_has_inline_for_table_type_details(self):
        self.assertIn(ReservationTableTypeDetailInline, ReservationAdmin.inlines)
