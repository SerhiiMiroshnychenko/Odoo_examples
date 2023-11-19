__Common field attributes__

The following keyword argument attributes are generally
available to all ﬁeld types:

`string` is the ﬁeld's default label, to be used in the
user interface. Except for `Selection` and relational
ﬁelds, it is available as the ﬁrst positional argument,
so most of the time, it is not used as a keyword
argument. If it's not provided, it is automatically
generated from the ﬁeld name.

`default` sets a default value for the ﬁeld. It can be a
ﬁxed value (such as `default=True` in the `active` ﬁeld),
or a callable reference, either the named function
reference or a `lambda` anonymous function.

`help` provides the text for tooltips that are displayed
to users when hovering the mouse over the ﬁeld in the
UI.

`readonly=True` makes the ﬁeld not editable in the
user interface by default. This is not enforced at the
API level: code in model methods will still be capable
of writing to it, and a view deﬁnition can override this.
It is only a user interface setting.

`required=True` makes the ﬁeld mandatory in the user
interface by default. This is enforced at the database
level by adding a `NOT NULL` constraint to the
database column.

`index=True` adds a database index to the ﬁeld, for
faster search operations at the expense of disk space
usage and slower write operations.

`copy=False` has the ﬁeld ignored when duplicating a
record via the `copy()` ORM method. Field values are
copied by default, except for to-many relational ﬁelds,
which are not copied by default.

`deprecated=True` marks the ﬁeld as deprecated. It
will still work as usual, but any access to it will write a
warning message to the server log.

`groups` allows you to limit the ﬁeld's access and
visibility to only some groups. It expects a comma-
separated list of XML IDs for security groups; for
example,
__groups="base.group_user,base.group_system"__.

`states` expects dictionary mapping values for UI
attributes, depending on the values of the `state` ﬁeld.
The attributes that can be used are `readonly`,
`required`, and `invisible`; for example, __states=
{'done':[('readonly',True)]}__.

*__TIP__
Note that the __states__ ﬁeld attribute is equivalent to the __attrs__
attribute in views. Also, views support a __states__ attribute that has
a diﬀerent use: it is a comma-separated list of states in which the
view element should be visible.*