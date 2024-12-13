from odoo import models, fields, api
from unidecode import unidecode
import logging
import json
import re

_logger = logging.getLogger(__name__)

class SurveyAnswerCronJob(models.Model):
    _name = 'survey.answer.cron.job'
    _description = 'Cron job pour traiter les soumissions de sondage'

    # Fonction pour normaliser la chaîne (enlever accents, espaces et majuscules)
    def normalize_string(self, text):
        if text is None:
            return ''  # Retourner une chaîne vide si 'text' est None
        normalized_text = unidecode(text).replace(" ", "").lower()
        return normalized_text
    def extract_fr_fr(self, text):
        """
        Extrait la portion de la chaîne jusqu'à 'fr_FR' inclus, puis nettoie les guillemets.
        """
        _logger.info(f"text: {text}")
        # Utiliser une expression régulière pour extraire la partie jusqu'à 'fr_FR' inclus
        match = re.search(r'"fr_FR": "(.*?)"', text)
        _logger.info(f"Match: {match}")
        if match:
            # On récupère le texte entre guillemets et on nettoie les guillemets
            extracted_text = match.group(1)
            # Nettoyer les guillemets supplémentaires et autres caractères indésirables
            clean_text = unidecode(extracted_text).replace('""', '').strip()
            return clean_text
        else:
            _logger.warning("Aucune correspondance trouvée pour 'fr_FR'.")
            return None
    # Fonction pour rechercher une sous-chaîne dans les premiers caractères de la chaîne principale
    def match_substring(self, substring, main_string):
        # Normaliser la chaîne principale
        main_string_clean = self.normalize_string(main_string)
        
        # Normaliser la sous-chaîne recherchée
        substring_clean = self.normalize_string(substring)
        
        # Découper la chaîne principale pour obtenir les premiers caractères correspondant à la longueur de la sous-chaîne
        main_string_cut = main_string_clean[:len(substring_clean)]
        _logger.info(f"Processing question {main_string_clean}: {substring_clean}:{main_string_cut} ")  # Log pour chaque question
        # Comparer si la sous-chaîne recherchée est égale aux premiers caractères de la chaîne principale
        if substring_clean == main_string_cut:
            return True
        return False

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
                # Traite le nom
                
                # Parcours des questions du sondage
                for question in user_input.survey_id.question_ids:
                    title = question.title  # Récupérer le champ JSON 'title' de la question
                    # initialisation le nom
                    nom = 'non renseigné'
                    _logger.info(f"Traitement de la question : {title}")
                    #title_fr=self.extract_fr_fr(title)
                    # Utiliser la fonction match_substring pour vérifier si "1.nom" est dans le titre de la question
                    #if self.match_substring('1.nom', title_fr):  # Recherche de "nom" dans le titre
                    #if title.lower()=="nom":      
                    if unidecode(title).replace(" ", "").lower() == "nom":                                         
                        # Recherche de la réponse pour cette question
                        nom_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=', question.id)
                        ], limit=1)
                    # Si une ligne de réponse est trouvée pour la question contenant "nom"
                        if nom_line:
                            nom = nom_line.value_char_box  # Récupère le nom de la réponse
                            nom = nom.capitalize()  # Mettre la première lettre en majuscule
                            _logger.info(f"Réponse soumise pour le nom : {nom}")

                        # Sortir de la boucle dès qu'on a trouvé la réponse
                            break
                           # Vérification si 'name' est toujours None (pas trouvé)
                #traite le prenom
                firstname = 'non renseigné'
                firstname_line = None                
                for question in user_input.survey_id.question_ids:
                    title = question.title  # Récupérer le champ JSON 'title' de la question

                    _logger.info(f"Traitement de la question : {title}")
                    if unidecode(title).replace(" ", "").lower() == "prenom":                                         
                
                      firstname_line = None
                      firstname_line = self.env['survey.user_input.line'].search([
                      ('user_input_id', '=', user_input.id),
                      ('question_id', '=',  question.id)#5)  # ID de la question 'prenom'
                      ], limit=1)

                # Si une ligne de réponse est trouvée pour la question contenant "prenom"
                if firstname_line:
                    firstname = firstname_line.value_char_box  # Récupère le nom de la réponse
                    firstname = firstname.capitalize()  # Mettre la première lettre en majuscule
                    _logger.info(f"Réponse soumise pour le prenom : {firstname}")
                #traite la date de naissance
                #traite le prenom
                #dateofbirth = 'non renseigné'
                dateofbirth_line = None
                for question in user_input.survey_id.question_ids:
                    title = question.title  # Récupérer le champ JSON 'title' de la question

                    _logger.info(f"Traitement de la question : {title}")
                    if unidecode(title).replace(" ", "").lower() == "datedenaissance":                                         
                
                      dateofbirth_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=',question.id)# 6)  # ID de la question 'date de naissance'
                        ], limit=1)

                # Si une ligne de réponse est trouvée pour la question contenant "date de naissance"
                dateofbirth = None
                if dateofbirth_line:
                    dateofbirth = dateofbirth_line.value_date  # Récupère le nom de la réponse
                    _logger.info(f"Réponse soumise pour la date de naissance : {dateofbirth}")

                #traite le telephone
                telephone_line = None
                # Parcours des questions du sondage       
                for question in user_input.survey_id.question_ids:
                    title = question.title  # Récupérer le champ JSON 'title' de la question

                    _logger.info(f"Traitement de la question : {title}")
                    if unidecode(title[:9]).replace(" ", "").lower() == "telephone":                                         
                        telephone_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=',  question.id)# 9)  # ID de la question 'telephone'
                        ], limit=1)

                # Si une ligne de réponse est trouvée pour la question contenant "telephone"
                telephone = None
                if telephone_line:
                    telephone = telephone_line.value_char_box  # Récupère le nom de la réponse
                    _logger.info(f"Réponse soumise pour le telephone : {telephone}")

                #traite le comité
                comite_line = None
                # Parcours des questions du sondage
                for question in user_input.survey_id.question_ids:
                    title = question.title  # Récupérer le champ JSON 'title' de la question
                    # initialisation comité
                    comite = 'non renseigné'
                    _logger.info(f"Traitement de la question : {title}")
                    if unidecode(title[:6]).replace(" ", "").lower() == "comite":                                         
                        # Recherche de la réponse pour cette question
                        comite_line = self.env['survey.user_input.line'].search([
                        ('user_input_id', '=', user_input.id),
                        ('question_id', '=',question.id)# 11)  # ID de la question 'comite'
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
                        'nom': nom,
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