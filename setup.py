
from setuptools import setup, find_packages

setup(
    name="stock-price-predictor",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "matplotlib",
        "yfinance",
    ],
    entry_points={
        "console_scripts": [
            "spp=src.main:main",
        ],
    },
)
