# SEO analysis service

Modeling text topics using Latent Dirichlet Allocation.

## Models

### Text

- fields:
    - created: text creation date;
    - fuzzy_mark: float, fuzzy control system output;
    - language: string of length 2 with a language code;
    - headline: article headline cleared by checker.CorrChecker;
    - cleared_text: article text cleared by checker.CorrChecker;
    - message_id: unique text identifier, integer in hex form, length 32.

## Submodules

### fuzzy_system

Implements an interface of the fuzzy output system based on the Mamdani algorithm.

Input variables:
- ns_classic: classic text nausea;
- ns_academic: academic text nausea.

For all fuzzy variables, triangular membership functions with three terms are used,
the boundaries of the functions are built with the expert estimates of the required
value for the selected parameter.

System rules:
 - if ns_classic is bad or ns_academic is bad then mark is bad;
 - if ns_classic is average and ns_academic is average then mark is average;
 - if ns_classic is good and ns_academic is average then mark is average;
 - if ns_classic is average and ns_academic is good then mark is average;
 - if ns_classic is good and ns_academic is good then mark is good.