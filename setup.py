import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="musicalbeeps",
    version="0.1",
    description="Play sound beeps corresponding to musical notes.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Cutwell/musicalbeeps",
    author="Maël Drapier, Zachary Smith",
    author_email="zachsmith.dev@gmail.com",
    license="MIT",
    keywords="music musical note notes beep beeps play player sound frequency",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Players"
    ],
    packages=find_packages(),
    install_requires=["numpy", "simpleaudio"],
)