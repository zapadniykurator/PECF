from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = [
    "requests>=2.25.0",
]

def get_package_files(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                files.append(os.path.join(root, filename))
    return files

setup(
    name="PECF",
    version="2.0",
    author="Zedikon",
    author_email="mrzedikon@gmail.com",
    description="New easy and usefull configuration language.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="",
    packages=['core', 'core.tools'],  
    package_dir={
        'core': 'core',
        'core.tools': 'core/tools'
    },
    package_data={
        'core': ['*.py'],
        'core.tools': ['*.py'],
    },
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)