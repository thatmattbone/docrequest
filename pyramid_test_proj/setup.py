import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = """ """
CHANGES = """ """

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'waitress',
    ]

setup(name='pyramid_test_proj',
      version='0.0',
      description='pyramid_test_proj',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="pyramid_test_proj",
      entry_points="""\
      [paste.app_factory]
      main = pyramid_test_proj:main
      """,
      )
