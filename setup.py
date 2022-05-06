import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lilly",
    version="0.2.0",
    description="This package provides an opinionated SOA-layered fastapi-based web-framework.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sopherapps/lilly",
    author="Martin Ahindura",
    author_email="team.sopherapps@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    install_requires=["fastapi", "click", "pydantic", "fastapi-utils", "SQLAlchemy"],
    entry_points={
    },
)
