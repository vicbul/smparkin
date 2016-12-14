import ast

one = [{'a':1},{'b':'c'}]
two = ['a']

text = '{"m2m:cin":{"a":1}}'

x = ast.literal_eval(text[text.find('{"'):])
print x.keys()[0]