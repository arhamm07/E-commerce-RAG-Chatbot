from setuptools import find_packages, setup

setup(
    name="ecommbot",
    version="0.0.1",
    author="Arham Rafique",
    author_email="arhammrafique@gmail.com",
    packages=find_packages(),
    install_requires=['langchain-astradb','langchain ','langchain-openai','datasets','pypdf','python-dotenv','flask']
)