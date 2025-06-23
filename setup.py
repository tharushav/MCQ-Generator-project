from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.0.1',
    author='Tharusha Vihanga',
    author_email='tharushavihanga2003@gmail.com',
    install_requires=['langchain' ,'huggingface_hub', 'streamlit', 'python-dotenv', 'PyPDF2', 'langchain_huggingface'],
    packages=find_packages()
)