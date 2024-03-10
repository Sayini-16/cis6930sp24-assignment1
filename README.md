## Assignment 1 - CIS 6930 Spring 2024 

## Author: Anirudh Sayini

## The Censoror

## Introduction

Whenever sensitive information is shared with the public, the data must go through a redaction process. That is, all sensitive names, places, and other sensitive information must be hidden. 
Documents such as police reports, court transcripts, and hospital records all contain sensitive information. Censoring this information is often expensive and time consuming.


## Running Instructions

1. **Environment Setup:**
   Ensure you have `pipenv` installed. If not, install it using pip:
   ```bash
   pip install pipenv
   ```
   
2. **Dependencies:**
   Before running the script, install the necessary dependencies using:
   ```bash
   pipenv install
   ```

3. **Execution:**
   To run the script on files, use the following command format:
   ```bash
   pipenv run python censoror.py --input '<input_pattern>' \
                                 --names --dates --phones --address \
                                 --output '<output_directory>/' \
                                 --stats stderr
   ```
   Replace `<input_pattern>` with the pattern matching the files you wish to process (e.g., '*.txt' for all text files) and `<output_directory>` with the path to the directory where you want to store the output files.

   Example command to process all `.txt` files:
   ```bash
   pipenv run python censoror.py --input '*.txt' \
                                 --names --dates --phones --address \
                                 --output 'files/' \
                                 --stats stderr
   ```

## Description of the project:

The project involves creating a data censoring system that automatically detects and redacts sensitive information, such as names, dates, phone numbers, and addresses, from text documents. This system will process multiple files, allow users to specify what types of data to censor, and generate a report on the redaction process. The goal is to provide an efficient and scalable solution for protecting sensitive information in various documents, using command-line interface for operation, and leveraging natural language processing tools.

## Packages Required for Project:

- pytest
- nltk
- spacy
- en_core_web_lg = {file = "https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.7.1-py3-none-any.whl"}

## Parameters

### `--input`
- This parameter accepts a glob pattern representing the text files to be processed.
- Multiple `--input` flags can be used to specify different groups of files.
- An error message will be displayed if a file cannot be read or processed for redaction.

### `--output`
- Specifies the directory where all censored files will be stored.
- Censored files are saved as text files, with the original file name plus the `.censored` extension.

## Censor Flags
These flags determine the types of sensitive information to be redacted:

- `--names`: Detects and redacts any type of name. The definition of a name is determined by the implementation.
- `--dates`: Identifies and censors dates in various formats (e.g., 4/9/2025, April 9th, 22/2/22).
- `--phones`: Targets and redacts phone numbers in their various forms.
- `--address`: Redacts physical (postal) addresses.

Feel free to add your own flags to extend the functionality. The redacted characters should be replaced with a character of your choice, such as the Unicode full block character █ (U+2588). The decision to censor whitespace between phrases or words should be discussed in this document.

### `--stats`
- Specifies the output location for the summary of the redaction process, supporting file names or special files (`stderr`, `stdout`).
- The summary includes types and counts of censored terms, along with specific statistics for each processed file.
- Optionally, the summary can include the beginning and end index of each censored item.

The projects have below files: 
**1. main.py**
**2. censoror.py**

## 1. main.py
 
This main.py utilizes NLTK and spaCy libraries to identify and redact personal information from text data. It processes text to find names, dates, addresses, and phone numbers, then replaces them with blocks for redaction. It also generates a summary of the redactions performed. The script demonstrates the integration of regular expressions, spaCy's NLP capabilities, and NLTK's text processing features for data anonymization.

### Functions

### `names(text)`
The `names` function extracts and returns a list of unique names identified as 'PERSON' entities in the provided text data using spaCy's natural language processing capabilities. It processes the text, identifies named entities, filters them by the 'PERSON' label, and appends each unique name to a list, which is then returned along with the original data.

