import random as r
from subprocess import run, PIPE


max_n = 10
num_positive_tests = 10000
num_negative_tests = 10000

positive_tests, negative_tests = set(), set()

def is_square(a):
    l = len(a)
    if l % 2 == 1:
        return False
    else:
        return a[: int(l / 2)] == a[int(l / 2): ] 

# generate positive inputs
for i in range(num_positive_tests):
    l = r.randint(0, max_n)
    s = "".join([str(r.randint(1, 2)) for _ in range(l)])

    positive_tests.update({s + s})

# generate negative inputs
for i in range(num_negative_tests):
    l = r.randint(0, max_n * 2)
    s = "".join([str(r.randint(1, 2)) for _ in range(l)])
    if not is_square(s):
        negative_tests.update({s})

print("testing positive")
for test in positive_tests:
    p = run("./interpreter square.tm 10000".split(), stdout=PIPE,
            input=test + '\n', encoding='ascii')
    if not p.stdout == "YES\n":
        print("bad", test)

print("testing negative")
for test in negative_tests:
    p = run("python3 interpreter.py square.tm 10000".split(), stdout=PIPE,
            input=test + '\n', encoding='ascii')

    if not p.stdout == "NO\n":
        print("bad", test)

