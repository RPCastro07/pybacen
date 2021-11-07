import setuptools
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
 
    name='pybacen',  # Required
    version='1.0.7',  # Required
    description='Dados de series temporais disponibilizados pelo Bacen',  # Optional
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


    install_requires=['pandas'],  # Optional

)