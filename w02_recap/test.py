# greet = lambda x : "Hello " + x

# print (greet ("Thatoe"))

# square = lambda x : x ** 2

# print (square(2))
# print (square(5))
# print (square(6))

def factorial (n):
    result = 1
    for i in range (n):
        result *= i+1
    return result

print (factorial(4))
print (factorial(6))