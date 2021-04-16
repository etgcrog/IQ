from utils.utils import configuracao
from iqoptionapi.stable_api import IQ_Option

config = configuracao()
username = config['email']
password = config['password']
balance = str(config['balance'])
API = IQ_Option(username, password)
API.connect()
API.change_balance(balance)
