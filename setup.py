import pathlib

from setuptools import find_packages, setup

BASE_DIR = pathlib.Path(__file__).parent

README = (BASE_DIR / "README.md").read_text()

setup(
    name="onesocial_django",
    version="1.0.0",
    description="Приложение Django для входа через соцсети с помощью OneSocial API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/onesocial-dev/onesocial-django",
    author="Oleg Yamnikov",
    author_email="oyam@oxymeal.ru",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=['personal', 'personal.*', 'example', 'example.*']),
    include_package_data=True,
    install_requires=[
        "Django>=2.0",
        "onesocial>=1.0.0",
    ],
)
