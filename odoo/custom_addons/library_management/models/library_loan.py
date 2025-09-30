from odoo import models, fields
from datetime import timedelta

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library loan'

    book = fields.Many2one('library.book', string= 'Book', required=True)
    member = fields.Many2one('library.member', string= 'member', required=True)
    loan_date = fields.Date(required=True, default= fields.Date.context_today)
    return_date = fields.Date(required=True, default= fields.Date.context_today + timedelta(days=3))
    state = fields.Selection(
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('late', 'Late'),
    default= 'draft')