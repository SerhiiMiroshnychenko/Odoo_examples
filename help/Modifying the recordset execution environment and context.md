**Modifying the recordset execution
environment and context**

The recordset execution context can be modiﬁed to take
advantage of the behaviors described in the previous
section or to add information to be used in methods
called on that recordset.
Контекст виконання набору записів можна змінити, 
щоб скористатися перевагами поведінки або додати інформацію
для використання в методах, викликаних у цьому наборі записів.

The environment and its context can be modiﬁed through
the following methods. Each of these returns a new
recordset, along with a copy of the original with a
modiﬁed environment:
Середовище та його контекст можна змінити за допомогою
наступних методів. Кожен із них повертає новий набір
записів разом із копією оригіналу зі зміненим середовищем:

The `<recordset>.with_context(<dictionary>)`
method replaces the context with the one provided in
the dictionary.
метод замінює контекст тим, що надається у словнику.

The `<recordset>.with_context(key=value, ...)`
method modiﬁes the context by setting the provided
attributes on it.
метод змінює контекст, встановлюючи для нього надані атрибути.

The `<recordset>.sudo([ﬂag=True])` method
enables or disables the superuser mode, allowing it to
bypass security rules. The context user is kept the
same.
метод вмикає або вимикає режим суперкористувача,
дозволяючи йому обходити правила безпеки.
Користувач контексту залишається незмінним.

The `<recordset>.with_user(<user>)` method
modiﬁes the user to the one provided, which is either
a user record or an ID number.
метод змінює користувача на наданого, 
який є записом користувача або ідентифікаційним номером.

The `<recordset>.with_company(<company>)`
method modiﬁes the company to the one provided,
which is either a company record or an ID number.
метод змінює компанію на надану,
яка є або записом компанії, або ідентифікаційним номером.

The `<recordset>.with_env(<env>)` method modiﬁes
the full environment of the recordset to the one
provided.
метод змінює повне середовище набору записів на надане.

Additionally, the environment object provides the
`env.ref()` function, taking a string with an external
identiﬁer and returning the corresponding record, as
shown in the following example:

```sh
>>> self.env.ref('base.user_root')
res.users(1,)
```
If the external identiﬁer does not exist, a ValueError
exception is raised.
