import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class GenerateTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        shutil.copy(os.path.join(REPO, "generate.py"), self.dir)
        shutil.copy(os.path.join(REPO, "theme.yaml"), self.dir)
        shutil.copytree(os.path.join(REPO, "templates"), os.path.join(self.dir, "templates"))

    def tearDown(self):
        shutil.rmtree(self.dir)

    def generate(self):
        return subprocess.run(
            [sys.executable, "generate.py"], cwd=self.dir, capture_output=True, text=True
        )

    def test_renders_all_enabled_apps(self):
        result = self.generate()
        self.assertEqual(result.returncode, 0, result.stderr)
        with open(os.path.join(self.dir, "theme.yaml")) as f:
            theme = yaml.safe_load(f)
        for app in theme["enabled_for"]:
            self.assertTrue(
                os.path.isdir(os.path.join(self.dir, "output", app, theme["name"])), app
            )

    def test_removes_stale_output(self):
        stale = os.path.join(self.dir, "output", "stale.txt")
        os.makedirs(os.path.dirname(stale))
        open(stale, "w").close()
        self.assertEqual(self.generate().returncode, 0)
        self.assertFalse(os.path.exists(stale))

    def test_fails_on_undefined_variable(self):
        with open(os.path.join(self.dir, "templates", "tmux", "broken.j2"), "w") as f:
            f.write("{{ yelow }}")
        result = self.generate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("yelow", result.stderr)


if __name__ == "__main__":
    unittest.main()
