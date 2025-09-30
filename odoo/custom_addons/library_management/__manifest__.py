{
    'name' : "Library Management",
    'author' : "Yamen Allaf",
    'category' : ' ',
    'version': '17.0.0.1.0',
    'depends' : ['base'
                 ],
    'data': [
    ],
    'application': True,
    'post_init_hook': 'post_init_create_depreciation_cron'
}