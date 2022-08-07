from gqylpy_dict import gdict

print('──── data ────')
data = {'a': [{'b': 'B'}]}
data = gdict(data)
print(data)
print(isinstance(data, dict))

print('──── get ────')
data = gdict({'a': [{'b': 'B'}]})
print(data.a[0].b)
print(data.deepget('a[0].b'))
print(data.deepget('a[0].c', default='C'))

print('──── set ────')
data = gdict({'a': [{'b': 'B'}]})
data.a[0].c = 'C'
data.deepset('a[2].d', 'D')
print(data)

print('──── get and set ────')
data = gdict({'a': [{'b': 'B'}]})
b = data.deepsetdefault('a[0].b', 'X')
c = data.deepsetdefault('a[1].c', 'C')
print(b)
print(c)
print(data)

print('──── contain ────')
data = gdict({'a': [{'b': 'B'}]})
print(data.deepcontain('a[0].b'))
print(data.deepcontain('a[0].c'))

print('──── get (built-in dict) ────')
data = gdict({'a': [{'b': 'B'}]})
print(gdict.getdeep(data, 'a[0].b'))
print(gdict.getdeep(data, 'a[0].c', default='C'))

print('──── set (built-in dict) ────')
data = gdict({'a': [{'b': 'B'}]})
data.setdeep(data, 'a[0].b', 'X')
data.setdeep(data, 'a[2].c', 'C')
print(data)
