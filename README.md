# ALEA Data Generator

[![PyPI version](https://badge.fury.io/py/alea-data-generator.svg)](https://badge.fury.io/py/alea-data-generator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/alea-data-generator.svg)](https://pypi.org/project/alea-data-generator/)

This is a basic synthetic data generation/perturbation library designed to support the creation or augmentation
designed by the ALEA Institute to support the creation and augmentation of data without relying on "tainted" LLMs.

Data generation techniques in this library:
 * do not require the use of any LLM or external data source
 * can be used with [KL3M](https://kl3m.ai), our Fairly Trained LLM

### Supported Patterns

The following data generation patterns are supported:

 * [x] Simple string templates with sampled values (e.g., `This Agreement, by and between <|company:a|> and <|company:b|>, is made as of <|date|>.`)
   - [x] Faker integration for common data types (e.g., names, addresses, dates, etc.)
 * [x] Large templates with sampled values (e.g., `jinja2` templates in files)
 * [ ] Common document types (e.g., emails, contracts, memos, etc. using templates)
 * [ ] Data perturbation (e.g., realistic errors introduced by humans, OCR, or other automated systems)
   - [x] Skipping, doubling, or  transposing/swapping characters
   - [x] Skipping, doubling, or  transposing/swapping tokens
   - [x] QWERTY and mobile keyboard mistakes (off-by-one key, shift errors, etc.)
   - [ ] Homophones (e.g., `their` vs. `there`)
   - [ ] Synonyms (e.g., `big` vs. `large`)
   - [ ] Negation/antonyms (e.g., `big` vs. `small`)
   - [ ] Capitalization errors (e.g., `big` vs. `Big`)
   - [ ] Punctuation errors (e.g., `big` vs. `big.`)
   - [ ] OCR-like errors (e.g., misreading characters, smudges, etc.) -
 * [ ] Representation conversion (e.g., `429` to `four hundred twenty-nine` or `four twenty-nine`)
  * [ ] Format conversion (e.g., Markdown <-> HTML variants)


## Future Roadmap

 * Document image generation for document/OCR models

## License

The ALEA Data Generator library is released under the MIT License. See the [LICENSE](LICENSE) file for details.

Some of the data generation techniques used in this library may also retrieve data from external sources,
which have their own licensing terms.  These terms are documented in the `alea-data-sources` here:

 * [alea-data-sources](https://github.com/alea-institute/alea-data-resources)

See, e.g., the CMU Pronouncing Dictionary (`cmudict`), which is used in tasks like homophonic errors:

  * [cmudict metadata](https://github.com/alea-institute/alea-data-resources/blob/v0.1.0/alea_data_resources/sources/cmudict.py#L10)

## Support

If you encounter any issues or have questions about using the ALEA Data Generator library, please [open an issue](https://github.com/alea-institute/alea-data-generator/issues) on GitHub.

## Learn More

To learn more about ALEA and its software and research projects like KL3M and leeky, visit the [ALEA website](https://aleainstitute.ai/).
