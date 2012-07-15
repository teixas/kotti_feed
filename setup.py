import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

tests_require = [
    'pytest-cov',
    'pytest',
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
      author='Nuno Teixeira',
      author_email='teixas@gmail.com',
      url='https://github.com/teixas/kotti_feed',
      keywords='rss kotti cms pylons pyramid',
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['kotti>=0.7dev'] + tests_require,
      )
