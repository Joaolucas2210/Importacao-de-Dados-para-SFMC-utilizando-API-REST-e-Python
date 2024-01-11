# Importação de Dados para SFMC utilizando API REST e Python

Uma breve descrição sobre o que esse projeto faz e para quem ele é

Importação de Dados para o Salesforce Marketing Cloud via Python REST API

Como importar dados para o Salesforce Marketing Cloud usando a API REST com Python. 

# 1. Configuração Inicial:
Para começar, você precisa configurar suas credenciais e criar uma Data Extension no Salesforce Marketing Cloud.

# 1.1. Criação de Credenciais:

Acesse Setup -> Apps -> Installed Packages.
Crie um novo pacote instalado e anote o Client ID e Client Secret gerados.
1.2. Criação da Data Extension:

Consulte o guia fornecido no artigo para criar uma Data Extension e obter a chave externa.

# 1.3. Credenciais:

Client ID:

Client Secret:

Subdomínio (Subdomain):

Chave Externa da Data Extension:

URL da API REST:


# 2. Configuração no Python:
Certifique-se de ter Python 3.X instalado e execute o seguinte comando para instalar as bibliotecas necessárias:

~~~Python
pip install requests datetime json
~~~
No topo do seu script Python, importe as bibliotecas necessárias:

~~~Python
import json
from datetime import datetime
import requests
import sys
from math import floor
from time import time
~~~~
# 3. Autenticação e Importação de Dados:


# 3.1. Método para Obter Access Token:

Função para obter o token de acesso:

~~~Python
def generate_access_token(clientid: str, clientsecret: str) -> str:
    subdomain = 'YOUR_SUBDOMAIN'
    auth_base_url = f'https://{subdomain}.auth.marketingcloudapis.com/v2/token'
    headers = {'content-type': 'application/json'}
    payload = {
      'grant_type': 'client_credentials',
      'client_id': clientid,
      'client_secret': clientsecret
    }
    authentication_response = requests.post(
        url=auth_base_url, data=json.dumps(payload), headers=headers
    ).json()

    if 'access_token' not in authentication_response:
        raise Exception(
          f'Unable to validate (ClientID/ClientSecret): {repr(authentication_response)}'
        )
    access_token = authentication_response['access_token']
    expires_in = time() + authentication_response['expires_in']

    return access_token, expires_in
~~~

# 3.2. Métodos para Importação de Dados:

Métodos para importar dados para a Data Extension:

~~~Python
def datetime_converter(value: datetime) -> str:
    if isinstance(value, datetime):
        return value.__str__()

def get_batch_size(record: dict) -> int:
    batch = json.dumps({'items': record}, default=datetime_converter)
    return floor(4000 / (sys.getsizeof(batch) / 1024))

def import_data(clientid: str, clientsecret: str,
                data_extension: str, data: list[dict]) -> None:
    expires_in, access_token = get_access_token(clientid, clientsecret)
    subdomain = 'YOUR_SUBDOMAIN'
    rest_url = f'https://{subdomain}.rest.marketingcloudapis.com'
    headers = {'authorization': f'Bearer {access_token}'}
    
    batch_size = get_batch_size(data[0])
    for batch in range(0, len(data), batch_size):
        if expires_in < time() + 60:
            expires_in, access_token = get_access_token(clientid, clientsecret)
        batch_data = records[batch:batch + batch_size]
        insert_request = requests.post(
            url=f'{rest_url}/data/v1/async/dataextensions/key:{data_extension}/rows',
            data=json.dumps({'items': batch_data}, default=datetime_converter),
            headers=headers
        )

        if insert_request.status_code not in (200, 202):
            raise Exception(f'Insertion failed with message: {insert_request.json()}')
    insert_request.close()
~~~

# 4. Exemplo de Uso:
Exemplo de como usar o script Python para importar dados:

~~~Python
if __name__ == "__main__":
    access_token, expires_in = generate_access_token("seu_client_id", "seu_client_secret")

    data_to_import = [
        {'column_1': 'value1', 'column_2': 'value2'},
        {'column_1': 'value3', 'column_2': 'value4'}
    ]

    import_data("seu_client_id", "seu_client_secret", "chave_externa_data_extension", data_to_import)
~~~

Certifique-se de substituir "seu_client_id", "seu_client_secret", "chave_externa_data_extension" e os valores dos campos com os dados antes de executar o script.
