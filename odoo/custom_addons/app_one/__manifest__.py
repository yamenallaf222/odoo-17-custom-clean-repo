{
    'name' : "App One",
    'author' : "Muhammed Nasser",
    'category' : ' ',
    'version': '17.0.0.1.0',
    # account module instead of account_accountant for community odoo
    'depends' : ['base', 'sale_management', 'account', 'mail', 'contacts'
                 ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/data.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'views/property_history_view.xml',
        'views/account_move_view.xml',
        'wizard/change_state_wizard_view.xml',
        'reports/property_report.xml',
    ],
    'assets':{
        'web.assets_backend':['/app_one/static/src/css/property.css',
                              '/app_one/static/src/components/listView/listView.css',
                              '/app_one/static/src/components/listView/listView.js',
                              '/app_one/static/src/components/listView/listView.xml' ],
        'web.report_assets_common':['/app_one/static/src/css/font.css'],
    },
    'application': True,
}