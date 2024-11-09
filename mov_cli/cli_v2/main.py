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
    if ctx.invoked_subcommand is not None:
        return



    print("NOTICE: THIS IS A WORK IN PROGRESS! Not everything will work.")