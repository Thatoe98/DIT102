'''
Thatoe Nyi
ID- 6708351
Class- DIT 102
'''

class Juice:
    def __init__(self, name, color, flavor, price):
        self.name = name
        self.color = color
        self.flavor = flavor
        self.price = price
        
    
    def show_info (self):
        print (f"{self.name} juice have {self.color} color and {self.flavor} flavor.")
        print (f"The price is {self.price} baht.\n")

def main():
    orange_juice = Juice("orange", "orange", "sour", 30)
    coconut_juice = Juice ("coconut", "clear", "sweet and fresh", 50)
    lychee_juice = Juice ("lychee", "white", "sweet and sour", 40)

    orange_juice.show_info()
    coconut_juice.show_info()
    lychee_juice.show_info()

if __name__ == "__main__":
    main()