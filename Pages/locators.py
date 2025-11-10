from selenium.webdriver.common.by import By
from Config.config import TestData


class BasePageLocators:
    SITE_LOGO = (By.CSS_SELECTOR, "a.logotype")
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
    PRINTABLE_COPY_BUTTON = (By.CSS_SELECTOR, ".card-body .btn")


class OrderPrintableCopyPageLocators:

    SHIPPING_ADDRESS_BLOCK = (By.CSS_SELECTOR, ".shipping-address .value")
    BILLING_ADDRESS_BLOCK = (By.CSS_SELECTOR, ".billing-address .rounded-rectangle .value")

    SHIPPING_WEIGHT = (By.XPATH,
                       "//div[normalize-space(text())='Shipping Weight']/following-sibling::div[@class='value']")
    SHIPPING_OPTION = (By.XPATH,
                       "//div[normalize-space(text())='Shipping Option']/following-sibling::div[@class='value']")
    SHIPPING_TRACKING_ID = (By.XPATH,
                            "//div[normalize-space(text())='Shipping Tracking ID']/following-sibling::div[@class='value']")


    PAYMENT_OPTION = (By.XPATH,
                      "//div[normalize-space(text())='Payment Option']/following-sibling::div[@class='value']")
    TRANSACTION_NUMBER = (By.XPATH,
                          "//div[normalize-space(text())='Transaction Number']/following-sibling::div[@class='value']")

    EMAIL_BLOCK = (By.XPATH, "//div[normalize-space(text())='Email']/following-sibling::div[@class='value']")
    PHONE_NUMBER_BLOCK = (By.XPATH,
                          "//div[normalize-space(text())='Phone Number']/following-sibling::div[@class='value']")
    TAX_ID_BLOCK = (By.XPATH, "//div[normalize-space(text())='Tax ID / VATIN']/following-sibling::div[@class='value']")

    ITEMS_TABLE = (By.CSS_SELECTOR, "table.items.data-table")

    ITEM_ROW = (By.XPATH, "//table[contains(@class,'items')]//tbody/tr")
    ITEM_SKU = (By.XPATH, "//table[contains(@class,'items')]//tbody/tr[1]/td[1]")
    ITEM_NAME_AND_SIZE = (By.XPATH, "//table[contains(@class,'items')]//tbody/tr[1]/td[2]")
    ITEM_QUANTITY = (By.XPATH, "//table[contains(@class,'items')]//tbody/tr[1]/td[3]")
    ITEM_UNIT_PRICE = (By.XPATH, "//table[contains(@class,'items')]//tbody/tr[1]/td[4]")
    ITEM_TAX = (By.XPATH, "//table[contains(@class,'items')]//tbody/tr[1]/td[5]")
    ITEM_TOTAL_SUM = (By.XPATH, "//table[contains(@class,'items')]//tbody/tr[1]/td[6]")

    ORDER_TOTAL_TABLE = (By.XPATH, "//table[contains(@class,'order-total')]")
    ORDER_TOTAL_TABLE_ROW = (By.XPATH, "//table[contains(@class,'order-total')]//tr")
    ORDER_SUBTOTAL = (By.XPATH,
                      "//table[contains(@class,'order-total')]//td[normalize-space(text())='Subtotal:']/following-sibling::td")
    ORDER_DELIVERY_COST = (By.XPATH,
                           "//table[contains(@class,'order-total')]//td[contains(text(),'Cash on Delivery')]/following-sibling::td")
    ORDER_TAX_INCLUDED = (By.XPATH,
                          "//table[contains(@class,'order-total')]//td[normalize-space(text())='Including Tax:']/following-sibling::td")
    ORDER_GRAND_TOTAL = (By.XPATH,
                         "//table[contains(@class,'order-total')]//td[strong[contains(.,'Grand Total:')]]/following-sibling::td//span[@class='currency-amount']")