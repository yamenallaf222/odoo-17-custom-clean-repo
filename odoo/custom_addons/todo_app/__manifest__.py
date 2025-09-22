{
    'name' : "To Do",
    'author' : "Yamen Allaf",
    'category' : ' ',
    'version': '17.0.0.1.0',
    'depends' : ['base', 'mail', 'contacts'
                 ],
    'data': [
        'security/security_groups.xml',
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/all_tasks_view.xml',
        'wizard/build_task_assignment_wizard_view.xml',
        'reports/todo_task_report.xml'
    ],
    'application': True,
}