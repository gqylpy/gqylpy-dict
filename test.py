from gqylpy_dict import gdict

x = {'a': [{'b': 'B'}]}
x = gdict(x)

print(x.a[0].b)
print(x.deepget('a[0].b'))
