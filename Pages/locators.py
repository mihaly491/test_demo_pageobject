from selenium.webdriver.common.by import By
from Config.config import TestData


class BasePageLocators:
    SEARCH = (By.NAME, "query")
    REGIONAL_SETTINGS = (By.CLASS_NAME, "regional-setting")
    ACCOUNT = (By.CLASS_NAME, "account")
    CART = (By.ID, "cart")
    COOKIE_NOTICE = (By.ID, "box-cookie-notice")
    ACCEPT_COOKIES_BTN = (By.NAME, "accept_cookies")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    SIGNUP_NAV_BTN = (By.CSS_SELECTOR, "li.nav-item.account.dropdown > a")
    LOGIN_BTN = (By.NAME, "login")


class MainPageLocators:
    ALERT_MSG = (By.CSS_SELECTOR, ".alert.alert-success")
    PRODUCT_AREA = (By.CSS_SELECTOR, "article.product")
    PRODUCT_BOX = (By.CSS_SELECTOR, "article.product img")
    PRODUCT_IMAGE = (By.XPATH, f"//img[@alt='{TestData.PRODUCT}']")


class ProductPageLocators:
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.title")
    SIZE_OPTION = (By.NAME, "options[Size]")
    ADD_TO_CART_BTN = (By.NAME, "add_cart_product")
    CART_BADGE = (By.CSS_SELECTOR, "#cart .badge")


class CheckoutPageLocators:
    CHECKOUT_WRAPPER = (By.CLASS_NAME, "cart wrapper")
    CHECKOUT_CART = (By.ID, "box-checkout-cart")
    CHECKOUT_CART_ITEMS = (By.CSS_SELECTOR, "#box-checkout-cart .items")
    CHECKBOX_TERMS_AGREED = (By.NAME, "terms_agreed")
    CONFIRM_ORDER_BTN = (By.NAME, "confirm_order")
    ITEM_PRICE = (By.CLASS_NAME, "unit-price")


class OrderSuccessPageLocators:
    ORDER_CONFIRMED_MSG = (By.CLASS_NAME, "card-title")
    ITEM_LIST = (By.CLASS_NAME, "item")
