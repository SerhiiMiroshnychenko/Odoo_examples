**SQL model constraints**

SQL constraints are added to the database table
deﬁnition and are enforced directly by PostgreSQL. They
are declared using the `_sql_constraints` class attribute.

It is a list of tuples, and each tuple has a format of
`(name, sql, message)`:

`name` is the constraint identiﬁer name.

`sql` is the PostgreSQL syntax for the constraint.

`message` is the error message to present to users
when the constraint is not veriﬁed.

The most used SQL constraints are `UNIQUE` constraints,
which are used to prevent data duplication, and `CHECK`
constraints, which are used to test a SQL expression on
the data.

```python
_sql_constraints = [
        ("library_book_name_date_uq",
         "UNIQUE (name, date_published)",
         "Book title and publication date must be unique."),
        ("library_book_check_date",
         "CHECK (date_published <= current_date)",
         "Publication date must not be in the future."),
    ]
```