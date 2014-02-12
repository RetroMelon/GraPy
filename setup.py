from setuptools import setup

dependencies = ["pygame"]

setup(name='grapy',
      version='0.1',
      description='A simple force directed graph library',
      url='http://github.com/RetroMelon/GraPy',
      author='Joe Frew',
      author_email='2089249F@students.gla.ac.uk',
      license='MIT',
      packages=['grapy'],
      dependencies = dependencies
      zip_safe=False)
