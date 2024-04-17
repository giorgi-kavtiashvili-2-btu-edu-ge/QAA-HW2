import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PurchasePage:
    def __init__(self, driver):
        self.driver = driver
        self.men_category_link = (By.LINK_TEXT, 'Men')
        self.product_item = (By.CSS_SELECTOR, '.product-item')
        self.add_to_cart_button = (By.ID, 'product-addtocart-button')
        self.error_message = (By.CSS_SELECTOR, '.message-error')

    def navigate_to_men_category(self):
        self.driver.get("https://magento.softwaretestingboard.com/")
        self.driver.find_element(*self.men_category_link).click()

    def choose_item_and_add_to_cart(self):
        product_items = self.driver.find_elements(*self.product_item)
        # Choose the first product item
        product_items[0].click()
        # Wait for add to cart button to be clickable
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_to_cart_button))
        add_to_cart_button.click()

    def get_error_message(self):
        try:
            error_message = self.driver.find_element(*self.error_message).text
            return error_message
        except:
            return None


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_item_purchase(browser):
    purchase_page = PurchasePage(browser)
    purchase_page.navigate_to_men_category()
    purchase_page.choose_item_and_add_to_cart()
    error_message = purchase_page.get_error_message()
    assert error_message is None, f"Error message displayed: {error_message}"

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html"])
