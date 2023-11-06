__Access security__

Internal system models are listed here:

`res.groups`: groups—relevant ﬁelds: `name`,
`implied_ids`, `users` 

`res.users`: users—relevant ﬁelds: `name`, `groups_id`

`ir.model.access`: Access Control—relevant ﬁelds:
`name`, `model_id`, `group_id`, `perm_read`,
`perm_write`, `perm_create`, `perm_unlink`

`ir.access.rule`: Record Rules—relevant ﬁelds: `name`,
`model_id`, `groups`, `domain_force`

XML IDs for the most relevant security groups are listed
here:

`base.group_user`: __internal user__ — any backend user

`base.group_system`: __Settings__ — the Administrator
belongs to this group

`base.group_no_one`: __technical feature__, usually used
to make features not visible to users

`base.group_public`: __Public__, used to make features
accessible to web anonymous users

XML IDs for the default users provided by Odoo are
listed here:

`base.user_root`: The root system superuser, also
known as __OdooBot__.

`base.user_admin`: The default user, by default named
__Administrator__.

`base.default_user`: The template used for new
backend users. It is a template and is inactive, but can
be duplicated to create new users.

`base.default_public user`: The template used to
create new portal users.