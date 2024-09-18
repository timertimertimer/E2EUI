import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_login(driver):
    url = 'https://www.saucedemo.com/'
    driver.get(url)
    driver.find_element(By.ID, 'user-name').send_keys('standard_user')
    driver.find_element(By.ID, 'password').send_keys('secret_sauce')
    driver.find_element(By.ID, 'login-button').click()
    assert "inventory" in driver.current_url, "Login failed"


def test_add_product_to_cart(driver):
    item = 'Sauce Labs Backpack'
    driver.find_element(By.XPATH, f"//div[text()='{item}']").click()
    driver.find_element(By.ID, 'add-to-cart').click()
    driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()
    cart_item = driver.find_element(By.CLASS_NAME, 'inventory_item_name').text
    assert cart_item == item, f"Expected product not found. Found: {cart_item}"


def test_checkout(driver):
    driver.find_element(By.ID, 'checkout').click()
    driver.find_element(By.ID, 'first-name').send_keys('John')
    driver.find_element(By.ID, 'last-name').send_keys('Doe')
    driver.find_element(By.ID, 'postal-code').send_keys('12345')
    driver.find_element(By.ID, 'continue').click()
    driver.find_element(By.ID, 'finish').click()
    success_msg = driver.find_element(By.CLASS_NAME, 'complete-header').text
    assert success_msg == "Thank you for your order!", f"Purchase failed. Message: {success_msg}"
