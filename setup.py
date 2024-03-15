"""Setup script for AuditAgent."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="auditagent",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered smart contract security auditor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AuditAgent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "slither-analyzer>=0.9.0",
        "mythril>=0.23.0",
        "solc-select>=1.0.0",
        "openai>=1.0.0",
        "web3>=6.0.0",
        "py-solc-x>=1.1.0",
        "click>=8.0.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "jinja2>=3.1.0",
        "markdown>=3.4.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "auditagent=examples.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
