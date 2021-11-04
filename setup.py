from setuptools import setup, find_packages

if __name__ == '__main__':
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

    setup(
        name='lemon_markets',
        version="0.0.0",  # has to be double quotes for bash to work
        description='SDK for the Lemon Markets API',
        long_description=long_description,
        long_description_content_type='text/markdown',
        license='MIT',
        python_requires='>=3.7',
        author='Linus Reuter',
        url='https://github.com/LinusReuter/lemon_markets_sdk.git',
        packages=find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        install_requires=[
            'pandas',
            'pytz',
            'requests'
        ],
    )
