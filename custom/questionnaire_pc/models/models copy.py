# coding: utf-8 

from odoo import models, fields, api



class PcSurveyDecision(models.Model):
    _name = 'pc.survey.decision'
    _description = 'gestion des candidatures'

    #user_input_id = fields.Many2one(
    #    'survey.user_input', string="Réponses au questionnaire associée", required=True, ondelete="cascade"
    #)
    email = fields.Char(string="Email", required=True)
    statut = fields.Selection([
        ('pending', 'En attente'),
        ('validated', 'Validée'),
        ('rejected', 'Rejetée'),
    ], string="Statut Candidature", default='pending', required=True)
    commentaire = fields.Text(string="Commentaire", help="Commentaire des services du Siège")
    #latest_response_id = fields.Many2one(
    #    'survey.user_input', string="Dernier jeu de réponses", compute="_compute_latest_response"
    #)

    '''@api.depends('email')
    def _compute_latest_response(self):
        for record in self:
            if record.email:
                latest_response = self.env['survey.user_input'].search(
                    [('email', '=', record.email)], order='create_date desc', limit=1
                )
                record.latest_response_id = latest_response.id if latest_response else False
            else:
                record.latest_response_id = False
     '''
#import logging

#_logger = logging.getLogger(__name__)

"""
class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    @api.model
    def create(self, vals):
        
        Détecte la création d'une nouvelle réponse pour un questionnaire spécifique
        et crée une ligne dans PcSurveyDecision.
        
        _logger.info("Entrée dans la méthode create pour survey.user_input")

        # Créer l'enregistrement dans survey.user_input
        new_record = super(SurveyUserInput, self).create(vals)
        #self.env.cr.flush()  # Force l'écriture en base de données
        #_logger.info("Après la création de l'enregistrement dans survey.user_input")
         # Délai volontaire pour garantir que les lignes sont enregistrées
       

        # Vérifier si la réponse appartient au questionnaire cible
        TARGET_SURVEY_ID = 1  # ID du questionnaire cible
        if new_record.survey_id.id == TARGET_SURVEY_ID:
            _logger.info(f"Le questionnaire ID {new_record.survey_id.id} correspond au sondage cible")

            # Utiliser directement l'ID de la question pour chercher la réponse associée
            email_question_id = 8  # ID de la question "email"
            user_input_id=53
            _logger.info(f"Le record ID est {new_record.id}  et la question ID est {email_question_id}")

            # Rechercher la ligne de réponse pour la question "email" dans char_box
            email_line = self.env['survey.user_input.line'].search([
                ('user_input_id', '=',user_input_id),# new_record.id),
                ('question_id', '=', email_question_id),
                ('survey_id', '=', new_record.survey_id.id),  # Ajout du filtre sur survey_id
            ], order='create_date desc', limit=1)  # Trier par date de création descendante (la plus récente)
            # Afficher le contenu du recordset dans les logs
            #_logger.info(f"Contenu du recordset email_line: {email_line}")
            #fields = self.env['survey.user_input.line'].fields_get()
            #logger.info(f"Champs disponibles dans survey.user_input.line : {fields}")
            if email_line:
                email = email_line.value_char_box  # Utilisation de char_box pour récupérer l'email
                _logger.info(f"Email récupéré : {email}")
                
               # Créer une entrée dans pc.survey.decision si l'email n'existe pas encore
                decision_model = self.env['pc.survey.decision']
                existing_decision = decision_model.search([('email', '=', email)], limit=1)
                if not existing_decision:
                    decision_model.create({
                        'email': email,
                        'statut': 'En attente',
                        'commentaire': '',
                    })
                else:
                 _logger.warning(f"Aucune ligne de réponse trouvée pour la question 'email' (question_id: {email_question_id})")
        else:
         _logger.info(f"Le questionnaire ID {new_record.survey_id.id} ne correspond pas au sondage cible.")

        return new_record
"""