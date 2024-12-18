# coding: utf-8 

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class PcSurveyDecision(models.Model):
    _name = 'pc.survey.decision'
    _description = 'gestion des candidatures'

    email = fields.Char(string="Email", required=True)
    statut = fields.Selection([
        ('to_be_traited', 'A traiter'),
        ('validated', 'Validée'),
        ('rejected', 'Rejetée'),
        ('needinformation',"Besoin complément d’information")
    ], string="Statut", default='to_be_traited', required=True)
    comite=fields.Char(string="Comité d'appartenance")
    nom=fields.Char(string="Nom")
    prenom=fields.Char(string="Prénom")
    telephone=fields.Char(string="Téléphone")
    date_naissance=fields.Date(string="Date de naissance")
    commentaire = fields.Text(string="Commentaire", help="Commentaire des services du Siège")
    date_contact_comite = fields.Date(string="Date de contact", help="Date de la vérification de la prise de contact avec le comité")
    email_verification = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
        ('to_be_decided', 'A statuer')
    ], string="Email", default='to_be_decided', required=True)
    call_verification = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
        ('to_be_decided', 'A statuer')
    ], string="Appel", default='to_be_decided', required=True)
    date_email_confirmation = fields.Date(string="Date intégration", help="Date d'envoi de l'email de confirmation d'intégration")
    email_confirmation = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
        ('to_be_decided', 'A statuer')
    ], string="Email Confirmation", default='to_be_decided', required=True)
    adhesion_status = fields.Selection([
        ('yes', 'Oui adhérent'),
        ('no', 'Non pas adhérent'),
        ('to_be_checked', 'A vérifier')
    ], string="Statut d’adhésion", default='to_be_checked', required=True)
      # Champ Integer pour stocker l'ID du questionnaire

    
    user_input_id = fields.Many2one('survey.user_input', string="Jeu de réponses au questionnaire", required=True)

    # Lien One2many vers 'survey.user_input.line' pour récupérer toutes les lignes de réponses
    # Champ calculé pour récupérer les réponses à choix multiples
    #multiple_choice_answers = fields.Char(string="Réponses à choix multiples", compute="_compute_multiple_choice_answers", store=False)
    #suggested_answer_ids= fields.One2many('survey.question.answer', related='user_input_id.user_input_line_ids', string="Réponses à choix multiples")#, compute="_compute_multiple_choice_answers", store=False)
    
    # Nouveau champ calculé pour regrouper toutes les réponses
    

    user_input_lines = fields.One2many(
        'survey.user_input.line',  # Modèle des lignes de réponse
        related='user_input_id.user_input_line_ids',  # Champ relationnel dans 'survey.user_input'
        string="Réponses au questionnaire"
    )
   
    
    