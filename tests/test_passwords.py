import subprocess
import sys
import unittest
from unittest.mock import patch
from main import ALPHANUMERIC, SYMBOLS, generate_password, noise_to_text_demo


class PasswordTests(unittest.TestCase):
    def test_length_and_alphabet(self):
        for length in (12, 20, 128):
            value = generate_password(length)
            self.assertEqual(len(value), length)
            self.assertTrue(set(value) <= set(ALPHANUMERIC + SYMBOLS))
        self.assertTrue(set(generate_password(128, False)) <= set(ALPHANUMERIC))

    @patch('main.secrets.choice', return_value='A')
    def test_os_randomness_path(self, choice):
        self.assertEqual(generate_password(20), 'A' * 20)
        self.assertEqual(choice.call_count, 20)
        self.assertEqual(choice.call_args.args[0], ALPHANUMERIC + SYMBOLS)

    def test_invalid_parameters(self):
        for length in (0, 11, 129, 20.5, True):
            with self.assertRaises(ValueError):
                generate_password(length)
        with self.assertRaises(ValueError):
            generate_password(20, 'yes')

    def test_noise_mapping_is_demonstrably_predictable(self):
        self.assertEqual(noise_to_text_demo([0] * 20), 'a' * 20)
        self.assertEqual(noise_to_text_demo([0, 62]), 'aa')
        with self.assertRaises(ValueError):
            noise_to_text_demo([1.5])

    def test_cli(self):
        result = subprocess.run([sys.executable, 'main.py', '--length', '24', '--count', '2', '--no-symbols'], capture_output=True, text=True, check=True, timeout=10)
        lines = result.stdout.splitlines()
        self.assertEqual([len(line) for line in lines], [24, 24])
        self.assertTrue(all(set(line) <= set(ALPHANUMERIC) for line in lines))
        demo = subprocess.run([sys.executable, 'main.py', '--noise-demo'], capture_output=True, text=True, check=True, timeout=10)
        self.assertIn('INSECURE', demo.stdout)
        invalid = subprocess.run([sys.executable, 'main.py', '--length', '0'], capture_output=True, text=True, timeout=10)
        self.assertNotEqual(invalid.returncode, 0)

    def test_import_without_audio(self):
        result = subprocess.run([sys.executable, '-c', "import main, sys; assert 'sounddevice' not in sys.modules; assert 'numpy' not in sys.modules"], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
