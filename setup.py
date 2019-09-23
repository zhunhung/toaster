import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytoaster",
    version="0.0.6",
    author="Zhun Hung",
    author_email="yongzhunhung@gmail.com",
    description="Sends a telegram message to you when your code finish running",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhunhung/toaster/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
 )