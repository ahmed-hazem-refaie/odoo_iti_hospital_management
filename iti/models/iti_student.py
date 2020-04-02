from odoo import models, fields, api
from odoo.exceptions import UserError


class ItiStudent(models.Model):
    _name = 'iti.student'
    # _log_access = False

    name = fields.Char(required=True)
    age = fields.Integer()
    mobile = fields.Char()
    basic_salary = fields.Float()
    bonus = fields.Float()
    salary = fields.Float(compute="compute_salary", store=True)
    bonus_percent = fields.Float(compute="compute_salary")
    birth_date = fields.Date()
    interview_time = fields.Datetime()
    gender = fields.Selection([
        ("m", 'Male'),
        ("f", "Female")
    ])
    military_certificate = fields.Binary()
    is_accepted = fields.Boolean()
    info = fields.Text()
    formatted_info = fields.Html()
    track_id = fields.Many2one(comodel_name="iti.track")
    is_track_open = fields.Boolean(related="track_id.is_open")
    skills_ids = fields.Many2many("iti.skill")
    state = fields.Selection([
        ('applied', "Applied"),
        ('first', "First Interview"),
        ('second', "second Interview"),
        ('rejected', "Rejected"),
        ('Accepted', "Accepted")
    ], default="applied")

    @api.depends("basic_salary", "bonus")
    def compute_salary(self):
        for rec in self:
            rec.salary = rec.basic_salary + rec.bonus
            # rec.bonus_percent = rec.bonus / rec.basic_salary

    @api.constrains("age")
    def _check_age(self):
        for record in self:
            if record.age > 30:
                raise ValidationError(f"Your record is too old: {record.age}")
        # all records passed the test, don't return anything

    _sql_constraints = [
        ("Valid Mobile", "UNIQUE(mobile)", "The mobile you entered already exist"),
        ("Check Age", "CHECK(age >= 15 and age <= 20)", "The age is not valid"),
    ]

    # @api.multi
    # def write(self, vals):
    #     for rec in self:
    #         if rec.state != "applied":
    #             rec.age = 15
    #         else:
    #             raise UserError(f"You can't delete student with state {rec.state}")
    #     return super().write(vals)

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state != "applied":
                raise UserError(f"You can't delete student with state {rec.state}")
        super().unlink()

    @api.model
    def create(self, vals):
        new_student = super().create(vals)
        return new_student

    @api.constrains("mobile")
    def check_mobile(self):
        if len(self.mobile) != 11:
            raise UserError("Mobile should be 11 numbers")




    # search(self, args, offset=0, limit=None, order=None, count=False)

    # self.search([]) => [rec].name

    """
    SELECT * from iti_student
    WHERE age > 15
    limit 2, 5
    order by id
    """




    def change_state(self):
        students = self.search([("state", "=", "applied")])
        for student in students:
            student.state = "first"
        # students.write({"state": "first"})


    # @api.onchange("gender")
    # def onchange_gender(self):
    #     if self.gender == "m":
    #         self.salary = 2000
    #         new_domain = []
    #     else:
    #         self.salary = 1500
    #         new_domain = [("is_open", "=", True)]
    #     return {
    #         "domain": {'track_id': new_domain},
    #         "warning": {
    #             "title": "Gender Change",
    #             "message": "You changed the gender, note that it may affect the salary and available tracks"
    #         }
    #     }


class ItiSkill(models.Model):
    _name = "iti.skill"

    name = fields.Char()
