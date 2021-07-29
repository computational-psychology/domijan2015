from setuptools import setup, find_packages

setup(
    name="domijan2015",
    version="0.1",
    description="Domijan2015",
    author="Lynn Schmittwilken",
    author_email="l.schmittwilken@tu-berlin.de",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    install_requires=["scipy", "numpy", "matplotlib", "pillow"],
)