![SS6](https://github.com/Sayini-16/cis6930sp24-assignment1/assets/81869410/5d3a2639-2cf0-487a-bf43-e0c500b413f8)

### `dates(text)`
Identifies and extracts date expressions from the text. This function is capable of recognizing various date formats and normalizing them for consistent processing.

![SS6](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/main_dates.png)

### `addresses(text)`
Detects and extracts physical address details from the text. The function looks for patterns that typically represent postal addresses to ensure that location data is redacted.

![SS6](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/main_address.png)

### `phones(text)`
Finds and extracts phone numbers from the text. It can handle multiple phone number formats, making it robust against the varied ways phone numbers can be presented.

![SS6](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/main_phone.png)

### `redact(names_list, dates, address_list, phone_numbers, text)`
The redaction function takes lists of names, dates, addresses, and phone numbers along with the original text. It then redacts all occurrences of these sensitive pieces of information from the text.

![SS6](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/main_redact.png)

### `stats(stats_path, file_name, entities)`
Generates a statistical summary of the redaction process. This function logs details such as the count and types of terms redacted and can output this information to a file or stdout/stderr as defined by the user.

![SS6](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/main_stats.png)


## 2. censoror.py

![SS1](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/censoror.png)

## Description
The `censoror.py` script is a command-line utility that forms the core of the data censoring system. It is designed to read in text files, apply specified redaction rules to censor sensitive information like names, dates, addresses, and phone numbers, and then output the redacted files to a designated directory.

## Usage
To use the script, you must provide command-line arguments to define the input files, output directory, and what types of data to censor. The flags used for specifying these parameters include `--input`, `--output`, and `--stats`.

### Command-Line Arguments
- `--input`: Specifies the glob pattern for the input text files to be processed.
- `--output`: Defines the directory where the redacted files will be saved. If the directory doesn't exist, it will be created.
- `--stats`: Designates a file or output stream to receive the redaction process statistics.

Additional flags are used to indicate which types of sensitive information should be redacted. The script supports redacting names, dates, addresses, and phone numbers.

## Bugs & Assumptions

- **Bugs:**
  - Ensure the `main.py` functions correctly identify and redact all instances of personal information. There may be edge cases where data is not detected or redacted.

- **Assumptions:**
  - The script assumes that the input files are encoded in UTF-8. Files with different encodings might not be processed correctly.
  - The redaction functions in `main.py` are assumed to be reliable and accurate. However, they may not cover all formats or variations of personal information.

---

## Pytest framework for the project :
I used the Pytest framework in Python to check for the individual test cases. To run the pytest framework, we need to first ensure if we have the pytest installed in our current project directory. I used the following command to install the pytest in my project's execution virtual environment.
~~~
pipenv install pytest
~~~

## 3.test_assignment1.py

Below are imported for this file
- pytest
- project1
<br>

## Testing with Pytest

Our project employs Pytest, a powerful testing framework for Python, to ensure the correctness and reliability of its functionalities. The tests cover key aspects of the application, from data fetching and processing to database operations and status reporting. Here's an overview of the tests included:

### Test Suite Overview

1. **`test_extract_dates`**: This test verifies that the `dates` function in the `main` module correctly extracts date entities from the provided text. The test checks if the number of dates extracted matches the expected count.

![SS6](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/dates.png)

2. **`test_extract_names`**: This test checks the `names` function in the `main` module to ensure it accurately identifies and extracts names from the text. It asserts that the length of the returned name list is as expected.

![SS6](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/names.png)

3. **`test_extract_phone`**: This function tests the `phones` function in the `main` module, ensuring it can extract phone numbers from the text. The test validates that the count of extracted phone numbers aligns with the anticipated number.

![SS6](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/phones.png)

4. **`test_extract_address`**: This test ensures that the `addresses` function in the `main` module effectively identifies and extracts addresses from the text. It checks if the number of addresses extracted is correct.

![SS6](https://github.com/sadam456/cis6930sp24-assignment1/blob/main/docs/address.png)


### Running the Tests

To run the tests, ensure you have Pytest installed in your development environment. Navigate to the root directory of the project and execute the following command:

```sh
pytest
```

Pytest will automatically discover and run all tests defined in the project, reporting their outcomes. Successful test execution indicates that the project's key functionalities are performing correctly under the tested conditions.


## To run the Pytest : 
I used the following command to run my python tests for the given function.
~~~
 pipenv run python -m pytest
~~~
