`ondelete`: This deﬁnes what happens when the
related record is deleted. The possible behaviors are
as follows:

`set null` (the default): An empty value is set when the
related record is deleted.

`restricted`: This raises an error, preventing the
deletion.

`cascade`: This will also delete this record when the
related record is deleted.

`context`: This is a dictionary of data that's meaningful
for the web client views to carry information when
navigating through the relationship, such as to set
default values. 

`domain`: This is a domain expression – a list of tuples
used to ﬁlter the records made available for selection
on the relationship ﬁeld. 

`auto_join=True`: This allows the ORM to use SQL
joins when doing searches using this relationship. If
used, the access security rules will be bypassed, and
the user could have access to related records that the
security rules would not allow, but the SQL queries
will run faster.

`delegate=True`: This creates a delegation inheritance
with the related model. When used, the
`required=True` and `ondelete="cascade"` attributes
must also be set. 
