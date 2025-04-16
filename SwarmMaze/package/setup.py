# setup.py
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swarmaze",  # The name you'll use on PyPI
    version="0.1.0",
    author="Seyed Masoud Hashemi Ahmadi",
    author_email="you@example.com",  # or omit
    description="A pathfinding visualizer for 2D mazes using Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ETS-Hashemi/projects/swarmaze",
    project_urls={
        "Bug Tracker": "https://github.com/ETS-Hashemi/projects/swarmaze/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pygame",
        # Other dependencies if needed
    ],
    entry_points={
        "console_scripts": [
            # This will let users do: `swarmaze maze.txt [algorithm]`
            "swarmaze = swarmaze.main:main"
        ]
    },
)
