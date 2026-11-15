"""OS-random password generation plus an explicitly insecure noise-mapping demo."""
import argparse
import secrets
import string

ALPHANUMERIC = string.ascii_letters + string.digits
SYMBOLS = '!@#$%^&*()-_=+[]{}:,.?'


def validate_length(length):
    if isinstance(length, bool) or not isinstance(length, int) or not 12 <= length <= 128:
        raise ValueError('Length must be an integer between 12 and 128')


def generate_password(length=20, include_symbols=True):
    """Draw each character independently using Python's secrets module."""
    validate_length(length)
    if not isinstance(include_symbols, bool):
        raise ValueError('include_symbols must be True or False')
    alphabet = ALPHANUMERIC + (SYMBOLS if include_symbols else '')
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def noise_to_text_demo(samples):
    """Show the old deterministic modulo mapping; never use as a secret generator."""
    samples = list(samples)
    if not 1 <= len(samples) <= 128 or any(isinstance(sample, bool) or not isinstance(sample, int) for sample in samples):
        raise ValueError('Demo samples must contain 1 to 128 integer values')
    return ''.join(ALPHANUMERIC[sample % len(ALPHANUMERIC)] for sample in samples)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--length', type=int, default=20)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--no-symbols', action='store_true')
    parser.add_argument('--noise-demo', action='store_true', help='Show deterministic synthetic zero-sample mapping instead of generating passwords')
    args = parser.parse_args()
    try:
        validate_length(args.length)
        if not 1 <= args.count <= 20:
            raise ValueError('Count must be between 1 and 20')
        if args.noise_demo:
            if args.count != 1 or args.no_symbols:
                raise ValueError('--noise-demo cannot be combined with --count or --no-symbols')
            print('INSECURE DEMONSTRATION — synthetic zero samples, not a password:')
            print(noise_to_text_demo([0] * args.length))
        else:
            for _ in range(args.count):
                print(generate_password(args.length, not args.no_symbols))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
