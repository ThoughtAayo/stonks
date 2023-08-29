# Getting Started

## ENV File

- create a copy of example.env
- rename the new file to .env
- Add in api keys.

## Install Tesseract

- https://tesseract-ocr.github.io/tessdoc/Installation.html

## Poetry:

- installation link: https://python-poetry.org/
- After poety is setup, run `poetry shell` from root folder
- Run `poetry install` to install project dependencies
- In `.env` file edit `SAMPLE_FILE_PATH` field to point to your sample pdf file
- run `poetry run stonks/app.py` to run the project

## Readings

- [Extracting text from pdf](https://towardsdatascience.com/how-to-extract-text-from-any-pdf-and-image-for-large-language-model-2d17f02875e6)
