import argparse

parser = argparse.ArgumentParser( description = "Factorial of a number" )
parser.add_argument("-n", help="number to find factorial", type=int)
parser.add_argument("-a", help="name", type=str)
args = parser.parse_args()

#x = input("Enter a number: ")
x = args.n
def factorial(x):
    if x == 1:
        return 1
    else:
        return x * factorial(x-1)
print(f"hello {args.a}, the answer is:")    
print(factorial(int(x)))