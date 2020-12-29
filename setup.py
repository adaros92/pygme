import pathlib

from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    description='Lightweight computer games written in Python',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/adaros92/pygme",
    version='0.2.1',
    install_requires=['curtsies'],
    tests_require=['pytest', 'pytest-cov', 'tox', 'Random-Word'],
    license="MIT",
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
    packages=find_packages(exclude=("test",)),
    name='pygme',
    python_requires='>=3.6',
    package_data={
            'pygme': ['data/*']
        },
    entry_points={
        'console_scripts': [
                'pygme = pygme.__main__:main'
            ]
    }
)
