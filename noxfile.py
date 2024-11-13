import nox


nox.options.default_venv_backend = "micromamba"


@nox.session(python="3.11", reuse_venv=True)
def test(session):
    session.conda_install("--file", "test-environment.yml", channel=["conda-forge", "bioconda"])
    session.install(".")
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
    session.run("pytest", "-v", "-x", *test_files)
