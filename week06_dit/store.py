from product import Product

class Store:
    def __init__(self):
        self.products = []

    def add_product(self, name,price):
        product = Product(name, price)
        self.products.append(product)

    def get_average(self):
        total = sum(p.price for p in self.products)
        return total / len(self.products)
    
    def update_product_by_name (self, name, new_price):
        for product in self.products:
            if product.name == name:
                product.price = new_price
                break
    
    def delete_product_by_name(self, name):
        for product in self.products:
            if product.name == name:
                self.products.remove(product)
                break

    