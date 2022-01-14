import setuptools

setuptools.setup(
    name='PyKIPass',
    version='1.1.0',
    license='MIT',
    author='alus20x',
    author_email='alus20x@gmail.com',
    description='Python wrapper for KIPass',
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding='UTF8').read(),
    url='https://github.com/alus20x/PyKIPass',
    packages=setuptools.find_packages()
)
