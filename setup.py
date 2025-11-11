"""
Setup configuration for Legrand AI TODO application.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='legrand-todo',
    version='1.0.0',
    author='Martyn Legrand',
    author_email='martynlegrand@example.com',
    description='A simple, efficient command-line TODO list manager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MartynLegrand/Legrand_AI',
    packages=find_packages(exclude=['tests', 'tests.*', 'docs']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        # No external dependencies required
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pylint>=2.15.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'legrand-todo=todo_app.cli:main',
        ],
    },
    include_package_data=True,
    keywords='todo task-manager cli productivity',
    project_urls={
        'Bug Reports': 'https://github.com/MartynLegrand/Legrand_AI/issues',
        'Source': 'https://github.com/MartynLegrand/Legrand_AI',
        'Documentation': 'https://github.com/MartynLegrand/Legrand_AI/blob/main/README.md',
    },
)
