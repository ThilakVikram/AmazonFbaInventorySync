def parser(co):
    # print(*range(10,0,-1))
    for i in range(co,0,-1):
        if i == 3:
            print("After restart")
            parser(co)
            # yield i
        else:
            yield i
# print([parser(0)])
for i in parser(10):
    print(len([*parser(10)]))
    print(f"i + {i}")