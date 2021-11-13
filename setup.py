import setuptools
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

#long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
 
    name='pybacen',  # Required
    version='1.1.1',  # Required
    description='Economic analysis in the Brazilian scenario',  # Optional
    #long_description=long_description,
    author='Rafael Pereira de Castro',  # Optional
    author_email='rafael.castro07@outlook.com',  # Optional

    license = 'MIT',
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='bacen, pybacen, series bacen',  # Optional

    packages = setuptools.find_packages(),

    python_requires='>=3.6, <4',


    install_requires=['pandas', 'requests', 'plotly'],  # Optional

)