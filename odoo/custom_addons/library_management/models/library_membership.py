from odoo import models, fields

class LibraryMembership(models.Model):
    _name = 'library.membership'
    _description = 'Library membership'

    name = fields.Char(required=True)
    max_books = fields.Integer(required=True)
    fee = fields.Float(required=True, string='Membership fee')
    # essentially make it default to all categories
    allowed_categories = fields.Many2many('library.category', default= lambda self: self.env['library.category'].search([]))