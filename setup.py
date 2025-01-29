import setuptools

# Read the README file
with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

# Read the LICENSE file
with open('LICENSE', 'r') as license_file:
    license_content = license_file.read()

setuptools.setup(
    name='json_to_csv',
    version='1.0.0',
    description='A command-line tool to convert JSON to CSV with the same filename.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify that the README is in Markdown
    author='Alec J. Davidson',
    author_email='alecjdavidson@outlook.com',
    url='https://github.com/AlecJDavidson/json_to_csv',
    packages=setuptools.find_packages(),
    install_requires=[
        'argparse',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license=license_content,
    include_package_data=True,
    extras_require={
        'tests': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'json_to_csv=json_to_csv.converter:main',
        ]
    },
    setup_requires=[
        'setuptools_scm',  # Ensure setuptools_scm is installed
    ],
)
