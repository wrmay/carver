import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='carver',
    version='0.1',
    author='Randy May',
    description='Utility functions for writing gcode files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # url='https://github.com/wrmay/carver',
    packages=setuptools.find_packages(),
    # license='MIT',
    install_requires=[]
)
