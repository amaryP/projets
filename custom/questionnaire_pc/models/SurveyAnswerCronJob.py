from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SurveyAnswerCronJob(models.Model):
    _name = 'survey.answer.cron.job'
    _description = 'Cron job pour traiter les soumissions de sondage'

    @api.model
    def run_survey_submission_check(self):
        """
        Vérifie les réponses soumises au questionnaire ID = 1 et effectue les actions nécessaires
        (par exemple, créer une décision pour chaque soumission).
        """
        # Récupérer toutes les réponses soumises pour le questionnaire ID=1
        user_inputs = self.env['survey.user_input'].search([
            ('survey_id', '=', 1),  # Filtrer sur le questionnaire avec ID=1
            ('state', '=', 'done')  # Ne prendre que les questionnaies terminés
        ])

        # Parcours des réponses soumises
        for user_input in user_inputs:
            # Parcours des lignes de réponse pour trouver la réponse à la question email
            email_line = self.env['survey.user_input.line'].search([
                ('user_input_id', '=', user_input.id),
                ('question_id', '=', 8)  # ID de la question 'Email'
            ], limit=1)

            if email_line and email_line.value_char_box:
                email = email_line.value_char_box
                _logger.info(f"Réponse soumise pour l'email : {email}")

                # Création de la décision si l'email n'existe pas déjà dans pc.survey.decision
                decision_model = self.env['pc.survey.decision']
                existing_decision = decision_model.search([('email', '=', email)], limit=1)
                if not existing_decision:
                    _logger.info(f"Création d'une nouvelle décision pour l'email : {email}")
                    decision_model.create({
                        'email': email,
                        #'statut': 'pending',
                        #'commentaire': '',
                        'user_input_id':user_input.id

                    })
                else:
                    _logger.info(f"La décision existe déjà pour l'email : {email}")
                    #on referencera les dernieres reponses, mais on ne touchera pas aux élements recuperés initialement.
            else:
                _logger.warning(f"Aucune ligne de réponse pour l'email dans le sondage ID: {user_input.id}")
