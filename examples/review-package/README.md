# Synthetic review package

R-01 has a matching record and local fixture. R-02 has only a planned observation. R-03 has a proposed decision and planned evidence.

Expected result: **incomplete, 1/3 supported required items**.

```bash
python -m tools.review examples/review-package/package.json
```

Run from the repository root. The fixture's pass is declared sample data; no deployed service was assessed. Its file digest is real, but matching the digest does not establish the claim's truth.

To explore a failure, copy this directory to a temporary location, modify the fixture without updating its digest, then run the tool on the copy. E-01 reports an artifact digest mismatch.

Do not replace public fixtures with customer evidence, private logs, credentials, or internal architecture.
