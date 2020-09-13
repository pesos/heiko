import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyheiko", # Replace with your own username
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
    python_requires='>=3.7',
    entry_points = {
        'console_scripts': ['heiko=heiko.cli:cli'],
    }
)
