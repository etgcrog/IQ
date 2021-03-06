from bot.bot_telegram import Main
from utils.utils import carregaSinais, timestamp_converter

import time, sys, logging, utils

logging.disable(level=(logging.DEBUG))


class Operacao(Main):
    # def __init__subclass(self):
    #     Main.__init__(self)

    def __init__(self, ):
        Main.__init__(self)

    def Martingale(self, valor):
        # gale para recuperacao = 1.5 , gale para cobertura = 2.3
        lucro_esperado = float(valor) * 2.3
        # perca = valor

        # while True:
        # 	if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
        # 		return round(valor, 2)
        # 		break
        # 	valor += 0.01
        return float(lucro_esperado)

    def Payout(self, par, timeframe):
        self.API.subscribe_strike_list(par, timeframe)
        while True:
            d = self.API.get_digital_current_profit(par, timeframe)
            if d > 0:
                break
            time.sleep(1)
        self.API.unsubscribe_strike_list(par, timeframe)
        return float(d / 100)

    def entradas(self, par, entrada, direcao, opcao, timeframe):
        banca = self.banca()
        if opcao == 'digital':
            status, id = self.API.buy_digital_spot(
                par, entrada, direcao, timeframe)
            if status:
                # STOP WIN/STP LOSS

                banca_att = banca
                stop_loss = False
                stop_win = False

                if round((banca_att - float(self.config['banca_inicial'])), 2) <= (
                        abs(float(self.config['stop_loss'])) * -1.0):
                    stop_loss = True

                # if round((banca_att - float(config['banca_inicial'])) + (float(entrada) * float(config['payout'])) + float(entrada), 2) >= abs(float(config['stop_win'])):
                # 	stop_win = True
                if round((banca_att - float(self.config['banca_inicial'])), 2) >= abs(float(self.config['stop_win'])):
                    stop_win = True

                while True:
                    status, lucro = self.API.check_win_digital_v2(id)

                    if status:
                        if lucro >= 0:
                            return 'win', round(lucro, 2), stop_win
                        else:
                            return 'loss', round(lucro, 2), stop_loss
                        break
            else:
                return 'error', 0, False

        elif opcao == 'binaria':
            status, id = self.API.buy(entrada, par, direcao, timeframe)

            if status:
                lucro = self.API.check_win_v3(id)

                banca_att = banca
                stop_loss = False
                stop_win = False

                if round((banca_att - float(self.config['banca_inicial'])), 2) <= (
                        abs(float(self.config['stop_loss'])) * -1.0):
                    stop_loss = True

                if round((banca_att - float(self.config['banca_inicial'])), 2) >= abs(float(self.config['stop_win'])):
                    stop_win = True

                if lucro:
                    if lucro >= 0:
                        return 'win', round(lucro, 2), stop_win
                    else:
                        return 'loss', round(lucro, 2), stop_loss

            else:
                return 'error', 0, False
        else:
            return 'opcao errado', 0, False

    def Timeframe(self, timeframe):

        if timeframe == 'M1':
            return 1

        elif timeframe == 'M5':
            return 5

        elif timeframe == 'M15':
            return 15

        elif timeframe == 'H1':
            return 60
        else:
            return 'erro'

    def checkProfit(self, par, timeframe):
        all_asset = self.API.get_all_open_time()
        profit = self.API.get_all_profit()

        digital = 0
        binaria = 0

        if timeframe == 60:
            return 'binaria'

        if all_asset['digital'][par]['open']:
            digital = self.Payout(par, timeframe)
            digital = round(digital, 2)

        if all_asset['turbo'][par]['open']:
            binaria = round(profit[par]["turbo"], 2)

        if binaria < digital:
            return "digital"

        elif digital < binaria:
            return "binaria"

        elif digital == binaria:
            return "digital"

        else:
            "erro"

    def realizaoperacao(self):
        sinais = carregaSinais()
        for x in sinais:
            timeframe_retorno = self.Timeframe(x.split(';')[0])
            timeframe = 0 if (timeframe_retorno ==
                              'error') else timeframe_retorno
            par = x.split(';')[1].upper()
            minutos_lista = x.split(';')[2]
            direcao = x.split(';')[3].lower().replace('\n', '')
            mensagem_paridade = 'paridade a ser operada: ' + par + ' ' + '/' + ' ' + 'timeframe: ' + \
                                str(timeframe) + ' ' + '/' + ' ' + 'horario: ' + \
                                str(minutos_lista) + ' ' + '/' + ' ' + 'direcao: ' + direcao
            # self.Mensagem(mensagem_paridade)
            # print(par)
            while True:
                # payout = Payout(par,timeframe)
                # config['payout'] = payout
                minutos = timestamp_converter()

                # print(minutos_lista)
                # minutos_lista_parse = time.strptime(minutos_lista,'%H:%M:%S')
                # c = time.strftime('%H:%M:%S', minutos_lista_parse)
                # print(c)
                if minutos_lista < minutos:
                    break

                # minutos_segundos = minutos + ':00'
                minutos_replace = minutos.replace(':', '')
                minutos_lista_new = minutos_lista + ':00'
                minutos_lista_replace = minutos_lista_new.replace(':', '')
                dif = int(minutos_lista_replace) - int(minutos_replace)
                dif -= 40

                opcao = self.checkProfit(par, timeframe)
                entrar = True if (0 <= dif <= 14) else False
                # print('Hora de entrar?',entrar,'/ Minutos:',minutos)
                # print('Paridade',par)

                if entrar:
                    self.Mensagem('\n\nIniciando Operacao')
                    dir = False
                    dir = direcao

                    if dir:
                        mensagem_operacao = 'Paridade: ' + par + ' ' + '/' + ' ' + 'opcao: ' + opcao + ' ' + \
                                            '/' + ' ' + 'Horario: ' + \
                                            str(minutos_lista) + ' ' + \
                                            '/' + ' ' + 'Dire????o: ' + dir
                        self.Mensagem(mensagem_operacao)
                        valor_entrada = self.valor_entrada_b
                        opcao = 'binaria' if (opcao == 60) else opcao
                        resultado, lucro, stop = self.entradas(
                            par, valor_entrada, dir, opcao, timeframe)
                        mensagem_resultado = '   ->  ' + \
                                             resultado + ' / R$ ' + str(lucro)
                        self.Mensagem(mensagem_resultado)

                        if resultado == 'error':
                            break

                        if resultado == 'win':
                            break

                        if stop:
                            mensagem_stop = '\n\nStop ' + resultado.upper() + ' batido!'
                            self.Mensagem(mensagem_stop)
                            sys.exit()

                        if resultado == 'loss' and self.config['martingale'] == 'S':
                            valor_entrada = self.Martingale(
                                float(valor_entrada))
                            for i in range(int(self.config['niveis']) if int(self.config['niveis']) > 0 else 1):

                                mensagem_martingale = '   MARTINGALE NIVEL ' + \
                                                      str(i + 1) + '..'
                                self.Mensagem(mensagem_martingale)
                                resultado, lucro, stop = self.entradas(
                                    par, valor_entrada, dir, opcao, timeframe)
                                mensagem_resultado_martingale = ' ' + \
                                                                resultado + ' / R$ ' + str(lucro) + '\n'
                                self.Mensagem(mensagem_resultado_martingale)
                                if stop:
                                    mensagem_stop = '\n\nStop ' + resultado.upper() + ' batido!'
                                    self.Mensagem(mensagem_stop)
                                    sys.exit()

                                if resultado == 'win':
                                    print('\n')
                                    break
                                else:
                                    valor_entrada = self.Martingale(
                                        float(valor_entrada))

                            break
                        else:
                            break
                time.sleep(0.1)
            # break
        time.sleep(10)
        bot = Operacao()
        bot.realizaoperacao()
        # sys.exit()
