import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "PYPI_README.md").read_text()

setup(
    name="MusicalNotes",
    version="0.1.1",
    description="Play sound beeps corresponding to musical notes.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MaelDrapier/MusicalNotes",
    author="Maël Drapier",
    author_email="mael.drapier@gmail.com",
    keywords="music musical note notes play player sound frequency",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Players"
    ],
    packages=find_packages(),
    install_requires=["pyaudio", "numpy"],
    entry_points={
        "console_scripts": [
            "musicalnotes=musicalnotes.script:main",
        ]
    },
)