"""Runtime hooks for integrating the Rule Engine with the Python interpreter.

This module provides mechanisms to intercept Python runtime events, such as
compilation, to enforce AST rules dynamically. It is primarily used to
monitor interactive REPL sessions.
"""

import ast
import sys
from typing import Any

from .engine import RuleEngine
from .errors import RuleError
from .rule import Rule
from .utils import recursion_guard


def monitor_repl(rules: list[Rule]) -> None:
    """Registers an audit hook to validate REPL input against the given rules.

    This function attaches a listener to `sys.addaudithook` that filters for
    "compile" events. It specifically targets interactive sessions (where the
    filename is "<stdin>") to ensure that code entered into the REPL adheres
    to the defined constraints before it is compiled and executed.

    The hook is protected by a recursion guard to prevent the validation logic
    itself from triggering infinite audit loops.

    Args:
        rules: A list of Rule objects that will be enforced on every snippet
            of code submitted to the REPL.
    """
    engine = RuleEngine(rules)

    @recursion_guard()
    def hook(event: str, args: tuple[Any, ...]) -> None:
        if event != "compile":
            return
        try:
            source_input = args[0]
            filename = args[1] if len(args) > 1 else "?"
            if filename != "<stdin>":
                return
            tree: ast.AST | None = None
            if isinstance(source_input, ast.AST):
                tree = source_input
            elif isinstance(source_input, (str, bytes)):
                tree = ast.parse(source_input)
            if tree:
                engine.visit(tree)
        except RuleError:
            raise
        except Exception as e:
            raise RuleError(f"REPL Monitor Error: {e}") from e

    sys.addaudithook(hook)
