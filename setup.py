from setuptools import setup, find_packages

setup(
    name="NaturalSortNoPadding",
    version="1.0.0",
    description="Create videos from image frames without requiring zero-padding",
    author="Ameer Khan",
    author_email="ameerk238@gmail.com",
    url="https://github.com/ameerk238/NaturalSortNoPadding",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "natural-sort-no-padding=frame_to_video:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    python_requires=">=3.6",
)