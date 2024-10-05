from typer.testing import CliRunner

from mov_cli.cli_v2.main import app

runner = CliRunner()

# NOTE: We'll do more proper tests later.

def test_app():
    result = runner.invoke(app, [])

    assert result.exit_code == 0