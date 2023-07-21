from twilio.rest import Client


account_sid = 'AC8d3d32b648a0ff044a1b594dbc2f76c9'
auth_token = '38a32989fb4d5d827cb211350ce0f988'
client = Client(account_sid, auth_token)


def send_sms(user_code, phone_number):
    message = client.messages.create(
                                    body=f'Hola Este es Tu numero de Verificacion {user_code}',
                                    from_='+13204464923',
                                    to=f'{phone_number}'
                                )
    print(message.sid)
