import requests
import json

class MarketingCloudIntegration:

    def __init__(self):
        self.client_id = ''
        self.client_secret = ''
        self.subdomain = ''
        self.data_extension_key = ''
        self.rest_url = ''

    def get_access_token(self):
        endpoint = f'https://{self.subdomain}.auth.marketingcloudapis.com/v2/token'
        headers = {'Content-Type': 'application/json'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        response_data = response.json()
        return response_data['access_token']

    def send_data_to_data_extension(self, access_token):
        endpoint = f'{self.rest_url}/data/v2/async/dataextensions/key:{self.data_extension_key}/rows'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'items': [{
                'Nome': 'ExemploNome',
                'E-mail': 'exemplo@email.com',
                'Telefone': 1234567890,
                'Mensagem': 'ExemploMensagem',
                'Formulário de origem': 'ExemploForm',
                'Empreendimento': 'ExemploEmpreendimento',
                'Modalidade de contratação': 'ExemploModalidade',
                'Área de interesse': 'ExemploÁrea',
                'Anexar seu currículo': False,
                'LGPD': True
            }]
        }

        response = requests.post(endpoint, headers=headers, json=data)

        print(response.text)


integration = MarketingCloudIntegration()
access_token = integration.get_access_token()
integration.send_data_to_data_extension(access_token)
