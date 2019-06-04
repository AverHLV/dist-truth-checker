# Welcome to Truth checking distributed service documentation

Truth checker distributed service, it`s a set of services that calculates some parameters of news articles
in order to determine their veracity. It uses a couple of machine learning and NLP algorithms for text researching.

## Services
- [aggregator](aggregator.md): language detection, saving text in raw format, correctness checking and sending
async requests;
- [topic modeling](topic_modeling.md): modeling of topic distribution via Latent Dirichlet Allocation and computing
similarity coefficient between headline and article text;
- [SEO analysis](seo_analysis.md): computing most popular SEO processing metrics and their evaluation via
Mamdani fuzzy control system.

## Language support
- aggregator: english, russian, ukrainian;
- topic modeling: english, russian, ukrainian;
- SEO analysis: any.