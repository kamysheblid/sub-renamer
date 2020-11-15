import setuptools

setuptools.setup(
    name = "sub-renamer",
    version = "0.0.1",
    license = 'LICENSE',
    author = "Kamy Sheblid",
    author_email = "kamysheblid@gmail.com",
    description = "Automatically rename subtitles filenames to their matching video filenames.",
    long_description = open('README.html').read(),
    long_description_content_type = "text/html",
    url = "https://github.com/kamysheblid/sub-renamer",
    packages = setuptools.find_packages(),
    # packages = ['episode'],
    classifiers = [
        "Topic::Utilies",],
    python_requires = '>=3.7',
    scripts = ['sub-renamer.py'],
    install_requires = [
        'python-Levenshtein'],
    )
