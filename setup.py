import setuptools
import gqylpy_dict as g

with open(g.__file__, encoding='utf8') as f:
    for line in f:
        if line.startswith('@version: ', 4):
            version = line.split()[-1]
            break
    author, email = f.readline().split(maxsplit=1)[-1].rstrip().split()
    source = f.readline().split()[-1]

setuptools.setup(
    name=g.__package__,
    version=version,
    author=author,
    author_email=email,
    license='WTFPL,Apache-2.0',
    url='http://gqylpy.com',
    project_urls={'Source': source},
    description='基于内置 dict，它是对内置 dict 的增强。dict 能做的它能做，dict 不能做'
                '的它更能做。',
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    packages=[g.__package__],
    python_requires='>=3.8, <4',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)
