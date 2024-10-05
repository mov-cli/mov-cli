import typer

__all__ = ()

app = typer.Typer(
    pretty_exceptions_enable = False,
    help = "Watch everything from the terminal."
)

@app.callback(invoke_without_command = True)
def mov_cli(
    ctx: typer.Context
):
    print(
        "Hello, you've reached the mov-cli master command but there's nothing here yet..."
    )