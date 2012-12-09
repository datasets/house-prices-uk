from setuptools import setup, find_packages

setup(
    name='uk_house_prices',
    version='0.1',
    # Name of License for your project
    # Suitable open licenses can be found at http://www.opendefinition.org/licenses/
    license='PDDL',

    # Title or one-line description of the package
    description='UK House Price Data',

    # URL of project/package homepage
    url='http://www.openeconomics.net/store/view/uk-house-prices',

    # Download url for this package if it has a specific location
    download_url='http://www.openeconomics.net/store/view/uk-house-prices/data',

    # Space-separated keywords/tags
    keywords='house, price, uk, country-uk, format-csv',

    # Notes or multi-line description for your project (in markdown)
    long_description='''

### Extras ###

source: Nationwide <http://www.nationwide.co.uk/hpi/historical.htm>
''',
    author='rgrp',
    author_email='',

    # Ignore from here onwards
    package_dir={'house_prices': ''},
    packages=find_packages(),
    include_package_data=True,
    # do not zip up the package into an 'Egg'
    zip_safe=False,
)
