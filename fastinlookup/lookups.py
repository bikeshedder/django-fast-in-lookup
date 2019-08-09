from django.db.models import Lookup
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignObject


@Field.register_lookup
class IneffLookup(Lookup):
    lookup_name = "ineff"

    def get_prep_lookup(self):
        pl = super().get_prep_lookup()
        print(pl)
        return pl

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return f'{lhs} IN (SELECT unnest({rhs}))', params


@ForeignObject.register_lookup
class ForeignIneffLookup(Lookup):
    lookup_name = "ineff"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return f'{lhs} IN (SELECT unnest({rhs}))', params
