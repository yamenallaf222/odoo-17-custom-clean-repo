from odoo import models, fields

class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=1, default='New', tracking=1)
    assign_to = fields.Many2many('res.partner', string='Assigned To', tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Date(tracking=1)
    status = fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
    ], default='new', tracking=1)
    
    def action_new(self):
        for rec in self:
            print("inside new action")
            rec.status = 'new'

    def action_in_progress(self):
        for rec in self:
            print("inside in_progress action")
            rec.write({
                'status':'in_progress'
            })

    def action_completed(self):
        for rec in self:
            print("inside completed action")
            rec.status = 'completed'


   