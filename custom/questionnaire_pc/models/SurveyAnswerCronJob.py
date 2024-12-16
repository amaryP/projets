from odoo import models, fields, api
from unidecode import unidecode
import logging

_logger = logging.getLogger(__name__)

class SurveyAnswerCronJob(models.Model):
    _name = 'survey.answer.cron.job'
    _description = 'Cron job pour traiter les soumissions de sondage'

    def normalize_string(self, text):
        if text is None:
            return ''  # Retourner une chaîne vide si 'text' est None
        normalized_text = unidecode(text).replace(" ", "").lower()
        return normalized_text

    def match_substring(self, substring, main_string):
        main_string_clean = self.normalize_string(main_string)
        substring_clean = self.normalize_string(substring)
        main_string_cut = main_string_clean[:len(substring_clean)]
        if substring_clean == main_string_cut:
            return True
        return False

    @api.model
    def run_survey_submission_check(self):
        """
        Vérifie les réponses soumises au questionnaire ID = 1 et effectue les actions nécessaires.
        """
        user_inputs = self.env['survey.user_input'].search([('survey_id', '=', 1), ('state', '=', 'done')])
        
        for user_input in user_inputs:
            email = 'non renseigné'
            nom = 'non renseigné'
            firstname = 'non renseigné'
            dateofbirth = 'non renseigné'
            telephone = 'non renseigné'
            comite = 'non renseigné'

            for question in user_input.survey_id.question_ids:
                title = unidecode(question.title).replace(" ", "").lower()  # Nettoyer la chaîne
                
                # Traiter la question "email"
                if title == "adresseemail":
                    email_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=', question.id)
                    ], limit=1)
                    if email_line and email_line.value_char_box:
                        email = email_line.value_char_box
                        _logger.info(f"Réponse soumise pour l'email : {email}")

                # Traiter la question "nom"
                elif title == "nom":
                    nom_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=', question.id)
                    ], limit=1)
                    if nom_line and nom_line.value_char_box:
                        nom = nom_line.value_char_box.capitalize()
                        _logger.info(f"Réponse soumise pour le nom : {nom}")

                # Traiter la question "prénom"
                elif title == "prenom":
                    firstname_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=', question.id)
                    ], limit=1)
                    if firstname_line and firstname_line.value_char_box:
                        firstname = firstname_line.value_char_box.capitalize()
                        _logger.info(f"Réponse soumise pour le prénom : {firstname}")

                # Traiter la question "date de naissance"
                elif title == "datedenaissance":
                    dateofbirth_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=', question.id)
                    ], limit=1)
                    if dateofbirth_line and dateofbirth_line.value_date:
                        dateofbirth = dateofbirth_line.value_date
                        _logger.info(f"Réponse soumise pour la date de naissance : {dateofbirth}")

                # Traiter la question "téléphone"
                #elif title == "telephone":
                elif "telephone" in unidecode(title).replace(" ", "").lower():  # Recherche de la sous-chaîne "telephone"                    
                    telephone_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=', question.id)
                    ], limit=1)
                    if telephone_line and telephone_line.value_char_box:
                        telephone = telephone_line.value_char_box
                        _logger.info(f"Réponse soumise pour le téléphone : {telephone}")

                # Traiter la question "comité"
                #elif title == "comite":
                elif unidecode(title[:6]).replace(" ", "").lower() == "comite":  # Vérification des premiers caractères                    
                    comite_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=', question.id)
                    ], limit=1)
                    if comite_line and comite_line.suggested_answer_id:
                        comite = comite_line.suggested_answer_id.value
                        _logger.info(f"Réponse suggérée pour le comité : {comite}")

            # Création ou mise à jour de la décision
            decision_model = self.env['pc.survey.decision']
            existing_decision = decision_model.search([('email', '=', email)], limit=1)
            if not existing_decision:
                _logger.info(f"Création d'une nouvelle décision pour l'email : {email}")
                decision_model.create({
                    'email': email,
                    'nom': nom,
                    'prenom': firstname,
                    'date_naissance': dateofbirth,
                    'telephone': telephone,
                    'comite': comite,
                    'user_input_id': user_input.id
                })
            else:
                _logger.info(f"La décision existe déjà pour l'email : {email}")
