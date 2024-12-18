from odoo import models, fields, api

class SurveyUserInputLine(models.Model):
    _inherit = "survey.user_input.line"

    combined_value = fields.Char(
        string="Réponse",
        compute="_compute_combined_value",
        store=False
    )

    def _compute_combined_value(self):
        for record in self:
            if record.suggested_answer_id:
                record.combined_value = record.suggested_answer_id.value
            elif record.value_char_box:
                record.combined_value = record.value_char_box
            elif record.value_date:
                # Format français : JJ/MM/AAAA
                 record.combined_value = record.value_date.strftime('%d/%m/%Y')                
            elif record.value_text_box:
                record.combined_value = record.value_text_box
            else:
                record.combined_value = ""
