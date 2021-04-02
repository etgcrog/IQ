from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
from dateutil import tz

# from selenium.webdriver.common.keys import Keys

ultima = 1
ultima_old = 0
filtro = ':rotating_light:'
ciclos = 1

print('Iniciando Bot...')
sleep(1)
print('Definindo Parametros')
sleep(1)
print('Verificando Arquivo')
sleep(3)
try:
    open(r'C:\Users\etgcr\Desktop\RoboBolsa\sinais.txt', 'r')
except FileNotFoundError:
    open(r'C:\Users\etgcr\Desktop\RoboBolsa\sinais.txt', 'w')
    print('Criando arquivo Sinais')
print('Limpando Arquivos Sinais')
open(r'C:\Users\etgcr\Desktop\RoboBolsa\sinais.txt', 'w')  # Zera arquivo sinais
sleep(5)
print('Bot Iniciado com Sucesso')
print('Aguardando por Sinais...')


class Encaminhar:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--lang-pt-BR')
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options = chrome_options)
        # self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(60)

    def timestamp_converter(self):
        hora = datetime.now()
        tm = tz.gettz('America/Sao Paulo')
        hora_atual = hora.astimezone(tm)
        return hora_atual.strftime('%H:%M')

    def chr_remove(self, old, to_remove):
        new_string = old
        for x in to_remove:
            new_string = new_string.replace(x, '')
        return new_string

    def iniciar(self):
        global ciclos
        self.driver.get('https://web.telegram.org/#/login')
        # url = self.driver.current_url
        autenticar_username = self.driver.find_element_by_xpath(
            '//*[@id="ng-app"]/body/div[1]/div/div[3]/div[2]/form/div[2]/div[2]/input')
        autenticar_username.send_keys('61999647890')
        proximo = self.driver.find_element_by_class_name('login_head_submit_btn')
        proximo.click()
        botao_ok = self.driver.find_element_by_xpath('//*[contains(text(), "OK")]')
        botao_ok.click()
        sleep(30)
        buscar = self.driver.find_element_by_xpath('//input[@placeholder="Buscar"]')
        buscar.send_keys("gri")
        encontrar_grilo = self.driver.find_element_by_xpath('//*[contains(text(), "Grilo")]')  # ACESSA O GRILO
        encontrar_grilo.click()
        sleep(5)
        self.ciclo()
        """
        <button class="btn btn-md btn-md-primary" ng-click="$dismiss()" my-focused="">
      <span my-i18n="modal_ok">OK</span>
    </button>
        """

    def standby(self):
        global ultima, ultima_old
        if str(ultima) == str(ultima_old):
            try:
            # self.driver.refresh()
            # sleep(30)
                elements = self.driver.find_elements_by_xpath('//div[@dir="auto"]')  # TESTAR PARA ÚLTIMAS MENSAGENS
                informacoes = []
                for n in range(len(elements)):
                    informacoes.append(elements[n].text)
                ultima = informacoes[-2]
            except:
                pass
        else:
            try:
                elements = self.driver.find_elements_by_xpath('//div[@dir="auto"]')  # TESTAR PARA ÚLTIMAS MENSAGENS
                informacoes = []
                for n in range(len(elements)):
                    informacoes.append(elements[n].text)
                ultima = informacoes[-2]
                ultima_old = ultima
                if filtro not in ultima:
                    pass
                else:
                    corrigido = ultima
                    corrigido = corrigido.replace(':rotating_light:', '🚨')
                    corrigido = corrigido.replace(':loudspeaker:', '📢')
                    corrigido = corrigido.replace(':bangbang:', '‼')
                    corrigido = corrigido.replace(':rooster:', '🐓')
                    corrigido = self.chr_remove(corrigido, "🚨🟢⏱📢 ‼🐓🛑 ️")  # Remove Emoji
                    corrigido = corrigido.replace("\n", ";")  # Coloca tudo na mesma linha
                    # print(corrigido)
                    if corrigido[6] == '-':  # Checar se é OTC
                        paridade = corrigido[0:10]  # Define Paridade
                        corrigido = corrigido.replace('-OTC', '')
                    else:
                        paridade = corrigido[0:6]  # Define a Paridade
                    direcao = corrigido[8:12]  # Define a Direção
                    direcao = self.chr_remove(direcao, "/")  # Remove / do PUT
                    # Remove Letras
                    novocorrigido = self.chr_remove(corrigido,
                                                    "ABCDEFGHIJKLMNOPQRSTUVWYXZÉÇÃçãabcdefghijklmnopqrstuvwyxz()/;")
                    horarioentrada = novocorrigido[1:6] + ':00'  # Define horario Entrada
                    horariosaida = novocorrigido[7:12] + ':00'  # Define horario Saida
                    entrada = self.chr_remove(horarioentrada[0:5], ":")  # Transforma em Inteiro
                    saida = self.chr_remove(horariosaida[0:5], ":")  # Transforma em Inteiro
                    if entrada[0:2] == saida[0:2]:
                        entrada = int(entrada)
                        saida = int(saida)
                        tempovela = str(saida - entrada)  # Diferença da Hora e String
                    else:
                        entrada = int(entrada)
                        saida = int(saida)
                        tempovela = str((saida - entrada) - 40)
                    tempovela = self.chr_remove(tempovela[0:2], "0")  # Remove os 0
                    # tempovelacru = int(tempovela)
                    tempovela = "M" + tempovela  # Formato M#
                    sinal = tempovela + ";" + paridade + ";" + horarioentrada + ";" + direcao
                    # print(paridade)
                    print(sinal)
                    with open(r'C:\Users\etgcr\Desktop\RoboBolsa\sinais.txt', 'a', encoding="utf-8") as ArquivoSinal:
                        print(sinal, file=ArquivoSinal)
            except:
                pass

    def ciclo(self):
        global ciclos
        while ciclos > 0:
            sleep(10)
            ciclos += 1
            self.standby()
            if ciclos == 10:
                ciclos = 1
                self.driver.refresh()
                # sleep(10)
                try:
                     botao_ok = self.driver.find_element_by_xpath('//*[contains(text(), "OK")]')
                     botao_ok.click()
                     buscar = self.driver.find_element_by_xpath('//input[@placeholder="Buscar"]')
                     buscar.send_keys("gri")
                     encontrar_grilo = self.driver.find_element_by_xpath('//*[contains(text(), "Grilo")]')  # ACESSA O GRILO
                     encontrar_grilo.click()
                except:
                    pass


if __name__ == '__main__':
    acessar = Encaminhar()
    acessar.iniciar()
