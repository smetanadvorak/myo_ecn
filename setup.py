from setuptools import setup, find_packages

setup(
name='myo_ecn',
python_requres='>=3',
install_requires=['numpy', 'scikit-learn', 'scipy', 'matplotlib', 'keyboard', 'pyserial'],
version='1.0',
packages=find_packages())
