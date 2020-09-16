from setuptools import setup, find_packages

setup(
    name='TNS Scraper',
    author='Paul-Julien Burg',
    url='https://github.com/paul-julien/TNSscrape',
    version='1.0',
    packages=find_packages(),
    install_requires=['beautifulsoup4','gensim','xmltodict','pandas','datetime','GoogleNews','argparse','email']



)
