{
    'name' : "App One",
    'author' : "Muhammed Nasser",
    'category' : ' ',
    'version': '17.0.0.1.0',
    'depends' : ['base', 'sale_management', 'mail'
                 ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/all_tasks_view.xml',
    ],
    'assets':{
        'web.assets_backend':['/app_one/static/source/css/property.css']
    },
    'application': True,
}