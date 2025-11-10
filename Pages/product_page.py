import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import ProductPageLocators


class ProductPage(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.wait_for_page_stability()

    def _get_cart_count(self):
        try:
            badge = self.driver.find_element(*ProductPageLocators.CART_BADGE)
            return int(badge.text.strip()) if badge.text.strip().isdigit() else 0
        except Exception:
            return 0

    def _cart_count_changed(self, old_count):
        new_count = self._get_cart_count()
        return new_count - old_count

    @allure.step("Проверить возможность выбрать размер товара")
    def should_be_size_select(self):
        assert self.is_element_present(ProductPageLocators.SIZE_OPTION)

    @allure.step("Выбрать размер товара: {option}")
    def choose_size(self, option):
        if not self.is_element_present(ProductPageLocators.SIZE_OPTION):
            return

        self.do_click(ProductPageLocators.SIZE_OPTION)
        options = self.get_list_items(ProductPageLocators.SIZE_OPTION)
        options.select_by_visible_text(option)

    def add_to_cart(self, total_expected=None):
        self.log_step("Добавление товара в корзину", ProductPageLocators.ADD_TO_CART_BTN)

        old_count = self._get_cart_count()
        self.do_click(ProductPageLocators.ADD_TO_CART_BTN)
        self.wait_for_element(ProductPageLocators.CART_BADGE)

        WebDriverWait(self.driver, 10).until(
            lambda d: self._cart_count_changed(old_count),
            message=f"Badge count did not increase after adding product (previous count: {old_count})"
        )

        new_count = self._get_cart_count()

        msg = f"✅ Товар успешно добавлен. В корзине теперь: {new_count}"
        if total_expected:
            msg += f" из {total_expected}"
        allure.attach(
            msg,
            name=f"Cart status (товаров: {new_count})",
            attachment_type=allure.attachment_type.TEXT
        )

        return new_count

    @allure.step("Проверить, что значок корзины отображает добавленные товары")
    def should_be_items_in_cart_badge(self):
        cart_badge_quantity = self.get_element_text(ProductPageLocators.CART_BADGE)
        assert cart_badge_quantity != "", "Cart badge not found. Have the product added to cart?"
