"""
Configuration du package ROI Marketing Calculator
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="roi-marketing-calculator",
    version="1.0.0",
    author="Votre Nom",
    author_email="votre.email@exemple.com",
    description="Calculateur de ROI et métriques marketing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-username/roi-marketing-calculator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Marketing Professionals",
        "Topic :: Office/Business :: Marketing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "roi-calculator=app:main",
        ],
    },
)