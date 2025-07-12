from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, default='New')
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
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
    owner_address = fields.Char(related='owner_id.address', readonly=0)
    owner_phone = fields.Char(related='owner_id.phone', readonly=0)


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
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            print("inside pending action")
            rec.write({
                'state':'pending'
            })

    def action_sold(self):
        for rec in self:
            print("inside sold action")
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'

    #self will be empty as it is triggered by an automated action
    def check_expected_selling_date(self):
        print(self)
        #empty list [] meaning all records will be retrieved
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True



    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Property, self).create(vals)
    #     print("inside create method")
    #     return res

    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset, limit, order, access_rights_uid)
    #     print ("inside search method")
    #     return res
    
    # def _write(self, vals):
    #     res = super(Property, self)._write(vals)
    #     print("inside write method")
    #     return res
    
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("isnide unlink method")
    #     return res


class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')

