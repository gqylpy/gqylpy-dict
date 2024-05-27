import setuptools
import gqylpy_dict as g

gdoc: list = g.__doc__.split('\n')

for index, line in enumerate(gdoc):
    if line.startswith('@version: ', 4):
        version = line.split()[-1]
        break
_, author, email = gdoc[index + 1].split()
source = gdoc[index + 2].split()[-1]

setuptools.setup(
    name=g.__package__,
    version=version,
    author=author,
    author_email=email,
    license='WTFPL,Apache-2.0',
    url='http://gqylpy.com',
    project_urls={'Source': source},
    description='''
        `gqylpy-dict` is based on the built-in `dict` and serves as an
        enhancement to it. It can do everything the built-in `dict` can do, and
        even more.
    '''.strip().replace('\n       ', ''),
    long_description=open('README.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    packages=[g.__package__],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Artistic Software',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13'
    ]
)
