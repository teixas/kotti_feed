import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

tests_require = [
    'WebTest',
    'pytest-cov',
    'pytest',
    'wsgi_intercept',
    'zope.testbrowser',
]

setup(name='kotti_feed',
      version='0.2',
      description="Add RSS feed generation to your Kotti site",
      long_description='\n\n'.join([README, CHANGES]),
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
      url='https://github.com/teixas/kotti_feed',
      keywords='rss kotti cms pylons pyramid',
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['kotti>=1.0', 'PyRSS2Gen'] + tests_require,
      )
