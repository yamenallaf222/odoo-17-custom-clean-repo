from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    timer_ids = fields.One2many('todo.timer', inverse_name='todo_task_id')
    ref = fields.Char(default='New', readonly=True)
    name = fields.Char(required=True, default='New', tracking=1)
    assign_to = fields.Many2many('res.partner', string='Assigned To', tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Date(tracking=1)
    hourly_rate = fields.Monetary(default = 25.0, currency_field= 'currency_id')
    client_id = fields.Many2one('res.partner', string= 'Client')
    total_amount = fields.Monetary(string= 'Total Amount', currency_field= 'currency_id', compute= '_compute_total_amount')
    currency_id = fields.Many2one('res.currency', string= 'Currency', default= lambda self: self.env.company.currency_id)
    invoice_line_id = fields.Many2one('invoice.line', string= 'Invoice Line')
    is_late = fields.Boolean()
    status = fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('closed','Closed'),
    ], default='new', tracking=1)
    estimated_time = fields.Float(required=True, default=10.0)
    timesheet_line_ids = fields.One2many('timesheet.line', inverse_name='todo_task_id')
    timesheet_lines_total_time = fields.Float(string="Total Time", compute="_compute_total_time", store=True)


    active = fields.Boolean(default=1)

    @api.depends('estimated_time', 'hourly_rate')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.estimated_time * rec.hourly_rate


    @api.depends('timesheet_line_ids.time')
    def _compute_total_time(self):
        for rec in self:
            rec.timesheet_lines_total_time = sum(rec.timesheet_line_ids.mapped('time'))

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

    @api.model
    def create(self, vals):
        res = super(TodoTask, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('todo_seq')         
        return res
    
    def write(self, vals):

        if(self.status == 'completed' or self.status == 'closed'):
            raise ValidationError('Sorry, you can not update this task as it has been finished.')
        res = super(TodoTask, self).write(vals)
        return res
    
    def action_open_bulk_task_assignment_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('todo_app.bulk_task_assignment_wizard_action')
        action['context'] = {'default_tasks' : self.ids }
        return action

class TimesheetLine(models.Model):
    _name = 'timesheet.line'
    _description = "Timesheet lines"

    date = fields.Date(required=True)
    description = fields.Text(required=True)
    time = fields.Float(required=True)
    todo_task_id = fields.Many2one('todo.task')

    @api.constrains('date')
    def _check_date_not_greater_than_task_date(self):
        for rec in self:
            if rec.date > rec.todo_task_id.due_date:
                raise ValidationError("Please add valid Timesheet lines' time values: not bigger than task's due date")



class TodoTimer(models.Model):
    _name = 'todo.timer'

    # region Timer Implementation

    todo_task_id = fields.Many2one('todo.task', required= True, ondelete='cascade')
    start_time = fields.Datetime(string='Start At', default= False)
    stop_time = fields.Datetime(string='Stopped At', default= False)
    elapsed = fields.Float(string='Elapsed')
    is_running = fields.Boolean(string='Running', default= False)
        
    @api.depends('start_time', 'stop_time')
    def _compute_is_running(self):
        for rec in self:
            rec.is_running = bool(rec.start_time and not rec.stop_time)
            
    # region Timer RPC methods
    @api.model
    def action_start_timer(self, record_ids = None, **kwargs):
        results = []

        records = self.browse(record_ids)

        print(records)

        for rec in records:
            rec.write(
                {
                    'start_time': fields.Datetime.now(),
                    'stop_time': False,
                    'is_running': True
                }
            )
            
            result_data =  {
                'id': rec.id,
                'start_time': rec.start_time and str(rec.start_time),
                'stop_time': rec.stop_time and str(rec.stop_time),
                'is_running': rec.is_running
            }

            results.append(result_data)
        return results

    @api.model
    def action_stop_timer(self, record_ids = None, **kwargs):
        results = []

        records = self.browse(record_ids)

        for rec in records:
            if not rec.start_time:
                raise ValidationError('Timer was not started.')

            rec.write(
                {
                    'stop_time': fields.Datetime.now(),
                    'is_running': False
                }
            )

            result_data = {
                'id': rec.id,
                'stop_time': rec.stop_time,
                'is_running': rec.is_running
            }

            results.append(result_data)
        return results

    @api.model
    def update_live_elapsed(self, record_ids = None, **kwargs):
        results = []

        records = self.browse(record_ids)

        for rec in records:
            if not rec.start_time:
                rec.elapsed = 0.0
            
            end = rec.stop_time or fields.Datetime.now()
            delta = fields.Datetime.from_string(end) - fields.Datetime.from_string(rec.start_time)

            # we re storing database field here 
            rec.elapsed = delta.total_seconds()

            result_data = {
                'id': rec.id,
                'elapsed': rec.elapsed
            }

            results.append(result_data)
        return results


    # def get_timer_is_running(record_ids, self):
    #     for rec in self:
    #         return [rec.read(['is_running'])[0]['is_running'] for rec in self.browse(record_ids)]

    # endregion

    # endregion