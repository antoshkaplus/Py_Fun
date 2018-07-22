from setuptools import setup

setup(name='antoshkaplus',
      version='1.0',
      description='finance support functions',
      url='http://github.com/storborg/funniest',
      author='Anton Logunov',
      author_email='antonlogunov91@gmail.com',
      license='MIT',
      packages=['antoshkaplus.finance', 'antoshkaplus.numtech',
                'antoshkaplus.stats', 'antoshkaplus.optimize'],
      zip_safe=False)
