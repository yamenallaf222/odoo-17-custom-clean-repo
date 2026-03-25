{
    'name' : "To Do",
    'author' : "Yamen Allaf",
    'category' : ' ',
    'version': '17.0.0.1.0',
    'depends' : ['base', 'mail', 'contacts'
                 ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/all_tasks_view.xml',
        'wizard/build_task_assignment_wizard_view.xml',
        'reports/todo_task_report.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'todo_app/static/src/css/custom.css',
            'todo_app/static/src/js/todo_timer_widget.js',
            'todo_app/static/src/xml/todo_timer_widget.xml',
        ],
    },
    'application': True,
}