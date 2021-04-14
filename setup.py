import setuptools

with open ("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OpenSeesPySubStepping",
    version="0.1.0",
    author="Konstantinos Mixios",
    author_email="k.mixios@gmail.com",
    description="Substepping method for LoadControl and Displacement Control Analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7.9',
)