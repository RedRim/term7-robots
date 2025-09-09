from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


username = 'standard_user'
password = 'secret_sauce'
url = 'https://www.saucedemo.com/'

# Г: Сортировка по цене (high to low)
# A: Добавить первый товар из списка.
# Б: Добавить товар в корзину, перейти в корзину и удалить его оттуда.


def main():
    driver = setup()
    try:
        login(driver)
        sort_by_price(driver)
        add_to_cart(driver)
        go_to_cart(driver)
        remove_from_cart(driver)
    finally:
        teardown(driver)

def setup():
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    return driver

def login(driver):
    username_input = driver.find_element(By.ID, 'user-name')
    password_input = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.ID, 'login-button')

    username_input.send_keys(username)
    time.sleep(0.5)
    password_input.send_keys(password)
    time.sleep(0.5)
    login_button.click()
    time.sleep(1)

def sort_by_price(driver):
    time.sleep(0.5)
    sort_select = driver.find_element(By.CSS_SELECTOR, 'select.product_sort_container')
    Select(sort_select).select_by_value('hilo')
    time.sleep(1)

def add_to_cart(driver):
    time.sleep(0.5)
    button = driver.find_element(By.NAME, 'add-to-cart-sauce-labs-fleece-jacket')
    button.click()
    time.sleep(1)

def go_to_cart(driver):
    time.sleep(0.5)
    button = driver.find_element(By.CLASS_NAME, 'shopping_cart_link')
    button.click()
    time.sleep(1)

def remove_from_cart(driver):
    time.sleep(0.5)
    button = driver.find_element(By.NAME, 'remove-sauce-labs-fleece-jacket')
    button.click()
    time.sleep(1)

def teardown(driver):
    driver.quit()

main()