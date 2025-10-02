from odoo import models, fields


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library member'

    name = fields.Char(required=True, default='new')
    partner_id = fields.Many2one('res.partner', string='Contact info', ondelete='cascade', required=True)
    membership_type = fields.Many2one('library.membership', string='Membership type', ondelete='set null')

    _sql_constraints =[
        ('partner_unique', 'unique(partner_id)', 'Each member must have a unique contact info')
    ]
