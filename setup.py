from setuptools import setup

setup(
    name="lif_visualizer",
    version="0.1.1",
    author="Dominik Werman",
    author_email="dominik.werman@4am-robotics.com",
    description="The LIF visualizer allows for the simple and quick visualisation of Layout Interchange Files using NetworkX.",
    long_description=open("README.md").read(),
    url="https://github.com/Odin-byte/lif_visualization/",
    license="Apache 2.0",
    packages=[
        "lif_visualizer",
    ],
    install_requires=[
        "matplotlib",
        "networkx"
    ],
    entry_points={
        "console_scripts": [
            "lif_visualizer = lif_visualizer.visualizer:main",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Programming Language :: Python",
    ],
)