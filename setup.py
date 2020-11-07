import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-heiko",
    version="0.0.1",
    author="Pranav Kesavarapu",
    author_email="pranavkesavarapu@gmail.com",
    description="A fancy load balancer for light weight devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/psiayn/heiko",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'asyncssh>=2.4.0',
        'PyYAML>=5.3.0'
    ],
    python_requires='>=3.7',
    entry_points = {
        'console_scripts': ['heiko=heiko.cli:cli'],
    }
)
