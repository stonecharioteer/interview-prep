"""Interactive prompt helpers using Rich."""

from rich.console import Console
from rich.prompt import IntPrompt, Prompt

console = Console()


def prompt_select_from_list(items: list[tuple[int, str]], prompt_text: str = "Select") -> int:
    """Display numbered list, return selected item's ID.

    Args:
        items: List of (item_id, display_text) tuples
        prompt_text: Text to show in the prompt

    Returns:
        The ID of the selected item
    """
    console.print()
    for i, (item_id, display) in enumerate(items, 1):
        console.print(f"  {i}. [dim]#{item_id}[/dim] {display}")
    console.print()
    while True:
        choice = IntPrompt.ask(prompt_text, console=console)
        if 1 <= choice <= len(items):
            return items[choice - 1][0]
        console.print(f"[red]Enter 1-{len(items)}[/red]")


def prompt_text(prompt_text: str, default: str = None) -> str:
    """Prompt for text input."""
    return Prompt.ask(prompt_text, default=default, console=console)


def prompt_int(prompt_text: str, default: int = None) -> int:
    """Prompt for integer input."""
    return IntPrompt.ask(prompt_text, default=default, console=console)
