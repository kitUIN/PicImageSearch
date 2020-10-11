import setuptools
requirements = [
    requirement.strip() for requirement in open('requirements.txt','r',encoding='utf-8').readlines()
]

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="PicImageSearch",
    version="0.5.5",
    author="kitUIN",
    author_email="kulujun@gmail.com",
    description="PicImageSearch APIs for Python 3.x 适用于 Python 3 以图搜源整合API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kitUIN/PicImageSearch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],install_requires=requirements,
    python_requires='>=3.6',
)