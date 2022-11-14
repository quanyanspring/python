

if __name__ == "__main__":
    print((lambda a, b, c, d: (lambda e, f: e + f)((lambda a, b: a + b)(a, b), (lambda c, d: c + d)(c, d)))(1, 2, 3, 4))
