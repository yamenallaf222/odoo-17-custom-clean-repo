{
    'name' : "Library Management",
    'author' : "Yamen Allaf",
    'category' : ' ',
    'version': '17.0.0.1.0',
    'depends' : ['base'
                 ],
    'data': [
        'views/base_menu.xml',
        'views/book_view.xml',
    ],
    'assets':{
        'web.assets_backend':[
                '/library_management/static/src/css/book_kanban.css'
            ]
    },
    'application': True,
    'post_init_hook': 'post_init_create_depreciation_cron'
}