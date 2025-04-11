
from store import Store

store = Store()

store.add_product("Apple", 1.5)
store.add_product("Banana", 2.5)
store.add_product("Orange", 3.5)
store.add_product("Pineapple", 4.5)
#read

for product in store.products:
    print(product)

print(f"Average price: {store.get_average()}")

#update
store.update_product_by_name("Banana", 3.0)
store.update_product_by_name("Orange", 4.0)



#delete
store.delete_product_by_name("Banana")
store.delete_product_by_name("Orange")

for product in store.products:
    print(product)