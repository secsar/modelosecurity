# Public-content review

Review the exact files being published, including metadata, links, images, examples, and commit messages.

## Appropriate content

- Original educational guidance.
- Blank reusable templates.
- Fictional architectures and synthetic records.
- Public references with appropriate attribution.
- Verified results whose publication is authorized.

## Exclude

- Customer or employer records and architecture.
- Private business plans, ownership information, internal project names, or unpublished commercial methods.
- Credentials, tokens, private keys, environment files, private endpoints, and deployment configuration.
- Personal addresses, private contact details, or identifiable logs.
- Claims of certifications, partnerships, patents, service commitments, or measured results without an approved public basis.

## Before publication

1. Verify that each file belongs in this repository.
2. Inspect content and references for confidential information.
3. Confirm that examples are clearly fictional.
4. Check links and consistency between tables and prose.
5. Distinguish plans, assumptions, observed results, and proofs.
6. Review the diff and commit message.
7. Confirm that the final published version matches the reviewed content.

Removing sensitive text in a later commit does not remove it from earlier history. If a secret is exposed, revoke or rotate it and address the publication separately. Avoid committing it in the first place.

