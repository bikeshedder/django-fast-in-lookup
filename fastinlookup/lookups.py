from django.db.models import Lookup
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignObject


@Field.register_lookup
class EffLookup(Lookup):
    lookup_name = "ineff"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return f'{lhs} IN (SELECT unnest({rhs}))', params


@ForeignObject.register_lookup
class ForeignEffInLookup(Lookup):
    lookup_name = "ineff"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return f'{lhs} IN (SELECT unnest({rhs}))', params
