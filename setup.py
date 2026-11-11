from setuptools import setup, find_packages

setup(
    name="markanm",
    version="0.1.0a3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=["httpx>=0.24.0"],
)
