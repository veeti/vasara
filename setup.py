from setuptools import setup

setup(
    name="vasara",
    version="0.1dev",
    license="MIT",
    packages=["vasara"],
    test_suite="vasara.tests",

    install_requires=[],
    tests_require=[],

    entry_points={
        "console_scripts": [
            "vsra = vasara.cli:main",
        ]
    }
)