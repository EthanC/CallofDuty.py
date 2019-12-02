import re

import setuptools

version = ""
readme = ""
requirements = []

with open("callofduty/__init__.py") as file:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Version is not set")

with open("README.md") as file:
    readme = file.read()

setuptools.setup(
    name="CallofDuty.py",
    author="EthanC",
    url="https://github.com/EthanC/CallofDuty.py",
    project_urls={
        "Documentation": "https://google.com/",
        "Issue Tracker": "https://github.com/EthanC/CallofDuty.py/issues",
    },
    version=version,
    packages=setuptools.find_packages(),
    license="MIT",
    description="CallofDuty.py is an asynchronous, object-oriented Python wrapper for the Call of Duty API.",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=["aiohttp"],
    python_requires=">=3.7.3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
