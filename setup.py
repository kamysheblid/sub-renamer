import setuptools

with open("README.html","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "sub-renamer-kamysheblid",
    version = "0.0.1",
    author = "Kamy Sheblid",
    author_email = "kamysheblid@gmail.com",
    description = "Automatically rename subtitles filenames to their matching video filenames."
    long_description = long_description,
    long_description_content_type = "text/html",
    url = "https://github.com/kamysheblid/sub-renamer",
    packages = setuptools.find_packages(),
    classifiers = [
        "Topic::Utilies",],
    python_requires = '>=3.7',
    )
