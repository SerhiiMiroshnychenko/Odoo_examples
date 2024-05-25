# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
	'name'			: 'Sale Order History | Customer Reorder Sale',
	'version'		: '16.0.0.0',
	'category'		: 'Sales',
	'summary'		: 'Repeat Sale Order Reordering Previous Order Sales Reorder Quotation Past Sale Reordering Duplicate Sale Order Repeat Customer Sales Order History Sales Quotation Reorder Past Reorder Sale from Customer Sales Reordering',
	'description'	: """ 
		Customer Reorder Sale Odoo App helps users to reordering the previous order again. User can view all the previous order of customer in 'Order History' tab and also make duplicate order by clicking on 'REORDER' button. Once that button is clicked, the duplicate sales order should be generated and display Reorder wizard, By using this wizard user can perform any of the operation like send by Email, confirm or cancel the order. Also user can see duplicate sale order should be added into the order history.
	""",
	'author'		: 'BrowseInfo',
    'website'		: 'https://www.browseinfo.com',
	'depends'		: ['base','sale','sale_management'],
	'data'			: [
	                    'views/res_partner.xml'
						],
	'license'		: 'OPL-1',
	'installable'	: True,
    'auto_install'	: False,
    'live_test_url'	:'https://youtu.be/CKa15TCVS_k',
    "images"		:['static/description/Sale-Reorder-Banner.gif'],
}
