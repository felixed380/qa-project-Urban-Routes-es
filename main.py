import data
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    comfort_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[2]')
    phone_number_field = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div')
    phone_number_window = (By.XPATH, '//*[@id="phone"]')
    next_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    sms_code = (By.XPATH, '//*[@id="code"]')
    confirmation_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    change_payment_method = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')
    add_card_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[3]/div')
    #card_number_button =(By.ID, 'number')
    card_number_button = (By.XPATH, '//*[@id="number"]')
    edit_card_number_click = (By.XPATH, '//*[@id="number"]')
    card_code_button = (By.CSS_SELECTOR, 'div.card-code-input')
    card_code_input = (By.CSS_SELECTOR, 'div.card-code-input input#code')
    confirm_card_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    technical_click = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form')
    close_payment_methods = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    message_button = (By.XPATH, '//*[@id="comment"]')
    activate_manta_and_panuelos = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/input')
    icecream_counter = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')
    icecream_plus = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    request_cab = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def set_from(self, from_address):
        field = self.wait.until(EC.visibility_of_element_located(self.from_field))
        field.send_keys(from_address)

    def set_to(self, to_address):
        field = self.wait.until(EC.visibility_of_element_located(self.to_field))
        field.send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        field = self.wait.until(EC.visibility_of_element_located(self.from_field))
        return field.get_property('value')

    def get_to(self):
        field = self.wait.until(EC.visibility_of_element_located(self.to_field))
        return field.get_property('value')

    def click_on_get_taxi(self):
        self.wait.until(EC.visibility_of_element_located(self.request_taxi_button)).click()

    def select_comfort(self):
        field = self.wait.until(EC.visibility_of_element_located(self.comfort_button))
        field.click()
        return field.text

    def set_phone_number(self, phone):
        self.wait.until(EC.visibility_of_element_located(self.phone_number_field)).click()
        field = self.wait.until(EC.visibility_of_element_located(self.phone_number_window))
        field.send_keys(phone)

    def get_phone_number(self):
        field = self.wait.until(EC.visibility_of_element_located(self.phone_number_window))
        return field.get_property('value')

    def confirm_phone_number(self):
        self.wait.until(EC.element_to_be_clickable(self.next_button)).click()
        field = self.wait.until(EC.visibility_of_element_located(self.sms_code))
        code = retrieve_phone_code(self.driver)
        field.send_keys(code)
        self.wait.until(EC.element_to_be_clickable(self.confirmation_button)).click()


    def set_payment_method(self):
        self.driver.find_element(*self.change_payment_method).click()
        self.driver.find_element(*self.add_card_button).click()


    def set_card_number(self):
        self.wait.until(EC.element_to_be_clickable(self.edit_card_number_click)).click()
        field = self.driver.find_element(*self.card_number_button)
        field.send_keys(data.card_number)
        field.send_keys(Keys.TAB)

    def get_card_number(self):
        field = self.driver.find_element(*self.card_number_button)
        return field.get_property('value')

    def set_card_code(self):
        field = self.wait.until(EC.element_to_be_clickable(self.card_code_button))
        field.click()
        self.driver.switch_to.active_element.send_keys(data.card_code)
        self.driver.find_element(*self.technical_click).click()

    def get_card_code(self):
        field = self.driver.find_element(*self.card_code_input)
        return field.get_property('value')

    def confirm_and_close_payment(self):
        self.wait.until(EC.element_to_be_clickable(self.confirm_card_button)).click()
        self.wait.until(EC.element_to_be_clickable(self.close_payment_methods)).click()

    def message_for_driver(self):
        field = self.driver.find_element(*self.message_button)
        field.send_keys(data.message_for_driver)
        field.send_keys(Keys.TAB)

    def get_message_for_driver(self):
        field = self.driver.find_element(*self.message_button)
        return field.get_property('value')

    def manta_y_panuelos(self):
        checkbox = self.driver.find_element(*self.activate_manta_and_panuelos)
        self.driver.execute_script("arguments[0].click();", checkbox)

    def check_manta_y_panuelos(self):
        checkbox = self.driver.find_element(*self.activate_manta_and_panuelos)
        return checkbox.is_selected()

    def icecream_plus_method(self):
        plus_button = self.driver.find_element(*self.icecream_plus)
        plus_button.click()
        plus_button.click()

    def icecream_count(self):
        icecream_check = self.driver.find_element(*self.icecream_counter)
        return icecream_check.text

    def confirm_cab(self):
        self.driver.find_element(*self.request_cab).click()
        time.sleep(35)

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        driver_options = Options()
        driver_options.add_argument('--window-size=1800,1200')
        driver_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=driver_options)



    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
        routes_page.click_on_get_taxi()
        routes_page.select_comfort()
        assert routes_page.select_comfort() == 'Comfort'
        routes_page.set_phone_number(data.phone_number)
        assert routes_page.get_phone_number() == data.phone_number
        routes_page.confirm_phone_number()
        routes_page.set_payment_method()
        routes_page.set_card_number()
        assert routes_page.get_card_number() == data.card_number
        routes_page.set_card_code()
        assert routes_page.get_card_code() == data.card_code
        routes_page.confirm_and_close_payment()
        routes_page.message_for_driver()
        assert routes_page.get_message_for_driver() == data.message_for_driver
        routes_page.manta_y_panuelos()
        assert routes_page.check_manta_y_panuelos() == True
        routes_page.icecream_plus_method()
        assert routes_page.icecream_count() == '2'
        routes_page.confirm_cab()
        time.sleep(5)


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
