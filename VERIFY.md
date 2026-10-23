# Verify the package offline

From this directory, using Python 3.10 or newer:

```sh
python -B verify_package.py
```

The script checks listed file sizes/SHA256 hashes and local Markdown links. It performs no network calls, target execution or writes. A successful result means the package matches its manifest; it does **not** reproduce the historical assessment or prove a vulnerability.

MANIFEST.json intentionally does not hash itself. No product environment or test account is needed for this offline check.
