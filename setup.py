import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sonatypeliftlib",
    version="0.0.3",
    author="Mark Dodgson",
    author_email="mark.dodgson@googlemail.com",
    license='MIT',
    description="Helper methods to allow easier interfacing to the V1 Api of Sonatype Lift",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doddi/sonatypeliftlib",
    packages=setuptools.find_packages(include=['sonatypeliftlib']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='sonatype lift',
    project_urls={
        'Homepage': 'https://github.com/doddi/sonatypeliftlib',
    },
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
