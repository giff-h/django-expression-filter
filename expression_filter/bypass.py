from typing import Any, List, Sequence

from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Expression, Value
from django.db.models.expressions import BaseExpression
from django.db.models.sql.compiler import SQLCompiler


class AnnotationBypass(Expression):
    conditional = True

    def __init__(self, expression: BaseExpression, compare: str, value: Any) -> None:
        super().__init__()
        self.expression = expression
        self.compare = compare
        self.value = value if hasattr(value, 'resolve_expression') else Value(value)

    def get_source_expressions(self) -> List[Any]:
        return [self.expression, self.value]

    def set_source_expressions(self, exprs: Sequence[Any]) -> None:
        self.expression, self.value = exprs

    def as_sql(self, compiler: SQLCompiler, connection: BaseDatabaseWrapper) -> Any:
        field = self.expression.output_field
        lookup_class = field.get_lookup(self.compare)
        return lookup_class(self.expression, self.value).as_sql(compiler, connection)
