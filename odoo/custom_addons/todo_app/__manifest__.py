{
    'name' : "To Do",
    'author' : "Yamen Allaf",
    'category' : ' ',
    'version': '17.0.0.1.0',
    'depends' : ['base', 'mail', 'contacts'
                 ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/all_tasks_view.xml',
        'reports/todo_task_report.xml'
    ],
    'application': True,
}