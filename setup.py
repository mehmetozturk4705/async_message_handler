import pathlib
from setuptools import setup

# The directory containing this file
BASE_PATH = pathlib.Path(__file__).parent

# The text of the README file
README = (BASE_PATH / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="async-message-handler",
    version="0.0.1",
    description="Asynchronous message handler between Process/Thread and asyncio event loop.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mehmetozturk4705/async_message_handler",
    author="Mehmet Öztürk",
    author_email="mehmetozturk4705@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "Inteded Audience :: Developers"
    ],
    packages=["asynchronous_message_handler"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
        ]
    },
)