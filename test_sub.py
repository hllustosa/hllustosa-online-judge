while True:
        try:
            [v1, v2] = [int(val) for val in input().split() ]
            print("%d" % (v1 + v2))
        except EOFError:
            break