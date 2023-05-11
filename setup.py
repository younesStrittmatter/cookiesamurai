from setuptools import setup, find_packages

setup(
    name="cookiesamurai",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'cookiesamurai = cookiesamurai.main:main',
        ],
    },
)