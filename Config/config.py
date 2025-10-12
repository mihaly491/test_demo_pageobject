class TestData:
    BASE_URL = "https://demo.litecart.net"
    SHOPPINGCART_URL = f"{BASE_URL}/checkout"
    USER_NAME = "user@email.com"
    PASSWORD = "demo"
    ALERT_MSG = "are now logged in as John Doe."
    ORDER_CONFIRMED_MSG = "was completed successfully!"
    PRODUCT = "Yellow Duck"
    PRODUCTS = ["Yellow Duck", "Purple Duck", "Red Duck", "Green Duck", "Blue Duck"]
    PRODUCTS_WITH_SIZES = ["Yellow Duck"]
    PRODUCT_SIZE = "Small"
    PRODUCT_SIZES = ["Small", "Medium", "Large"]

    def change_product(self, product):
        self.PRODUCT = product

    def change_product_size(self, size):
        self.PRODUCT_SIZE = size