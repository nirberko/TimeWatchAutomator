import unittest
from unittest.mock import patch, MagicMock
import timewatcher


class TestTimewatcher(unittest.TestCase):

    @patch('timewatcher.get_config')
    @patch('timewatcher.webdriver.Chrome')
    def test_login(self, MockChrome, mock_get_config):
        # Mock the config to return test data
        mock_get_config.return_value = {
            'company_id': 'test_company',
            'user_id': 'test_user',
            'password': 'test_password'
        }

        # Mock the web driver
        mock_driver = MagicMock()
        MockChrome.return_value = mock_driver

        # Call the login function
        timewatcher.login(mock_driver)

        # Check if the correct calls were made
        mock_driver.get.assert_called_once_with('https://checkin.timewatch.co.il/punch/punch.php')
        self.assertEqual(mock_driver.find_element.call_count, 4)
        mock_driver.find_element().send_keys.assert_any_call('test_company')
        mock_driver.find_element().send_keys.assert_any_call('test_user')
        mock_driver.find_element().send_keys.assert_any_call('test_password')
        mock_driver.find_element().click.assert_called_once()


if __name__ == '__main__':
    unittest.main()
