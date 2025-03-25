import pytest

pytest_plugins = "pytest_pulp_cli"


@pytest.fixture
def pulp_cli_vars(pulp_cli_vars: t.MutableMapping[str, str]) -> t.MutableMapping[str, str]:
    # If PULP_FIXTURES_URL is needed in the future, uncomment this assignment
    # PULP_FIXTURES_URL = os.environ.get("PULP_FIXTURES_URL", "https://fixtures.pulpproject.org/")
    result: t.MutableMapping[str, str] = {}
    result.update(pulp_cli_vars)

    return result
