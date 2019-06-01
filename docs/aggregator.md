# Aggregator service

Text management, adding new texts, preprocessing text, sending asynchronous requests to other services,
viewing check results.

## Models

### Text

- fields:
    - created: text creation date;
    - language: string of length 2 with a language code;
    - cleared_headline: article headline cleared by checker.CorrChecker;
    - cleared_text: article text cleared by checker.CorrChecker;
    - message_id: unique text identifier, integer in hex form, length 32;
    - headline: raw article headline;
    - raw_text: raw article text.

- methods:
    - clean: text clearing, correctness checking and language detection.

### TextsAdmin

- fields:
    - token: unique superuser identifier for API authentication.

## Submodules

### arclient

HTTP client for sending asynchronous requests. Sends a GET or POST requests to the specified list of services.
Implements requests timeout, adding custom headers and logging.

### checker

Text correctness checker. Workflow:

- detect language by langdetect, port of Google's language-detection library;
- delete all non-language symbols except spaces;
- check text correctness by entropic criteria;
- stem words by Snowball stemmers;
- delete stopwords.

H1 and H2 values for entropic criteria:

| Language  |  H1  |  H2  |
|:---------:|:----:|:----:|
|  English  | 4.18 | 3.95 |
|  Russian  |  4.5 |  4.2 |
| Ukrainian |  4.6 |  4.2 |