import setuptools

setuptools.setup(
        name="cs",
        author="Egor Martynov",
        packages=["cs"],
        entry_points={"console_scripts": ["cs=cs.__main__.main"]})
