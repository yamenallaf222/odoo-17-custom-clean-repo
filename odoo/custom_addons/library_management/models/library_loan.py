from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library loan'

    book = fields.Many2one('library.book', string= 'Book', required=True)
    member = fields.Many2one('library.member', string= 'Member', required=True)
    loan_date = fields.Date(required=True, default= fields.Date.context_today)
    return_date = fields.Date(required=True, default= fields.Date.context_today + timedelta(days=3))
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('borrowed', 'Borrowed'),
            ('returned', 'Returned'),
            ('late', 'Late')
        ]
        , default= 'draft')

    @api.constrains('loan_date', 'return_date')
    def _check_dates_validity(self):
        if self.loan_date >= self.return_date:
            raise ValidationError(
                f'Loan date:{self.loan_date}, is higher or equal than return_date:{self.return_date} which is strictly prohibited'
            )


    @api.model
    def create(self, vals):
        member = None
        book = None
        state = None

        if 'member' and 'book' and 'state' in vals:
            member = vals['member']
            book = vals['book']
            state = vals['state']
        else:
            raise ValidationError('Loan creation process failed due to one of these fields missing the values passed for creation [Member, Book, State]')
        
        if member.membership_type == None:
            raise ValidationError('The member does not have an active membership, thus he is prohibited from any form of loans!!!!')
        
        max_books_pertaining_with_member = member.membership_type.max_books
        books_already_pertained_with_member = self.search_count([('member', '=', member), '|', ('state', '=', 'reserved'), ('state', '=', 'borrowed')])

        if books_already_pertained_with_member + 1 > max_books_pertaining_with_member:
            raise ValidationError(f"""Can not create this loan cause the member: {member} membership type: {member.membership_type.name} does not allow for 
                                  more than {max_books_pertaining_with_member} books to be reserved or borrowed,
                                  of which this record creation would make them {books_already_pertained_with_member + 1}!!!""")

        book.availability_status = state

        res = super(self).create(vals)
        return res
