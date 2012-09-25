import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

tests_require = [
    'WebTest',
    'pytest-cov',
    'pytest',
    'wsgi_intercept',
    'zope.testbrowser',
    ]

setup(name='kotti_feed',
      version='0.1',
      description="Add RSS feed generation to your Kotti site",
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
        ],
      author='Kotti developers',
      author_email='kotti@googlegroups.com',
      url='http://pypi.python.org/pypi/kotti_feed',
      keywords='rss kotti cms pylons pyramid',
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['kotti>=0.7', 'PyRSS2Gen'] + tests_require,
      )
