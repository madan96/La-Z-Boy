from setuptools import setup

setup(
    # Application name:
    name="lazboy",
    # Keywords
    keywords=['movie', 'recommender', 'ml', 'development', 'Python', 'IMDb', 'Entertainment'],
    # Version number (initial):
    version='1.0.2',

    # Application author details:
    author="Rishabh Madan",
    author_email="rishabhm@iitkgp.ac.in",

    # Packages
    packages=["lazboy"],
    
    license='MIT',
    url = 'https://github.com/madan96/La-Z-Boy',
    # license="LICENSE.txt",
    description="Movie and Entertainment Rating System And Recommender",

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],
    # Dependent packages (distributions)
    install_requires=[
        "BeautifulSoup",
        "mechanize",
        "fpdf",
        "tabulate"
    ],
)
