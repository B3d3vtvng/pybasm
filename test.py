def foo(x, y):
    if x > y:
        return x
    elif x == y:
        return 0
    else:
        return y

for i in range(10):
    print(foo(i, i+1))

while True:
    if foo(10, 20) == 10:
        break

my_list = [1, 2, 3, 4]
my_str = "Hello, World!"