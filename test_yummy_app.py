import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    """Kiem thu tinh tong tien don hang."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


class TestMediumLevel(unittest.TestCase):
    """Bon ca kiem thu ma giam gia theo bang thiet ke."""

    def test_giam10_when_online(self):
        app = YummyApp(network_status="online")
        result = app.apply_promo_code(100000, "GIAM10")
        self.assertEqual(result, 90000)

    def test_promo_code_when_offline(self):
        app = YummyApp(network_status="offline")
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_new_os_only_on_os_15(self):
        app = YummyApp(os_version=15)
        result = app.apply_promo_code(100000, "NEW_OS_ONLY")
        self.assertEqual(result, 80000)

    def test_new_os_only_on_os_14(self):
        app = YummyApp(os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
    """Ba ca kiem thu GPS bang mock."""

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_inside_region(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        result = YummyApp().get_nearby_restaurants()
        self.assertEqual(
            result,
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_outside_region(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        result = YummyApp().get_nearby_restaurants()
        self.assertEqual(result, [])

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_signal_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError()
        result = YummyApp().get_nearby_restaurants()
        self.assertEqual(result, "Khong the xac dinh vi tri.")


if __name__ == "__main__":
    unittest.main()
