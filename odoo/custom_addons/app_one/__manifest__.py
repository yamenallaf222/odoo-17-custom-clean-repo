{
    'name' : "App One",
    'author' : "Muhammed Nasser",
    'category' : ' ',
    'version': '17.0.0.1.0',
    'depends' : ['base', 'sale_management', 'mail', 'contacts'
                 ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'views/property_history_view.xml',
        'wizard/change_state_wizard_view.xml',
        'reports/property_report.xml',
    ],
    'assets':{
        'web.assets_backend':['/app_one/static/source/css/property.css']
    },
    'application': True,
}