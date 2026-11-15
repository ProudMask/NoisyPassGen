# NoisyPassGen

A small password-generator portfolio example using Python's operating-system-backed `secrets` module. The original ambient-noise idea is retained as a separate, explicitly insecure synthetic demonstration of why direct sample-to-character mapping is not a dependable password-generation method.

## Run

Python 3.10 or later; no third-party packages or microphone required:

```bash
python main.py --length 20
python main.py --length 24 --no-symbols --count 3
python -m unittest discover -s tests -v
```

Normal mode prints one generated value per line to standard output. It does not save, upload, log, or copy passwords to the clipboard. Standard output can still be captured by your terminal or shell, so choose the execution environment accordingly. Do not commit generated values to Git.

## Generation contract

Each character is independently selected with secrets.choice from ASCII letters, digits, and optionally a documented punctuation subset. Default length is 20; accepted lengths are 12–128, with 1–20 generated values per invocation. These bounds are application choices, not a universal password-policy recommendation. `--no-symbols` selects letters and digits only. No seed or deterministic password mode is exposed.

The symbol alphabet is `!@#$%^&*()-_=+[]{}:,.?`. Every draw uses the full selected alphabet; the generator does not guarantee that each character category appears, guarantee uniqueness, or enforce a destination site's policy.

```python
from main import generate_password

value = generate_password(length=20, include_symbols=True)
```

Importing the module performs no recording, printing, or generation.

## What changed from the noise prototype

The original code recorded five seconds of microphone audio at import and mapped each sample modulo an alphabet length, producing approximately 220500 characters. Quiet or repeated samples can produce repeated characters. Neither recording length nor output length establishes usable secret entropy.

The normal generator now uses OS randomness and has no audio dependency. The old generate_password_from_noise entry point is removed rather than retaining a misleading password-generation API. To inspect the old mapping concept without recording:

```bash
python main.py --noise-demo --length 20
```

This maps synthetic zero-valued samples to repeated `a` characters and labels the output as insecure. `noise_to_text_demo(samples)` is deterministic and is never used by generate_password. It performs no audio capture.

## Verification and scope

Tests cover output length/alphabet, bounded input validation, use of secrets.choice, deterministic zero-noise behavior, CLI behavior, and silent imports without audio modules. Tests do not claim to prove cryptographic security or estimate entropy from output samples. This project is not a password manager, storage/encryption system, audio entropy extractor, or ML model.

Reference: [Python secrets documentation](https://docs.python.org/3/library/secrets.html).
