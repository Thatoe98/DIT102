class Clothes:
    def __init__(self, brand, color, texture):
        self.__brand = brand
        self.color = color
        self.texture = texture

    def get_brand (self):
        return self.__brand
    
    def change_brand(self, brand):
        self.__brand = brand


dressing = Clothes("Sketchers", "Black", "Silk")

print (dressing.color)
print (dressing.texture)
print (dressing.get_brand())

dressing.color = "White"
dressing.change_brand("Armani")
print (dressing.color)
print (dressing.texture)
print (dressing.get_brand())