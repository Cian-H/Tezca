"""Tezca - The Serpent's Venerable Enemy.

A library designed to selectively disable certain features of the python programming
language. The module provides objects that can be used to compose `Ruleset`s, that can then be
invoked to restrict or change the behaviour of the interpreter.
"""

__all__ = ["Rule", "RuleEngine", "monitor_repl"]

from .engine import RuleEngine
from .hooks import monitor_repl
from .rule import Rule
