from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

common_kwargs = dict(
    version='0.1',
    license='MIT',
    install_requires=required,
    long_description=open('README.md').read(),
    url='https://github.com/nestauk/nuts_finder',
    author='Joel Klinger',
    author_email='joel.klinger@nesta.org.uk',
    maintainer='Joel Klinger',
    maintainer_email='joel.klinger@nesta.org.uk',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Environment :: Web Environment'
        'Topic :: System :: Monitoring',
    ],
    python_requires='>3.6',
    include_package_data=True,
)

setup(name='nuts_finder',
      packages=['nuts_finder'],
      **common_kwargs)

