# Contributing to Modelo Security resources

Contribute a correction, a clearer explanation, an improved template, or a fictional worked example.

## Scope

This repository contains public guidance and decision resources. Detailed policy specifications belong in [security-modeling](https://github.com/secsar/security-modeling); detailed threat scenarios belong in [threat-modeling](https://github.com/secsar/threat-modeling).

## Submission requirements

- Read the [public-content review checklist](docs/public-content-review.md).
- Use original content, appropriately attributed sources, and synthetic examples.
- Do not submit private business material, proprietary implementation details, credentials, or identifiable customer data.
- Explain the practical question the contribution answers.
- Label assumptions, proposed work, and completed validation accurately.
- Check internal links and consistency with related artifacts.
- Avoid unsupported promotional claims.

A pull request should describe the change, its purpose, and checks performed. Public issues are for documentation feedback; do not include confidential security findings or sensitive records.


## Tooling changes

Run `python -m unittest discover -s tests -v`. Include negative cases for malformed inputs and misleading evidence states. The synthetic package must remain clearly labeled, and tool results must not be described as security certification or production approval.
