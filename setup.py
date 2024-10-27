from setuptools import setup, find_packages

setup(
    name="frontend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "panel>=1.3.0",
        "param>=2.0.0",
        "bokeh>=3.0.0"
    ]
)
