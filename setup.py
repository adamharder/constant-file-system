#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="cfs",
    description="A micro-filesystem for storing a collection of files and metadata in a single flat file where any file in the collection can be fetched in constant time. Inspired by the Constant Database (CDB).",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    keywords=["CFS", "filesystem"],
    license="MIT",
    version="0.1",
    packages=find_packages(
        include=[
            "cfs",
        ]
    ),
    url="https://github.com/adamharder/constant-file-system",
    project_urls={
        "Changes": "https://github.com/adamharder/constant-file-system/releases",
        "Code": "https://github.com/adamharder/constant-file-system",
        "Issue tracker": "https://github.com/adamharder/constant-file-system/issues",
    },
    author="GrepBox Inc.",
    author_email="",
    python_requires=">=3.6",
    install_requires=[
        "deprecated>=1.2.3",
        "packaging>=20.4",
        'importlib-metadata >= 1.0; python_version < "3.8"',
    ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    extras_require={
    },
)