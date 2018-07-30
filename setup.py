from setuptools import setup, find_packages

setup(name='antoshkaplus',
      version='1.1',
      description='a bunch of helper modules',
      url='https://github.com/antoshkaplus/Py_Modules',
      author='Anton Logunov',
      author_email='antonlogunov91@gmail.com',
      license='MIT',
      packages=find_packages(include=['antoshkaplus.*']),
      zip_safe=False)
