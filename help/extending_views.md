__Extending views__

Views are deﬁned using XML and are stored in the
architecture ﬁeld, __arch__. To extend a view, we must locate
the node where the extension will take place, and then
perform the intended change, such as adding XML
elements.

Odoo provides a simpliﬁed notation to extend XML by
using the XML tag we want to match – __<ﬁeld>__, for
example – with one or more distinctive attributes to
match, such as __name__. Then, we must add the __position__
attribute to declare the kind of modiﬁcation to make.

Any XML element and attribute can be used to select the
node to use as the extension point, except for __string__
attributes. The values of string attributes are translated
into the user's active language during view generation,
so they can't be reliably used as node selectors.

The extension operation to perform is declared with the
__position__ attribute. Several operations are allowed, as
follows:

`inside` (the default): Appends the content inside the
selected node. The node should be a container, such
as `<group>` or `<page>`.

`after`: Adds the content after the selected node.

`before`: Adds the content before the selected node.

`replace`: Replaces the selected node. If it's used with
empty content, it deletes the element. Since Odoo 10,
it also allows you to wrap an element with other
markups by using `$0` in the content to represent the
element being replaced; for example, ```<ﬁeld
name="name" position="replace"><h1>$0</h1>
</ﬁeld>```.

`attributes`: Modiﬁes the attribute values for the
matched element. The content should have one or
more ```<attribute name="attr-
name">value<attribute>``` elements, such as
```<attribute name="invisible">True></attribute>```.
If it's used with no body, such as in ```<attribute
name="invisible"/>```, the attribute is removed from
the selected element.

__TIP__
While `position="replace"` allows us to delete XML elements, this
should be avoided. It can break based on modules that may be
using the deleted node as an extension point to add other
elements. As an alternative, consider leaving the element and
making it invisible instead.

__Moving XML nodes to a different location__

Except for the `attributes` operation, the preceding
locators can be combined with a child element with
`position="move"`. The eﬀect is to move the child locator
target node to the parent locator's target position.

Here is an example of moving __my_ﬁeld__ from its current
location to the position after target_ﬁeld:
````
<field name="target_field" position="after">
<field name="my_field" position="move"/>
</field>
````
The other view types, such as list and search views, also
have an __arch__ ﬁeld and can be extended in the same way
as form views can.
