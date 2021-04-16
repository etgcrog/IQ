from datetime import datetime
from dateutil import tz


def timestamp_converter_segundos():
    hora = datetime.now()
    tm = tz.gettz('America/Sao Paulo')
    hora_atual = hora.astimezone(tm)
    return hora_atual.strftime('%S.%f')

print(timestamp_converter_segundos())

corecao_delay_entrada = 48
segundos_delay_entrada = timestamp_converter_segundos()
segundos_delay_entrada = segundos_delay_entrada.replace(':','')
segundos_delay_entrada = float(segundos_delay_entrada)
print(timestamp_converter_segundos())
segundos_delay_entrada = abs(segundos_delay_entrada - 60)
print(timestamp_converter_segundos())

if 0 <= segundos_delay_entrada <= 30:
    corecao_delay_entrada += segundos_delay_entrada

elif 30 <= segundos_delay_entrada <= 60:
     segundos_delay_entrada -= 60
     corecao_delay_entrada += segundos_delay_entrada
     if corecao_delay_entrada < 0:
         corecao_delay_entrada = 0


# minutos_lista = '15:03'
# minutos = timestamp_converter()
# print(type(minutos))
# minutos_lista_replace = minutos_lista.replace(':','')
# hora = int(minutos_lista_replace[:2])
# minuto = int(minutos_lista_replace[2:])
# if hora == 0:
#     hora = 24
# if minuto == 0:
#     hora -= 1
#     minuto = 59
# else:
#     minuto -= 1
# hora = '0' + str(hora) if (hora < 10) else str(hora)
# minuto = '0' + str(minuto) if (minuto < 10) else str(minuto)
# hora_entrada = hora + ':' + minuto + ':'
print(segundos_delay_entrada)
print(corecao_delay_entrada)