import requests
import base64
import json

client_id = 'johnpmajor96@gmail.com_api_client_1641323507'
client_secret = "542c7223bacd469ab0f6a1fdcb5658fb"

identity_url = "https://id.livevol.com/connect/token"


authorization_token  = base64.b64encode((client_id + ':' + client_secret).encode())
headers = {"Authorization": "Basic " + authorization_token.decode('ascii')}
payload = {"grant_type": "client_credentials"}

# Requesting access token
token_data = requests.post(identity_url, data=payload, headers=headers)


def get_options_info(ticker, option_type, date, min_strike, max_strike):
    return f'https://api.livevol.com/v1/live/allaccess/market/option-and-underlying-quotes?root={ticker}&option_type={option_type}&date={date}&min_strike={min_strike}&max_strike={max_strike}&symbol={ticker}'


if token_data.status_code == 200:
    access_token = token_data.json()['access_token']
    if len(access_token) > 0:
        print("Authenticated successfully")
        
		# Requesting data from API
        api_url = get_options_info('TSLA', 'C', '2022-01-04', 175, 185)
        result = requests.get(api_url, headers={"Authorization": "Bearer " + access_token})
        json_result = result.json()
        options = json_result['options']
        for items in options:
            date = items['expiry']
            strike = items['strike']
            price = items['option_mid']
            type = items['option_type']
            if type == 'C':
                type = 'Call'
            if type == 'P':
                type = 'Puts'
            print(f'{date} {strike} {price} {type}')
            
else:
    print("Authentication failed")