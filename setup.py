import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="habitica-helper",
    version="1.2",
    author="Anni Järvenpää",
    author_email="anni.jarvenpaa@gmail.com",
    description="A collection of tools for automating Habitica tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aajarven/habitica-helper.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "click",
        "requests",
        "yfinance",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        ],
)
