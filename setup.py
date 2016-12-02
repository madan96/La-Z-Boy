from distutils.core import setup

setup(
    # Application name:
    name="La-Z-Boy",

    # Keywords
    keywords='movie ml development',

    # Version number (initial):
    version='0.1.0',

    # Application author details:
    author="Rishabh Madan",
    author_email="rishabhm@iitkgp.ac.in",

    # Packages
    packages=["scrapper"],

    # Include additional files into the package
    include_package_data=True,

    license='MIT',

    # license="LICENSE.txt",
    description="Movie and Entertainment Rating System And Recommender",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "BeautifulSoup",
        "mechanize",
        "fpdf",
        "tabulate"
    ],
)
