from odoo import models, fields

class building(models.Model):
    _name = 'building'
    _description = 'Building Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = "code"

    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    name = fields.Char()
    #this field is a reserved one that enables archiving for records of this model
    active = fields.Boolean(default=1)

    