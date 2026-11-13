# AI assistant and tool-use review

Use when an assistant retrieves content, handles organizational data, or invokes tools. This is an architectural review guide, not a model benchmark or deployed guardrail.

## Execution boundary

Inventory user instructions, retrieved documents, model outputs, tool descriptions, credentials, memory, and downstream actions. Identify which component authorizes side effects.

A model output is a proposal or data value; the application must still determine whether the action is authorized.

| Area | Decision required | Evaluation evidence |
| --- | --- | --- |
| Retrieved content | How are untrusted instructions separated from authorized tasks? | Hostile instructions embedded in otherwise relevant retrieved text |
| Tool authority | Which actions/resources are permitted per identity? | Allowed action succeeds; out-of-scope resource/action denied at tool layer |
| Sensitive output | Where can protected information be sent? | Synthetic sensitive markers and destination restrictions |
| Human approval | Is approval bound to exact action parameters? | Parameter change after approval requires another authorization decision |
| Memory | Who may write, read, and delete persistent state? | Cross-user isolation, revocation, retention, and corrupted-memory cases |
| Evaluation | Which benign behavior must remain successful? | Paired adversarial/benign cases, denominators, and failure analysis |

## Measurement

Record tasks, system version, model identifier if applicable, tool configuration, repetitions, and outcomes. Separate task success, blocked unauthorized action, false refusal, and inconclusive results. Do not collapse them into an unqualified secure score.

A text classifier rejecting suspicious input does not prove that the action boundary enforces authority. Test the final tool decision as well as the model response.

Keep detailed attack cases in [threat-modeling](https://github.com/secsar/threat-modeling) and authority/state properties in [security-modeling](https://github.com/secsar/security-modeling). This guide makes no live AI calls or effectiveness claims.
