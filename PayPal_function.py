# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:05:19 2024

@author: 22011881g
"""

import requests
import json


def get_token():
    data = {
        'grant_type': 'client_credentials',
    }

    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', data=data, auth=(
        'AaN1T7CIGO-5Aq_ejBTr6PVwfg9gBCZsubDPC8pYWpafcLoSsUz81dyPQuPbdoi5imLgjNMCSCJPhxP6',
        'EM4Q-o7e8-gqiW3VZFEzlM69LOFfbasLK5kZYMka0XQk_TPRwuHffj5jCZB4BzGYDq34Hvi_TxVRLK8J'))
    data = response.json()
    access_token = data.get('access_token')
    print("\nToken got.\nCode : {}".format(response.status_code))
    print("Access_token : {}".format(access_token))
    return access_token


def create_order(access_token, currency_code, value, reference_id):
    url = "https://api.sandbox.paypal.com/v2/checkout/orders"

    cur = '"USD"'
    value = str(value)
    payload = '{ "intent": "CAPTURE", "purchase_units": [{"reference_id": "T2","amount": {"currency_code": ' + cur + ',"value": ' + value + '}}],"application_context": {"return_url": "", "cancel_url": ""}}'

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'accept-language': "en_US",
        'authorization': "Bearer " + access_token
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    data = response.json()
    id = data.get('id')
    print("\nOrder created.\nCode : {}".format(response.status_code))
    return (id)


def check_order_detail(access_token, id):
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders/' + str(id)

    response = requests.get(url, headers=headers)

    print("\nOrder detail checked.\nCode : {}".format(response.status_code))
    print(response.text)


def confirm_payment(id, given_name, surname, email_address, access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'
    }

    data = '{ "payment_source": { "paypal": { "name": { "given_name": "' + given_name + '", "surname": "' + surname + '" }, "email_address": "' + email_address + '", "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "brand_name": "Token Cafe", "locale": "en-US", "landing_page": "LOGIN", "shipping_preference": "SET_PROVIDED_ADDRESS", "user_action": "PAY_NOW", "return_url": "http://127.0.0.1:5000/check_paid", "cancel_url": "http://127.0.0.1:5000" } } } }'
    url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders/' + str(id) + '/confirm-payment-source'
    response = requests.post(url, headers=headers, data=data)

    print("\nPayer Action\nCode : {}".format(response.status_code))

    dict = json.loads(response.text)
    print(response.text)
    # a = {"id":"7JH848549C086502Y","status":"PAYER_ACTION_REQUIRED","payment_source":{"paypal":{"email_address":"sb-fa2bn29862044@personal.example.com","name":{"given_name":"John","surname":"Doe"}}},"payer":{"name":{"given_name":"John","surname":"Doe"},"email_address":"sb-fa2bn29862044@personal.example.com"},"links":[{"href":"https://api.sandbox.paypal.com/v2/checkout/orders/7JH848549C086502Y","rel":"self","method":"GET"},{"href":"https://www.sandbox.paypal.com/checkoutnow?token=7JH848549C086502Y","rel":"payer-action","method":"GET"}]}
    b = dict['links']
    payment_link = ''
    for c in b:
        if 'payer-action' in c['rel']:
            payment_link = c['href']
            print("Please confirm your payment via this link: \n\n{}\n\n".format(payment_link))

    return payment_link


def capture(access_token, id):
    headers = {
        'PayPal-Request-Id': id,
        'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json',
    }
    url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders/' + str(id) + '/capture'
    response = requests.post(url, headers=headers)
    print("\nPayment Captured\nCode : {}".format(response.status_code))
    data = response.json()
     
    return (data)


def generate_invoice(access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
    }

    response = requests.post('https://api-m.sandbox.paypal.com/v2/invoicing/generate-next-invoice-number',
                             headers=headers)
    dict = json.loads(response.text)
    invoice = dict["invoice_number"]
    print('invoice : {}'.format(invoice))
    return (invoice)


def send_invoice(access_token, invoice_number):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
        'PayPal-Request-Id': 'b1d1f06c7246c',
    }

    data = '{ "send_to_invoicer": true }'
    url = 'https://api-m.sandbox.paypal.com/v2/invoicing/invoices/{}/send'.format(invoice_number)
    response = requests.post(url, headers=headers, data=data)
    print(response.text)
    print("sent_invoice")


def create_order_(currency_code, value):
    access_token = get_token()
    id = create_order(access_token, currency_code, value, reference_id="20240328_01")
    return access_token, id


def make_payment_link(given_name, surname, email_address, access_token, id):
    check_order_detail(access_token, id)
    payment_link = confirm_payment(id, given_name, surname, email_address, access_token)
    return payment_link


def check_paid_(access_token, id):
    check_order_detail(access_token, id)
    result = (capture(access_token, id))

    return result

def refund(access_token, id,refund_id):
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+access_token,'Prefer': 'return=representation'}
    url = 'https://api.sandbox.paypal.com/v2/payments/captures/{}/refund'.format(refund_id)
    response = requests.post(url, headers=headers, data={})
    status = response.json()
    print (status["id"])
    status = status['status']
  
    return (status)