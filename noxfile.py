"""
Can be run in container with
 docker run --rm -it --user $(id -u):$(id -g) --mount type=bind,source=$(pwd),target=$(pwd) --workdir $(pwd) --platform linux/amd64 --entrypoint bash mambaorg/micromamba:debian12
"""

import nox
import subprocess
from contextlib import contextmanager

nox.options.default_venv_backend = "micromamba"


@contextmanager
def ensure_temp_version(session):
    try:
        # Get current HEAD commit
        head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        # Create temporary tag at HEAD
        session.run('git', 'tag', '-f', 'v0.0.0.dev0', head, external=True)
        yield
    finally:
        # Clean up temporary tag
        session.run('git', 'tag', '-d', 'v0.0.0.dev0', external=True, success_codes=[0, 1])


@nox.session(python="3.11", reuse_venv=True)
def test(session):
    session.conda_install("--file", "test-environment.yml", channel=["conda-forge", "bioconda"])
    session.conda_install("git")
    with ensure_temp_version(session):
        session.install("-e", ".")
        session.run("pip", "freeze")
        test_files = [
            "tests/tests.py",
            "tests/test_expand.py",
            "tests/test_io.py",
            "tests/test_schema.py",
            "tests/test_linting.py",
            "tests/test_executor_test_suite.py",
            "tests/test_api.py",
        ]
        #env={"CI": "true"}
        session.run("pytest", "-v", "-x", *test_files)

