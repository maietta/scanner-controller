# readlineSetup.py

"""
Provides cross-platform readline support with tab-completion.

- On Unix/macOS: uses builtin readline
- On Windows: uses pyreadline3 (if installed)
- If neither is available, disables tab completion
"""


def initialize_readline(COMMANDS):
    """
    Set up tab-completion for available COMMANDS.

    Parameters:
        COMMANDS (dict): Dictionary mapping command strings to their handler
                        functions.
                        The function docstrings are used to extract
                        subcommands.

    Returns:
        None: The function configures readline in-place and doesn't return
              a value.

    Note:
        Command handlers should have docstrings that list their
        subcommands/arguments for proper tab completion of second-level
        commands.
    """
    try:
        import readline  # Unix and macOS
    except ImportError:
        try:
            import pyreadline3 as readline  # Windows with pyreadline3
        except ImportError:
            print(
                "Note: readline or pyreadline3 not available. "
                "Tab-completion disabled."
            )
            return

    def completer(text, state):
        """
        Set up tab-completion for available COMMANDS.

        Dynamically filters commands and subcommands based on input.
        """
        buffer = readline.get_line_buffer().strip()
        parts = buffer.split()

        # If no input or first word, suggest top-level commands
        if len(parts) == 0 or (len(parts) == 1 and not buffer.endswith(" ")):
            matches = [cmd for cmd in COMMANDS if cmd.startswith(text)]

        # If input contains a space, suggest subcommands or arguments
        elif len(parts) >= 1:
            command = parts[0].lower()
            if command in COMMANDS:
                # Get subcommands or arguments for the matched command
                subcommands = (
                    COMMANDS[command].__doc__.split()
                    if COMMANDS[command].__doc__
                    else []
                )
                subcommands = (
                    COMMANDS[command].__doc__.split()
                    if COMMANDS[command].__doc__
                    else []
                )
                matches = [sub for sub in subcommands if sub.startswith(text)]
            else:
                matches = []
        else:
            matches = []

        # Return the match for the current state
        try:
            return matches[state]
        except IndexError:
            return None

    # Configure readline settings
    readline.set_completer(completer)
    readline.parse_and_bind(
        "tab: complete"
    )  # Map tab key to completion function
    readline.set_history_length(100)  # Store last 100 commands in history
