import setuptools

setuptools.setup(
    name = "sub-renamer",
    version = "0.0.1",
    license = 'LICENSE',
    author = "Kamy Sheblid",
    author_email = "kamysheblid@gmail.com",
    description = "Automatically rename subtitles filenames to their matching video filenames.",
    long_description = open('README.org').read(),
    long_description_content_type = "text/plain",
    url = "https://github.com/kamysheblid/sub-renamer",
    packages = setuptools.find_packages(),
    classifiers = [
        "Topic::Utilies",],
    python_requires = '>=3.7',
    scripts = ['sub-renamer.py'],
    extra_requires = [
        'python-Levenshtein'],
    )
