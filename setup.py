import setuptools

with open("README.md", "r",encoding='utf-8') as f:
    long_description = f.read()

__version__ ="0.0.0"
REPO_NAME="TextSummarizer"
AUTHOR_USER_NAME = "nishahariii"
SRC_REPO ="textSummarizer"
AUTHOR_EMAIL="nishahariii@gmail.com"

setuptools.setup(
    name= SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    AUTHOR_EMAIL= AUTHOR_EMAIL,
    description="Rxt Summarization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker":"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues/"
    }
)