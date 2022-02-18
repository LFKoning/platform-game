"""Package Setup File."""
import setuptools

with open("README.md") as readme_file:
    README = readme_file.read()

with open("HISTORY.md") as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = [
    "pygame==2.1.2",
]
TEST_REQUIREMENTS = ["pytest", "pytest-cov"]
EXTRAS_REQUIRE = {
    "dev": ["pylint", "black"] + TEST_REQUIREMENTS,
}

setuptools.setup(
    name="the_game",
    version="0.0.1",
    description="The Game.",
    long_description=README + "\n\n" + HISTORY,
    keywords="game, gaming, side-scroller",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    author="Lukas Koning",
    author_email="lfkoning@gmail.com",
    url="",
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE,
    package_dir={"": "src"},
    test_suite="tests",
    packages=setuptools.find_packages("src"),
    entry_points={
        "console_scripts": [
            "game = the_game.main:run",
        ],
    },
)
