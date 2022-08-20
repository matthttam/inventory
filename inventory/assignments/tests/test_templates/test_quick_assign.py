from assignments.tests.factories import DeviceAssignmentFactory
from authentication.tests.factories import SuperuserUserFactory, User
from bs4 import BeautifulSoup
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase, TestCase
from django.urls import reverse
from inventory.tests.helpers import chrome_set_value, get_chrome_driver
from people.tests.factories import PersonFactory
from devices.tests.factories import DeviceFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumlogin import force_login


class DeviceAssignmentQuickAssignTemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SuperuserUserFactory(username="my_superuser@example.com")
        DeviceAssignmentFactory(id=1)

    def setUp(self):
        self.user = User.objects.get(username="my_superuser@example.com")
        self.client.force_login(self.user)
        self.response = self.client.get(reverse("assignments:quickassign"))

    def test_templates(self):
        self.assertTemplateUsed(self.response, "dashboard/dashboard.html")

    def test_title(self):
        self.assertInHTML("Inventory - Quick Assign", self.response.content.decode())

    def test_buttons(self):
        soup = BeautifulSoup(self.response.content.decode(), "html.parser")
        submit_buttons = soup.find("form").select('button[type="submit"]')
        self.assertEqual(len(submit_buttons), 1)
        self.assertInHTML(submit_buttons[0].contents[0], "Submit")


class DeviceAssignmentQuickAssignLiveTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = get_chrome_driver()
        superuser = SuperuserUserFactory()
        force_login(superuser, self.browser, f"{self.live_server_url}/")
        self.browser.get(f"{self.live_server_url}/assignments/quickassign/")
        self.my_person_list = [
            {
                "internal_id": "1234",
                "first_name": "Adam",
                "last_name": "Smith",
                "email": "Adam.Smith@example.com",
            },
            {
                "internal_id": "2345",
                "first_name": "Bob",
                "last_name": "Smith",
                "email": "Bob.Smith@example.com",
            },
        ]
        PersonFactory(**self.my_person_list[0])
        PersonFactory(**self.my_person_list[1])

        self.my_device_list = [
            {"asset_id": "L001234", "serial_number": "SN-0"},
            {"asset_id": "L001235", "serial_number": "SN-1"},
        ]
        DeviceFactory(**self.my_device_list[0])
        DeviceFactory(**self.my_device_list[1])

    def get_device_search_box(self):
        return self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="check_form"]/div[1]/div/span/span/span[1]/input',
        )

    def get_person_search_box(self):
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="check_form"]/div[2]/div/span/span/span[1]/input',
                )
            )
        )
        return self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="check_form"]/div[2]/div/span/span/span[1]/input',
        )

    def open_person_search_box(self):
        self.browser.execute_script(
            f"$('#person').select2('open')",
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="person"]',
                    )
                )
            ),
        )

    # DEVICE SEARCH TESTS
    def test_device_search_is_focused_load(self):
        device_search_box = self.get_device_search_box()
        self.assertEqual(
            device_search_box,
            self.browser.switch_to.active_element,
            msg="Device search box is not focused automatically!",
        )

    def test_device_search_uses_asset(self):
        device_search_box = self.get_device_search_box()
        device_search_box.send_keys("L00")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-device-results" and not(contains(., "Searching…"))]',
                )
            )
        )
        results_box = device_search_box.find_element(
            by=By.XPATH,
            value='//*[@id="select2-device-results"]',
        )
        list_options = results_box.find_elements(by=By.TAG_NAME, value="li")
        list_option_values = [element.text for element in list_options]
        self.assertCountEqual(list_option_values, ["L001234 (SN-0)", "L001235 (SN-1)"])

    def test_device_search_uses_serial(self):
        device_search_box = self.get_device_search_box()
        device_search_box.send_keys("SN-")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-device-results" and not(contains(., "Searching…"))]',
                )
            )
        )
        results_box = device_search_box.find_element(
            by=By.XPATH,
            value='//*[@id="select2-device-results"]',
        )
        list_options = results_box.find_elements(by=By.TAG_NAME, value="li")
        list_option_values = [element.text for element in list_options]
        self.assertCountEqual(list_option_values, ["L001234 (SN-0)", "L001235 (SN-1)"])

    def test_device_search_matches_on_asset(self):
        device_search_box = self.get_device_search_box()
        device_search_box.send_keys("L001235")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-device-container" and not(contains(., "L######"))]',
                )
            )
        )
        selection = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-device-container"]',
        )

        self.assertEqual(selection.text, "L001235 (SN-1)")

    def test_device_search_matches_on_serial(self):
        device_search_box = self.get_device_search_box()
        device_search_box.send_keys("SN-1")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-device-container" and not(contains(., "L######"))]',
                )
            )
        )
        selection = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-device-container"]',
        )

        self.assertEqual(selection.text, "L001235 (SN-1)")

    ### Person Search
    def test_person_search_uses_internal_id(self):
        self.open_person_search_box()
        person_search_box = self.get_person_search_box()
        person_search_box.send_keys("123")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-person-results" and not(contains(., "Searching…"))]',
                )
            )
        )

        results_box = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-person-results"]',
        )
        list_options = results_box.find_elements(by=By.TAG_NAME, value="li")
        list_option_values = [element.text for element in list_options]
        self.assertCountEqual(list_option_values, ["Smith, Adam - 1234"])

    def test_person_search_uses_first_name(self):
        self.browser.execute_script(
            f"$('#person').select2('open')",
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="person"]',
                    )
                )
            ),
        )
        person_search_box = self.get_person_search_box()
        person_search_box.send_keys("Ada")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-person-results" and not(contains(., "Searching…"))]',
                )
            )
        )

        results_box = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-person-results"]',
        )
        list_options = results_box.find_elements(by=By.TAG_NAME, value="li")
        list_option_values = [element.text for element in list_options]
        self.assertCountEqual(list_option_values, ["Smith, Adam - 1234"])

    def test_person_search_uses_last_name(self):
        self.browser.execute_script(
            f"$('#person').select2('open')",
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="person"]',
                    )
                )
            ),
        )
        person_search_box = self.get_person_search_box()
        person_search_box.send_keys("Smi")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-person-results" and not(contains(., "Searching…"))]',
                )
            )
        )

        results_box = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-person-results"]',
        )
        list_options = results_box.find_elements(by=By.TAG_NAME, value="li")
        list_option_values = [element.text for element in list_options]
        self.assertCountEqual(
            list_option_values, ["Smith, Adam - 1234", "Smith, Bob - 2345"]
        )

    def test_person_search_uses_combined_name(self):
        self.open_person_search_box()
        person_search_box = self.get_person_search_box()
        person_search_box.send_keys("adam smith")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-person-results" and not(contains(., "Searching…"))]',
                )
            )
        )

        results_box = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-person-results"]',
        )
        list_options = results_box.find_elements(by=By.TAG_NAME, value="li")
        list_option_values = [element.text for element in list_options]
        self.assertCountEqual(list_option_values, ["Smith, Adam - 1234"])

    def test_person_search_uses_comma_combined_name(self):
        """'Smith, Adam' should return results for 'first name like Adam* and last name like Smith*'"""
        self.open_person_search_box()
        person_search_box = self.get_person_search_box()
        person_search_box.send_keys("Smith, Adam")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-person-results" and not(contains(., "Searching…"))]',
                )
            )
        )

        results_box = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-person-results"]',
        )
        list_options = results_box.find_elements(by=By.TAG_NAME, value="li")
        list_option_values = [element.text for element in list_options]
        self.assertCountEqual(list_option_values, ["Smith, Adam - 1234"])

    def test_person_search_uses_email(self):
        self.open_person_search_box()
        person_search_box = self.get_person_search_box()
        person_search_box.send_keys("adam.smith@example.")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-person-results" and not(contains(., "Searching…"))]',
                )
            )
        )

        results_box = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-person-results"]',
        )
        list_options = results_box.find_elements(by=By.TAG_NAME, value="li")
        list_option_values = [element.text for element in list_options]
        self.assertCountEqual(list_option_values, ["Smith, Adam - 1234"])

    def test_person_search_matches_on_internal_id(self):
        self.open_person_search_box()
        person_search_box = self.get_person_search_box()
        person_search_box.send_keys("1234")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-person-container" and not(contains(., "ID, Email, or Name"))]',
                )
            )
        )
        selection = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-person-container"]',
        )

        self.assertEqual(selection.text, "Smith, Adam - 1234")

    def test_person_search_matches_on_email(self):
        self.open_person_search_box()
        person_search_box = self.get_person_search_box()
        person_search_box.send_keys("adam.smith@example.com")
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="select2-person-container" and not(contains(., "ID, Email, or Name"))]',
                )
            )
        )
        selection = self.browser.find_element(
            by=By.XPATH,
            value='//*[@id="select2-person-container"]',
        )

        self.assertEqual(selection.text, "Smith, Adam - 1234")
