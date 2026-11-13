# Modelo Security
### Security architecture • Modeling • Assurance

Public resources for connecting security requirements, design decisions, and evidence.

[Website](https://modelosecurity.com) · [Security modeling](https://github.com/secsar/security-modeling) · [Threat modeling](https://github.com/secsar/threat-modeling)

## Start here

| Resource | What it helps you do |
| --- | --- |
| [Security review guide](guides/security-review.md) | Organize an architecture review around decisions and evidence |
| [Architecture decision template](templates/security-decision.md) | Explain a security decision, alternatives, and tradeoffs |
| [Evidence register](templates/evidence-register.csv) | Track what supports each security claim |
| [Worked decision example](examples/document-access-decision.md) | See how a fictional design decision connects to validation |

## How the repositories fit together

| Repository | Focus |
| --- | --- |
| **modelosecurity** | Public resources, review guidance, and practical decision records |
| [security-modeling](https://github.com/secsar/security-modeling) | Policies, permissions, information flow, state transitions, and security properties |
| [threat-modeling](https://github.com/secsar/threat-modeling) | Threat scenarios, attack paths, prioritization, and mitigation analysis |

Each repository owns its detailed artifacts. References connect related work without duplicating specifications or threat registers.

## Working approach

**Define the requirement. Explain the decision. Identify the evidence. State the limits.**

A useful security review makes the intended behavior clear, identifies who is responsible for enforcing it, and records how the implementation will be evaluated. Conclusions should distinguish design intent from observed results.

## About these resources

This repository contains educational guidance and fictional examples. It does not contain a production platform or customer implementation. Example controls and tests are not claims of completed assessments, certification, or measured effectiveness.

For information about Modelo Security, visit [modelosecurity.com](https://modelosecurity.com).

## Contributing

Corrections and focused improvements are welcome. Read the [contribution guidance](CONTRIBUTING.md) and [public-content review checklist](docs/public-content-review.md) before submitting material.
