from odoo import models, fields


class ItiTrack(models.Model):
    _name = 'iti.track'
    _rec_name = "track_name"

    track_name = fields.Char()
    is_open = fields.Boolean()
    student_ids = fields.One2many("iti.student", "track_id")
