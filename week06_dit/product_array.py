from product import Product

products = [Product("Phone", 340.99), Product("PC", 1420.69), Product("Tablet", 450.223), Product("Laptop", 1300.444)]


total = 0
for product in products:
    print(product)
    total += product.price

print(f"Total: {total}")


products.append(Product("Mouse", 20.99))
products.append(Product("Keyboard", 50.99))

total = 0
for product in products:
    print(product)
    total += product.price

print(f"Total: {total}")

for product in products:
    if product.name == "Phone":
        product.price = 300.99
        break
for product in products:
    print(product)


laptop = next((p for p in products if p.name == "Laptop") , None)
if laptop:
    laptop.price = 1200.99
print (products)