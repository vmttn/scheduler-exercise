from setuptools import find_packages, setup

setup(
    name="scheduler",
    packages=find_packages("src"),
    package_dir={"": "src"},
)
