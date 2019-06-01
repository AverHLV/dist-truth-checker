# Topic modeling service

Modeling text topics using Latent Dirichlet Allocation.

## Models

### Text

- fields:
    - created: text creation date;
    - true_similarity: float, LDA computed similarity between article headline and text;
    - false similarity: float, LDA computed similarity between article text and a reference article with a rare topic.
    - language: string of length 2 with a language code;
    - headline: article headline cleared by checker.CorrChecker;
    - cleared_text: article text cleared by checker.CorrChecker;
    - message_id: unique text identifier, integer in hex form, length 32.

## Submodules

### lda

Implements the interface for the corpora (collections of texts) and LDA model. The LDA algorithm implements clustering
of texts for a predetermined number of clusters-topics. For each cluster, a set of keywords is formed, which is based
on the Dirichlet distribution. The computation of the similarity of the texts is carried out on the basis of the
constructed vectors of text distribution by keywords with a help of Jensen-Shannon distance.

Fitted models overview:

|   Model   | Number of topics | Log Likelihood | Perplexity |
|:---------:|:----------------:|:--------------:|------------|
|  English  |        10        |  -30888501.372 | 3381.247   |
|  Russian  |        10        |  -6091576.967  | 3118.759   |
| Ukrainian |        10        |  -6587708.423  | 2348.799   |