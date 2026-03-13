from odoo import models, fields, api
from odoo.exceptions import ValidationError

class InvoiceLine(models.Model):

    _name = 'invoice.line'
    _description = 'Invoice Line'

    tasks = fields.One2many('todo.task')
    client_id = fields.Many2one('res.partner')
    total_hours = fields.Float(compute= '_compute_total_hours')
    total_amount = fields.Monetary(string= 'Total Amount', currency_field='currency_id', compute= '_compute_total_amount')
    currency_id = fields.Many2one('res.currency', string= 'Currency', default= lambda self: self.env.company.currency_id)
    invoice_date = fields.Date(default= fields.Date.today)

    def _compute_total_hours(self):        
        for rec in self:
            rec.total_hours = sum(task.estimated_time for task in rec.tasks)
    
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(task.total_amount for task in rec.tasks)


