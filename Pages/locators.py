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

    @staticmethod
    def product_image(product_name):
        return (By.XPATH, f"//img[@alt='{product_name}']")


class ProductPageLocators:
    ADD_TO_CART_BTN = (By.NAME, "add_cart_product")
    CART_BADGE = (By.CSS_SELECTOR, "#cart .badge")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.title")
    SIZE_OPTION = (By.NAME, "options[Size]")

    @staticmethod
    def size_option(size_name):
        return (By.XPATH, f"//select[@name='options[Size]']/option[text()='{size_name}']")


class CheckoutPageLocators:
    CHECKOUT_WRAPPER = (By.CLASS_NAME, "cart wrapper")
    CHECKOUT_CART = (By.ID, "box-checkout-cart")
    ITEM_PRICE = (By.CLASS_NAME, "unit-price")
    CARD_BODY = (By.CLASS_NAME, "card-body")

    COMPANY_INPUT = (By.NAME, "company")
    TAX_ID_INPUT = (By.NAME, "tax_id")
    FIRSTNAME_INPUT = (By.NAME, "firstname")
    LASTNAME_INPUT = (By.NAME, "lastname")
    ADDRESS1_INPUT = (By.NAME, "address1")
    ADDRESS2_INPUT = (By.NAME, "address2")
    POSTALCODE_INPUT = (By.NAME, "postcode")
    CITY_INPUT = (By.NAME, "city")
    COUNTRY_CODE_SELECT = (By.NAME, "country_code")
    ZONE_CODE_SELECT = (By.NAME, "zone_code")
    EMAIL_INPUT = (By.NAME, "email")
    PHONE_INPUT = (By.NAME, "phone")

    CHECKOUT_CART_ITEMS = (By.CSS_SELECTOR, "#box-checkout-cart .items")
    CHECKBOX_TERMS_AGREED = (By.NAME, "terms_agreed")
    CONFIRM_ORDER_BTN = (By.NAME, "confirm_order")
    SAVE_CHANGES_BTN = (By.NAME, "save_customer_details")


class OrderSuccessPageLocators:
    ORDER_CONFIRMED_MSG = (By.CSS_SELECTOR, "h1.card-title")
    ITEM_LIST = (By.CSS_SELECTOR, "ul > li.item")

