from django.db.models import Aggregate, CharField, Value
from django.conf import settings


# class GroupConcat(Aggregate):
#    function = "GROUP_CONCAT"
#    template = ""
#    # allow_distinct = True
#
#    def __init__(self, expression=None, delimiter=None, distinct=False, **extra):
#        db_engine = settings.DATABASES["default"]["ENGINE"]
#        if db_engine == "django.db.backends.sqlite3":
#            self.as_sqlite3(expression, delimiter, **extra)
#        elif db_engine == "django.db.backends.mysql":
#            self.as_mysql(expression, distinct=distinct, separator=delimiter, **extra)
#        elif db_engine == "django.db.backends.postgresql":
#            return self.as_postgresql(extra.pop("compiler"), extra.pop("connection"))
#        else:
#            raise NotImplementedError(
#                f"DB Engine {db_engine!r} not supported for {self.function!r}"
#            )
#
#    def as_mysql(self, expression, distinct, separator=",", **extra):
#        template = '%(function)s(%(distinct)s%(expressions)s%(ordering)s%(separator)s)'
#        super(GroupConcat, self).__init__(
#            expression,
#            distinct='DISTINCT ' if distinct else '',
#            ordering=' ORDER BY %s' % ordering if ordering is not None else '',
#            separator=' SEPARATOR "%s"' % separator,
#            output_field=CharField(),
#            **extra
#        )
#
#        #self.template = "%(function)s(%(distinct)s%(expressions)s%(separator)s)"
#        #output_field = extra.pop("output_field", CharField())
#        #distinct = "DISTINCT " if distinct else ""
#        #separator = " SEPARATOR '{}'".format(separator) if separator is not None else ""
#        #super().__init__(
#        #    expression,
#        #    separator=separator,
#        #    # distinct=distinct,
#        #    output_field=output_field,
#        #    **extra,
#        #)
#
#    def as_sqlite3(self, expression, delimiter, **extra):
#        self.template = "%(function)s(%(expressions)s)"
#        output_field = extra.pop("output_field", CharField())
#        delimiter = Value(delimiter)
#        super().__init__(expression, delimiter, output_field=output_field, **extra)
#
#    def as_postgresql(self, compiler, connection):
#        self.function = "STRING_AGG"
#        return super().as_sql(compiler, connection)
#
