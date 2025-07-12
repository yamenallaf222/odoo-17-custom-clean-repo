from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=1, default='New', tracking=1)
    assign_to = fields.Many2many('res.partner', string='Assigned To', tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    status = fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('closed','Closed'),
    ], default='new', tracking=1)
    estimated_time = fields.Float(required=1, default=10.0)
    timesheet_line_ids = fields.One2many('timesheet.line', inverse_name='todo_task_id')
    active = fields.Boolean(default=1)

    @api.constrains('estimated_time')
    def _check_estimated_time_is_not_less_than_the_total_time_of_timesheet_lines(self):
        for rec in self:
            total_time = sum(line.time for line in self.timesheet_line_ids)
            if rec.estimated_time < total_time:
                raise ValidationError("Please make sure the total time of Timesheet lines is not greater than estimated time")



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

    def action_closed(self):
        for rec in self:
            print("inside closed action")
            rec.status = 'closed'

    def check_due_date(self):
        todo_task_ids = self.search([])
        for rec in todo_task_ids:
            if fields.date.today() > rec.due_date and (rec.status not in ('closed', 'completed') ):
                rec.is_late = True
            else:
                rec.is_late = False


class TimesheetLine(models.Model):
    _name = 'timesheet.line'
    _description = "Timesheet lines"

    date = fields.Date(required=1)
    description = fields.Text(required=1)
    time = fields.Float(required=1)

    todo_task_id = fields.Many2one('todo.task')

    @api.constrains('date')
    def _check_date_not_greater_than_task_date(self):
        for rec in self:
            if rec.date > rec.todo_task_id.due_date:
                raise ValidationError("Please add valid Timesheet lines' time values: not bigger than task's due date")




   