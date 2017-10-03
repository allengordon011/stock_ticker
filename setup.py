from setuptools import setup

setup(
    name='stock_ticker',
    version='0.1.0',
    description="A simple stock ticker website for building and saving a user-specific list of stocks, and displaying a simple ticker of the list of stocks.",
    long_description=open('README.rst').read(),
    author="Allen Gordon",
    author_email='allengordon011@gmail.com',
    url='https://github.com/allengordon011/stock_ticker',
    packages=['stock_ticker'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    'Flask',
    'flask_sqlalchemy'
    ],
    license="MIT license"
)
