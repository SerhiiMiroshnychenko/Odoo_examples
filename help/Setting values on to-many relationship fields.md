__Setting values on to-many relationship fields__

For one-to-many and many-to-many ﬁelds, instead of a
single ID, a list of related IDs is expected. Furthermore,
several operations can be performed – we may want to
replace the current list of related records with a new
one, or append a few records to it, or even unlink some
records.

To support write operations on to-many ﬁelds, we can
use a special syntax in the `eval` attribute. To write to a
to-many ﬁeld, we can use a list of triples. Each triple is awrite command that does diﬀerent things based on the
code that was used in the ﬁrst element.
To overwrite the list of authors of a book, we would use
the following code:
```
<field name="author_ids"
eval="[(6, 0,
[ref('res_partner_alexandre'),
ref('res_partner_holger')]
)]"
/>
```
To append a linked record to the current list of the
authors of a book, we would use the following code:
```
<field name="author_ids"
eval="[(4, ref('res_partner_daniel'))]"
/>
```
The preceding examples are the most common. In both
cases, we used just one command, but we could chain
several commands in the outer list. The `append (4)` and
`replace (6)` commands are the most used. In the case of
`append (4)`, the last value of the triple is not used and is
not needed, so it can be omitted, as we did in the
preceding code sample.
The complete list of available `to-many write commands`
is as follows:

`(0, _ , {'ﬁeld': value})` creates a new record and links
it to this one.

`(1, id, {'ﬁeld': value})` updates the values on an
already linked record.

`(2, id, _)` removes the link to and deletes the id-
related record.

`(3, id, _)` removes the link to, but does not delete, the
id-related record. This is usually what you will use to
delete related records on many-to-many ﬁelds.

`(4, id, _)` links an already existing record. This can
only be used for many-to-many ﬁelds.

`(5, _, _)` removes all the links, without deleting the
linked records.

`(6, _, [ids])` replaces the list of linked records with
the provided list.

The `_` underscore symbol that was used in the preceding
list represents irrelevant values, usually ﬁlled with `0` or
`False`.
TIP
The trailing irrelevant values can be safely omitted. For example, `(4,
id, _)` can be used as `(4, id)`.

In this section, we learned how to use the `<record>` tag
to load records into the database. As an alternative,
there are a few shortcut tags that can be used in place of
a regular `<record>` tag. The next section will introduce
these to us.