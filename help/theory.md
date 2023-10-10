ORM Methods : 𝐜𝐡𝐞𝐜𝐤_𝐚𝐜𝐜𝐞𝐬𝐬_𝐫𝐢𝐠𝐡𝐭𝐬() Function

It is a helper function that can be used to verify that the current user is allowed to perform a given operation, like writing to a model.

𝐀𝐫𝐠𝐮𝐦𝐞𝐧𝐭𝐬
⚒ operation : create, read, write, or unlink
⚒ raise_exception: A boolean value that indicates whether an exception should be raised if the operation is forbidden.


𝐄𝐱𝐚𝐦𝐩𝐥𝐞𝐬

self.with_user(4).env['account.move.line'].
𝐜𝐡𝐞𝐜𝐤_𝐚𝐜𝐜𝐞𝐬𝐬_𝐫𝐢𝐠𝐡𝐭𝐬('read', raise_exception=False)
# 𝐓𝐫𝐮𝐞 or 𝐅𝐚𝐥𝐬𝐞 depends on security applied to the user

self.with_user(4).env['account.move.line'].
𝐜𝐡𝐞𝐜𝐤_𝐚𝐜𝐜𝐞𝐬𝐬_𝐫𝐢𝐠𝐡𝐭𝐬('read',raise_exception=True)
# in case there are no access rights for this user,
# you will get 𝐞𝐱𝐜𝐞𝐩𝐭𝐢𝐨𝐧 like below
# You are not allowed to access 'Journal Item' (account.move.line) records


💡 What is the expected Exception if no access rights are granted ?
IF operation == read
# {AccessError} You are not allowed to access...
IF operation == create
# {AccessError} You are not allowed to create...
IF operation == delete
# {AccessError} You are not allowed to delete...
IF operation == write
# {AccessError} You are not allowed to modify...

Feel free to let me know if you need more information about when or how to use this function.