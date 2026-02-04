"""A module defining custom types for tezca."""

import ast
from collections.abc import Callable

type Action = Callable[[ast.AST], None]
type Predicate = Callable[[ast.AST], bool]
