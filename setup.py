from setuptools import setup, find_packages

setup(
    name = "gen3-augur",
    author = "Yilin Xu",
    author_email = "yilinxu@uchicago.edu",
    version = 0.1, 
    description = "Utility tools for data accessing from gen3 and data processing with augur",
    license = "Apache 2.0",
    packages = find_packages(),
    python_requires='>=3.5',
    entry_points= ''' 
        [console_scripts]
        gen3-augur=gen3-augur.__main__:main
    ''', 
)
