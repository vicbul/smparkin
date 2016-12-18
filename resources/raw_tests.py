import ast

one = [{'a':1},{'b':'c'}]
two = ['a']

text = '{"m2m:cin":{"a":1}}'

class test():
    a = 1
    def __init__(self):
        print self.a

class test2(test):
    test.a = 2
    def __init__(self):
        print self.a

one = test()
two = test2()

print one,two