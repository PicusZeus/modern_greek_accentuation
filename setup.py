from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="modern-greek-accentuation",
    version="0.2.4",
    description="Python 3 library for accenting, analyzing accentuation, "
                "syllabification, augmentation and transcription of Modern Greek words",
    long_description_content_type="text/markdown",
    long_description=long_description,

    license="MIT",
    url="http://github.com/PicusZeus/modern-greek-accentuation",
    author="Krzysztof Hilman",
    author_email="krzysztof.hilman@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    python_requires='>+3.6'
)
