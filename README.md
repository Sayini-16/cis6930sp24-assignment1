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
The `dates` function identifies and collects date entities from the provided text data using spaCy's NLP tools. It scans the text for entities labeled as "DATE" and appends each found date to a list. The function returns the original text data along with the list of extracted date entities.

![SS6](https://github.com/Sayini-16/cis6930sp24-assignment1/assets/81869410/d67752e6-8716-4d63-b171-fe34e208b429)

### `addresses(text)`
The `addresses` function uses spaCy's Matcher to identify and extract potential address entities from the text data. It defines a custom pattern to match sequences that resemble addresses, such as a sequence of digits followed by street names and optional suffixes. The function then searches the text for matches to this pattern, extracts each found address, and adds it to a list. The original text and the list of extracted addresses are returned.

![SS6](https://github.com/Sayini-16/cis6930sp24-assignment1/assets/81869410/a058891b-39f2-4c14-ad54-ff950c7228d2)

### `phones(text)`
The `phones` function extracts phone numbers from the input text using the CommonRegex library, which provides a convenient way to identify common patterns like phone numbers in text. The function parses the input data to find phone number patterns, populating a list with the extracted phone numbers. It returns the original data along with the list of phone numbers found. If the input data is empty, it returns an empty list for phone numbers.

![SS6](https://github.com/Sayini-16/cis6930sp24-assignment1/assets/81869410/419faef9-f2d0-4636-abdb-5ce48063fe43)

### `redact(names_list, dates, address_list, phone_numbers, text)`
The `redact` function anonymizes the text data by replacing identified names, dates, addresses, and phone numbers with a block character. It concatenates all the elements from the provided lists into a single list and iterates over it, using a regular expression to replace each element in the text with a series of block characters equal in length to the element. This process effectively redacts sensitive information from the data, returning the redacted version of the text.

![SS6](https://github.com/Sayini-16/cis6930sp24-assignment1/assets/81869410/8cfe8b0a-1ef6-411f-b273-00e2d5f8d995)

### `stats(stats_path, file_name, entities)`
The `stats` function generates a summary of the redaction process for a specific file. It calculates the total number of redacted items by summing the lengths of the names, dates, addresses, and phone numbers lists. The function then constructs a status report detailing the number of each type of entity redacted from the file. This report includes the total count of redacted items and individual counts for names, dates, addresses, and phone numbers, providing a clear overview of the redaction results.

![SS6](https://github.com/Sayini-16/cis6930sp24-assignment1/assets/81869410/5a63489c-ae08-407c-b47b-6c6dd70a74d8)


## 2. censoror.py

The censor.pyis designed to redact sensitive information from text files based on specified criteria. It processes a set of files, identifies and redacts names, dates, addresses, and phone numbers, and generates a summary of the redaction. Here's a breakdown of its main components:

1. **Initialization:** Clears or creates a stats.txt file to store redaction summaries and initializes various lists to manage arguments and data.
2. **Argument Parsing:** Extracts command line arguments to determine input files, output destination, stats file path, and specific redaction flags (names, dates, addresses, phones).
3. **File Processing:** Iterates over the specified input files, reading and processing each one to identify and redact the specified types of information.
4. **Redaction and Summary:** For each file, it calls the `main` module's functions to detect and redact the specified information types, then updates the stats file with a summary of the actions taken.
5. **Output Generation:** Writes the redacted content to new files in the specified output directory, appending `.censored` to the original filenames.

This script automates the redaction process, ensuring sensitive information is anonymized before further processing or sharing of the text files.
![SS1](https://github.com/Sayini-16/cis6930sp24-assignment1/assets/81869410/6f4dd789-f403-4be1-b4be-9a53db7e7fa4)

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
