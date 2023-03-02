import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quick_rest",
    version="0.1.9",
    author="Michael Everingham",
    author_email="lamerlink@live.com",
    description="A versatile wrapper for REST APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaeleveringham/quick_rest",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests>=2.26.0',
      ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires='>=3.7',
)
