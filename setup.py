from lemon_markets import __version__
from setuptools import setup, find_packages

if __name__ == '__main__':
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setup(
        name='lemon_markets_sdk',
        version=__version__,
        description='SDK for Lemon Markets API',
        long_description=long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        python_requires='>=3.6',
        author='Linus Reuter',
        url="https://github.com/LinusReuter/lemon-markets-api-access",
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'requests',
        ],
    )
