from setuptools import setup

setup(
   name='TaMERI',
   version='1.0',
   description='Machine learning prediction of transmembrane evolutionary rate ratio',
   author='Dominik Müller',
   author_email='ga37xiy@tum.de',
   packages=['TaMERI'],
   install_requires=['argparse', 'pandas', 'sklearn', 'numpy'],
)
