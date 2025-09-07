from odoo import fields, models
from odoo.exceptions import UserError


class BulkTaskAssignment(models.TransientModel):

    _name = "bulk.task.assignment"

    assignee = fields.Many2one('res.partner', string='Assignee')
    tasks = fields.Many2many('todo.task', string='Assigned tasks')
    
    def action_confirm(self):
        for task in self.tasks:
            # 4 means append to a Many2many list
            task.assign_to = [(4, self.assignee.id)]
