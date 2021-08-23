fact = int(input("Calculate factorial of: "))
fact_new = 1

for j in range(1, fact+1):
    fact_new *= j
    print(fact_new)

print("Factorial of: ", fact, " is: ", fact_new)
