#!/usr/bin/env python3
import sys
import subprocess
import click


@click.group()
def cli():
    """AI CLI Tool — Interact with Ollama models."""
    pass


@cli.command("models")
def list_models():
    """List all Ollama models installed locally."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True
        )
        click.echo(result.stdout)
    except FileNotFoundError:
        click.echo("Error: Ollama CLI not found.", err=True)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error retrieving models: {e.stderr}", err=True)
        sys.exit(1)


@cli.command("chat")
@click.argument("model")
@click.argument("prompt")
def run_model(model, prompt):
    """Run a given model with a prompt and stream the output."""
    try:
        process = subprocess.Popen(
            ["ollama", "run", model, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        # Stream output line-by-line
        for line in process.stdout:
            click.echo(line.strip())

        process.wait()

        if process.returncode != 0:
            err_output = process.stderr.read()
            if err_output:
                click.echo(f"Error: Model execution failed.\n{err_output}", err=True)
            sys.exit(process.returncode)

    except FileNotFoundError:
        click.echo("Error: Ollama CLI not found.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
