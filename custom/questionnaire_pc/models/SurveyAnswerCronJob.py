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

                # Recherche du nom dans les réponses, basé sur la question contenant 'nom'
                # On accède explicitement à la valeur de "title" dans le champ JSON
                ''' # a refaire une fois le nouveau champs reference implementé
                
                for question in user_input.survey_id.question_ids:
                    title = question.title  # Récupérer le champ JSON title de la question
                    if isinstance(title, dict):  # Vérifier si title est un dictionnaire
                        # On vérifie si 'nom' est dans le libellé de la question
                          title_fr = title.get('fr_FR', '')  # Récupérer la valeur en français (fr_FR)
                          if 'nom' in title_fr.lower():  # Recherche insensible à la casse
                            # Recherche de la réponse pour cette question
                            name_line = self.env['survey.user_input.line'].search([
                                ('user_input_id', '=', user_input.id),
                                ('question_id', '=', question.id)
                            ], limit=1)
                            break
                '''
                #traite le nom
                name_line = None
                name_line = self.env['survey.user_input.line'].search([
                ('user_input_id', '=', user_input.id),
                ('question_id', '=', 4)  # ID de la question 'nom'
                ], limit=1)

                # Si une ligne de réponse est trouvée pour la question contenant "nom"
                name = None
                if name_line:
                    name = name_line.value_char_box  # Récupère le nom de la réponse
                    name = name.capitalize()  # Mettre la première lettre en majuscule
                    _logger.info(f"Réponse soumise pour le nom : {name}")
                #traite le prenom
                firstname_line = None
                firstname_line = self.env['survey.user_input.line'].search([
                ('user_input_id', '=', user_input.id),
                ('question_id', '=', 5)  # ID de la question 'prenom'
                ], limit=1)

                # Si une ligne de réponse est trouvée pour la question contenant "prenom"
                firstname = None
                if firstname_line:
                    firstname = firstname_line.value_char_box  # Récupère le nom de la réponse
                    firstname = firstname.capitalize()  # Mettre la première lettre en majuscule
                    _logger.info(f"Réponse soumise pour le prenom : {firstname}")
                #traite la date de naissance
                dateofbirth_line = None
                dateofbirth_line = self.env['survey.user_input.line'].search([
                ('user_input_id', '=', user_input.id),
                ('question_id', '=', 6)  # ID de la question 'date de naissance'
                ], limit=1)

                # Si une ligne de réponse est trouvée pour la question contenant "date de naissance"
                dateofbirth = None
                if dateofbirth_line:
                    dateofbirth = dateofbirth_line.value_date  # Récupère le nom de la réponse
                    _logger.info(f"Réponse soumise pour la date de naissance : {dateofbirth}")

                #traite le telephone
                telephone_line = None
                telephone_line = self.env['survey.user_input.line'].search([
                ('user_input_id', '=', user_input.id),
                ('question_id', '=', 9)  # ID de la question 'telephone'
                ], limit=1)

                # Si une ligne de réponse est trouvée pour la question contenant "telephone"
                telephone = None
                if telephone_line:
                    telephone = telephone_line.value_char_box  # Récupère le nom de la réponse
                    _logger.info(f"Réponse soumise pour le telephone : {telephone}")

                #traite le comité
                comite_line = None
                comite_line = self.env['survey.user_input.line'].search([
                ('user_input_id', '=', user_input.id),
                ('question_id', '=', 11)  # ID de la question 'comite'
                ], limit=1)

                comite = None
                if comite_line:
                 # Si une ligne de réponse est trouvée pour la question 'comité'
                 # On accède à l'ID de la réponse suggérée via suggested_answer_id
                    suggested_answer_id = comite_line.suggested_answer_id
                    if suggested_answer_id:
                        comite = suggested_answer_id.value  # Récupère la valeur de la réponse suggérée
                        _logger.info(f"Réponse suggérée pour le comité : {comite}")
                    else:
                        _logger.warning(f"Aucune réponse suggérée trouvée pour la question 'comité'.")
                else:
                    _logger.warning(f"Aucune ligne de réponse trouvée pour la question 'comité'.")


                # Création de la décision si l'email n'existe pas déjà dans pc.survey.decision
                decision_model = self.env['pc.survey.decision']
                existing_decision = decision_model.search([('email', '=', email)], limit=1)
                if not existing_decision:
                    _logger.info(f"Création d'une nouvelle décision pour l'email : {email}")
                    decision_model.create({
                        'email': email,
                        #'statut': 'pending',
                        #'commentaire': '',
                        'nom': name,
                        'prenom':firstname,
                        'date_naissance':dateofbirth,
                        'telephone':telephone,
                        'comite':comite,
                        'user_input_id':user_input.id

                    })
                else:
                    _logger.info(f"La décision existe déjà pour l'email : {email}")
                    #on referencera les dernieres reponses, mais on ne touchera pas aux élements recuperés initialement.
            else:
                _logger.warning(f"Aucune ligne de réponse pour l'email dans le sondage ID: {user_input.id}")
