import os
from distutils.core import setup

current_directory = os.path.dirname(os.path.abspath(__file__))

try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name='shikithon',
    version="0.0.2",
    license='MIT',
    description='Yet another Python wrapper for Shikimori API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='SecondThundeR',
    author_email='awayfromgalaxy@gmail.com',
    url='https://github.com/SecondThunder/shikithon',
    project_urls={
        "Bug Tracker": "https://github.com/pypa/shikithon/issues",
    },
    keywords=[
        "Python", "Shikimori", "API"
    ],
    install_requires=[
        "pydantic==1.9.0",
        "requests==2.27.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["shikithon"],
    python_requires=">=3.6",
    include_package_data=True,
)
