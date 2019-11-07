from setuptools import setup

common_kwargs = dict(
    version='0.1.5',
    license='MIT',
    install_requires=["geojson==2.5.0",
                      "requests==2.22.0",
                      "Shapely==1.6.2.post1"],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
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
        'Programming Language :: Python :: 3.6'
    ],
    python_requires='>3.6',
    include_package_data=True,
)

setup(name='nuts_finder',
      packages=['nuts_finder'],
      **common_kwargs)
