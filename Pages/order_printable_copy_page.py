from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Base.base_page import BasePage
from Config.config import TestData
from Pages.locators import OrderPrintableCopyPageLocators
from Pages.checkout_page import CheckoutPage
import allure
import json
import re


class OrderPrintableCopyPage(BasePage):

    def __init__(self, driver, url, checkout_data):
        super().__init__(driver, url)
        self.switch_to_new_tab()
        self.wait_for_page_stability()
        self.checkout_data = checkout_data

    def _safe_get_text(self, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
            # text = self.driver.execute_script("return arguments[0].innerText;", element)
            return element.text.strip()
        except Exception:
            return ""

    def get_email(self):
        return self._safe_get_text(OrderPrintableCopyPageLocators.EMAIL_BLOCK)

    def get_phone_number(self):
        return self._safe_get_text(OrderPrintableCopyPageLocators.PHONE_NUMBER_BLOCK)

    def get_shipping_address(self):
        return self._safe_get_text(OrderPrintableCopyPageLocators.SHIPPING_ADDRESS_BLOCK)

    def get_billing_address(self):
        return self._safe_get_text(OrderPrintableCopyPageLocators.BILLING_ADDRESS_BLOCK)

    def _get_order_items(self):
        items = []
        rows = self.driver.find_elements(*OrderPrintableCopyPageLocators.ITEM_ROW)

        for row in rows:
            try:
                sku = row.find_element(By.XPATH, "./td[1]").text.strip()
                item = row.find_element(By.XPATH, "./td[2]").text.strip().replace("\n", " ")
                qty = row.find_element(By.XPATH, "./td[3]").text.strip()
                price = row.find_element(By.XPATH, "./td[4]").text.strip()
                tax = row.find_element(By.XPATH, "./td[5]").text.strip() if len(row.find_elements(By.XPATH, "./td[5]")) > 0 else ""
                sum_ = row.find_element(By.XPATH, "./td[6]").text.strip()

                items.append({
                    "sku": sku,
                    "item": item,
                    "qty": qty,
                    "price": price,
                    "tax": tax,
                    "sum": sum_,
                })
            except Exception as e:
                allure.attach(str(e), name="Ошибка при разборе строки таблицы", attachment_type=allure.attachment_type.TEXT)
                continue

        return items

    def _get_order_totals(self):
        totals = {}
        try:
            total_rows = self.driver.find_elements(*OrderPrintableCopyPageLocators.ORDER_TOTAL_TABLE_ROW)
            for row in total_rows:
                try:
                    label = row.find_element(By.XPATH, "./td[1]").text.strip()
                    value = row.find_element(By.XPATH, "./td[2]").text.strip()
                    totals[label] = value
                except Exception:
                    continue
        except Exception:
            pass
        return totals


    @allure.step("Сбор данных из печатной формы заказа")
    def collect_order_summary(self):
        data = {
            "billing_address": self.get_billing_address(),
            "shipping_address": self.get_shipping_address(),
            "email": self.get_email(),
            "phone": self.get_phone_number(),
            "order_items": self._get_order_items(),
            "order_totals": self._get_order_totals()
        }

        allure.attach(
            json.dumps(data, indent=2, ensure_ascii=False),
            name="Данные из печатной формы (collect_order_summary)",
            attachment_type=allure.attachment_type.JSON
        )

        return data

    @allure.step("Сравнение данных печатной формы с данными, введёнными при оформлении заказа")
    def assert_order_matches_checkout(self):
        printable_data = self.collect_order_summary()

        allure.attach(
            json.dumps(self.checkout_data, indent=2, ensure_ascii=False),
            name="Checkout data (expected)",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(printable_data, indent=2, ensure_ascii=False),
            name="Printable data (actual)",
            attachment_type=allure.attachment_type.JSON
        )

        self.assert_contains(
            self.checkout_data.get("address", ""),
            printable_data["shipping_address"],
            "Проверка адреса доставки"
        )

        self.assert_contains(
            self.checkout_data.get("address", ""),
            printable_data["billing_address"],
            "Проверка платёжного адреса"
        )

        self.assert_contains(
            self.checkout_data.get("email", ""),
            printable_data["email"],
            "Проверка email в печатной версии заказа"
        )

        self.assert_contains(
            self.checkout_data.get("phone", ""),
            printable_data["phone"],
            "Проверка номера телефона в печатной версии заказа"
        )

        with allure.step("Проверка данных о товарах в заказе"):
            expected_items = self.checkout_data.get("order_items", [])
            printed_items = printable_data.get("order_items", [])

            if not expected_items:
                allure.attach("Нет ожидаемых товаров", name="Checkout items", attachment_type=allure.attachment_type.TEXT)
            if not printed_items:
                allure.attach("Нет найденных товаров в печатной версии", name="Printable items", attachment_type=allure.attachment_type.TEXT)

            if isinstance(expected_items, dict):
                expected_items = [expected_items]
            if isinstance(printed_items, dict):
                printed_items = [printed_items]

            for expected_item in expected_items:
                with allure.step(f"Сравнение товара SKU: {expected_item.get('sku', '—')}"):
                    # Пытаемся найти соответствующий товар по SKU
                    matched = next((i for i in printed_items if expected_item["sku"] in i["sku"]), None)

                    if not matched:
                        self.assert_with_allure(
                            False,
                            expected=f"Товар с SKU {expected_item['sku']}",
                            actual="Не найден в печатной версии",
                            message=f"Проверка наличия товара {expected_item['sku']}"
                        )
                        continue

                    # Сравнение имени товара
                    self.assert_contains(
                        expected_item["item"],
                        matched["item"],
                        f"Проверка наименования товара SKU {expected_item['sku']}"
                    )

                    # Сравнение количества
                    self.assert_equals(
                        expected_item["qty"],
                        matched["qty"],
                        f"Проверка количества для SKU {expected_item['sku']}"
                    )

                    # Сравнение цены
                    self.assert_equals(
                        expected_item["price"],
                        matched["price"],
                        f"Проверка цены для SKU {expected_item['sku']}"
                    )

                    # Сравнение налога
                    self.assert_contains(
                        expected_item["tax"],
                        matched["tax"],
                        f"Проверка налога для SKU {expected_item['sku']}"
                    )

        with allure.step("Проверка итоговых сумм заказа"):
            expected_totals = self.checkout_data.get("order_totals", {})
            printed_totals = printable_data.get("order_totals", {})

            # Прикрепляем данные для прозрачности
            allure.attach(
                str(expected_totals),
                name="Ожидаемые суммы (из checkout)",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                str(printed_totals),
                name="Фактические суммы (из печатной версии)",
                attachment_type=allure.attachment_type.TEXT
            )

            for field, expected_value in expected_totals.items():
                actual_value = printed_totals.get(field)
                with allure.step(f"Проверка суммы '{field}'"):
                    self.assert_equals(
                        expected_value,
                        actual_value,
                        f"Проверка итоговой суммы: {field}"
                    )