import setuptools

with open ("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OpenSeesPySubStepping",
    version="0.1",
    author="iammix",
    author_email="k.mixios@gmail.com",
    description="Sub-stepping methods for LoadControl and Displacement Control analyses",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7.9',
)