import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="new_private_subnets_in_existing_vpc",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "new_private_subnets_in_existing_vpc"},
    packages=setuptools.find_packages(where="new_private_subnets_in_existing_vpc"),

    install_requires=[
        "aws-cdk.core==1.117.0",
        "aws-cdk.aws_ec2",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
