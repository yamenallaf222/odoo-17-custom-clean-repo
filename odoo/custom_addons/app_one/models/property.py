from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, default='New')
    ref = fields.Char(default="New", readonly=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=1)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address', readonly=False)
    owner_phone = fields.Char(related='owner_id.phone', readonly=False)


    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','Closed'),
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name exists!')
    ]

    line_ids = fields.One2many('property.line', inverse_name='property_id')
    active = fields.Boolean(default=1)

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print(rec)
            print("inside _compute_diff method")
            rec.diff = rec.expected_price - rec.selling_price


    @api.onchange('expected_price', 'owner_id.phone')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print("inside _onchange_expected_price method")
            return {
                'warning':{'title':'warning', 'message':'negative value.', 'type':'notification'}
            }


    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please add valid number of bedrooms')
            
    def action_draft(self):
        for rec in self:
            print("inside draft action")
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            print("inside pending action")
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            print("inside sold action")
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    #self will be empty as it is triggered by an automated action
    def check_expected_selling_date(self):
        print(self)
        #empty list [] meaning all records will be retrieved
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

    def action(self):
        print(self.env['owner'].search([]))

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id' : rec.env.uid,
                'property_id' : rec.id,
                'old_state' : old_state,
                'new_state' : new_state,
                'reason' : reason or ""
            })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {'default_property_id': self.id}
        return action
    

class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')

