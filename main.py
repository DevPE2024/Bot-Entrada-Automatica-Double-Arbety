import datetime
import telebot
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import tkinter as tk
from tkinter import ttk
from telethon import TelegramClient, events
import telethon
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from telethon.tl.types import MessageEmpty


class WebScraper:

    def __init__(self):
        # EDIT!

        self.api_id = 23308273
        self.api_hash = 'a807767851c060e773ec73cd2d2cb111'
        self.client = TelegramClient(
            'session_name', self.api_id, self.api_hash)
        self.client.start(force_sms=False)
        self.game = "Double"
        self.token = '6240343377:AAHSgzfJiOl1ojjc1DhYyFTXls-OtI9R2bQ'
        self.chat_id = '-1001954316479'
        self.direction_color = 'None'
        self.service = ChromeService(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--profile-directory=Default')
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-logging")
        self.options.add_argument("--disable-login-animations")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--disable-default-apps")
        self.options.add_argument("--disable-popup-blocking")

        self.driver = None

        # MAYBE EDIT!
        self.win_results = 0
        self.loss_results = 0
        self.max_hate = 0
        self.win_hate = 0
        self.stop = 0.0
        self.win = 0.0
        self.parar = 0
        # NO EDIT!
        self.count = 0
        self.analisar = True
        self.alvo = 0
        self.message_delete = False
        self.bot = telebot.TeleBot(token=self.token, parse_mode='MARKDOWN')
        self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))
        self.check_date = self.date_now
        self.protection = True
        self.ok = 0
        self.VERMELHO = ['1', '2', '3', '4', '5', '6', '7']
        self.VERDE = ['8', '9', '10', '11', '12', '13', '14']

        self.janela = tk.Tk()
        self.janela.title("Double Bot")

        self.combo = ttk.Label(self.janela, text="Valor Entrada:")
        self.combo.pack()
        self.combo = ttk.Entry(self.janela)
        self.combo.pack()

        self.combo5 = ttk.Label(self.janela, text="Valor Branco:")
        self.combo5.pack()
        self.combo5 = ttk.Entry(self.janela)
        self.combo5.pack()

        self.combo2 = ttk.Label(self.janela, text="Stop Win:")
        self.combo2.pack()
        self.combo2 = ttk.Entry(self.janela)
        self.combo2.pack()

        self.combo3 = ttk.Label(self.janela, text="Stop Loss:")
        self.combo3.pack()
        self.combo3 = ttk.Entry(self.janela)
        self.combo3.pack()

        self.botao = tk.Button(
            self.janela, text="Executar", command=self.executar)
        self.botao.pack()

        self.janela.mainloop()

    def initialize_browser(self):
        self.driver = webdriver.Chrome(
            options=self.options, service=self.service)
        return self.driver

    def pegar_resultado(self):
        self.element = self.driver.find_element(By.CLASS_NAME, 'items')
        self.divs = self.element.find_elements(
            By.XPATH, './/div[@style="opacity: 1;"]')

        r = []
        for div in self.divs:
            r.append(div.text)

        r.reverse()

        return r

    def results(self):

        if self.win_results + self.loss_results != 0:
            a = 100 / (self.win_results + self.loss_results) * self.win_results
        else:
            a = 0
        self.win_hate = (f'{a:,.2f}%')

        self.bot.send_message(chat_id=self.chat_id, text=(f'''
► PLACAR GERAL = ✅{self.win_results}  |  🚫{self.loss_results} 
► Consecutivas = {self.max_hate}
► Assertividade = {self.win_hate}
► Saldo: R${self.saldo}
    
    '''))
        return

    def gale(self, cont):
        saldo = self.pegar_saldo()
        self.banca_gale1 = float(self.valor_banca)
        self.banca_gale1 *= (2*cont)
        self.cobrir_gale1 = float(self.valor_cobrir)
        self.cobrir_gale1 *= (2*cont)

        if saldo < self.banca_gale1:
            self.bot.send_message(chat_id=self.chat_id, text=(
                "Banca Insuficiente para o gale"))
        else:
            if self.direction_color == '🔴' and float(self.valor_cobrir) > 0:
                self.jogar_vermelho(self.banca_gale1, self.cobrir_gale1)

            elif self.direction_color == '🔴' and float(self.valor_cobrir) == 0:
                self.jogar_vermelho_sem_cobrir(self.banca_gale1)

            if self.direction_color == '🟢' and float(self.valor_cobrir) > 0:
                self.jogar_verde(self.banca_gale1, self.cobrir_gale1)

            elif self.direction_color == '🟢' and float(self.valor_cobrir) == 0:
                self.jogar_verde_sem_cobrir(self.banca_gale1)

        # self.check_results()
        return

    def pegar_saldo(self):
        saldo_string = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/header/div/div/div/div[2]/div[1]/div').text
        saldo_sem_simbolo = saldo_string.replace("R$", "").replace(",", ".")
        saldo_float = float(saldo_sem_simbolo)
        return saldo_float

    def alert_gale(self, cont):
        self.gale_1(cont)

    def martingale(self, result):

        if result == "WIN":
            print(f"WIN")
            self.saldo = self.pegar_saldo()
            self.win_results += 1
            self.max_hate += 1
            self.bot.send_message(chat_id=self.chat_id,
                                  text=(f'''✅✅✅ WIN ✅✅✅'''))
            self.ok = 0
            self.parar = 1
            self.count = 0
            self.direction_color = 'None'
            self.results()
            return
        elif result == "LOSS":
            print(f"LOSS")
            self.saldo = self.pegar_saldo()
            self.loss_results += 1
            self.max_hate = 0
            self.bot.send_message(
                chat_id=self.chat_id, text=(f'''🚫🚫🚫 LOSS 🚫🚫🚫'''))
            self.ok = 0
            self.parar = 1
            self.count = 0
            self.direction_color = 'None'
            self.results()
            return

    def jogar_vermelho(self, banca, cobrir):
        wait = WebDriverWait(self.driver, 200)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="betValue"]')))

        elem = self.driver.find_element(By.XPATH, '//*[@id="betValue"]')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(banca))

        botao_verm = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/div[2]/div/div[1]').click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/button')))
        botao_verde = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/button')
        botao_verde.click()
        botao_branco = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/div[2]/div/div[2]').click()
        #
        elem2 = self.driver.find_element(By.XPATH, '//*[@id="betValue"]')
        elem2.click()
        elem2.send_keys(Keys.CONTROL + 'a')
        elem2.send_keys(str(cobrir))
        botao_verde.click()
        self.direction_color = '🔴'
        self.ok = 3

        return

    def jogar_vermelho_sem_cobrir(self, banca):
        wait = WebDriverWait(self.driver, 200)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="betValue"]')))

        elem = self.driver.find_element(By.XPATH, '//*[@id="betValue"]')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(banca))

        botao_verm = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/div[2]/div/div[1]').click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/button')))
        botao_verde = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/button')
        botao_verde.click()
        self.direction_color = '🔴'
        self.ok = 3

        return

    def jogar_verde(self, banca, cobrir):
        wait = WebDriverWait(self.driver, 200)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="betValue"]')))

        elem = self.driver.find_element(By.XPATH, '//*[@id="betValue"]')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(banca))

        botao_verm = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/div[2]/div/div[3]').click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/button')))
        botao_verde = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/button')
        botao_verde.click()
        botao_branco = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/div[2]/div/div[2]').click()
        #
        elem2 = self.driver.find_element(By.XPATH, '//*[@id="betValue"]')
        elem2.click()
        elem2.send_keys(Keys.CONTROL + 'a')
        elem2.send_keys(str(cobrir))
        botao_verde.click()
        self.direction_color = '🟢'
        self.ok = 3

        return

    def jogar_verde_sem_cobrir(self, banca):
        wait = WebDriverWait(self.driver, 200)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="betValue"]')))

        elem = self.driver.find_element(By.XPATH, '//*[@id="betValue"]')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(banca))

        botao_verm = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/div[2]/div/div[3]').click()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/button')))
        botao_verde = self.driver.find_element(
            By.XPATH, '//*[@id="root"]/div[6]/div/div[2]/main/div[1]/div/div[1]/div/div[1]/div/div/button')
        botao_verde.click()
        self.direction_color = '🟢'
        self.ok = 3

        return

    def checar(self, results):
        print(f"Ultimos Resultados:{results[:5]}\n")
        time.sleep(1)
        if results[0] in self.VERMELHO and self.direction_color == '🔴':
            self.martingale('WIN')
            return
        elif results[0] in self.VERMELHO and self.direction_color == '🟢':
            self.martingale('LOSS')
            return
        if results[0] in self.VERDE and self.direction_color == '🟢':
            self.martingale('WIN')
            return
        elif results[0] in self.VERDE and self.direction_color == '🔴':
            self.martingale('LOSS')
            return
        if results[0] == '0' and self.protection == True:
            self.martingale('WIN')
            return
        elif results[0] == '0' and self.protection == False:
            self.martingale('LOSS')
            return

    def check_results(self):
        check = []
        results = []
        check = self.pegar_resultado()
        time.sleep(1)
        results = check

        while self.parar == 0:
            try:
                time.sleep(1.5)
                results = self.pegar_resultado()
                if check[:5] != results[:5]:
                    self.parar = 1
                    self.checar(results)
                    break
            except:
                self.parar = 0
        return

    async def monitor_deleted_messages(self):

        # Obter as mensagens recentes do grupo
        messages = await self.client.get_messages(-1001865945986, limit=100)

        # Verificar se as mensagens anteriores foram excluídas
        for previous_message in self.previous_messages:
            if previous_message not in messages and not isinstance(previous_message, MessageEmpty):
                deleted_message_text = previous_message.text

        self.previous_messages = messages[:5]
        self.previous_messages2 = messages[:8]

    def start(self):
        self.previous_messages = []
        driver = self.initialize_browser()
        driver.maximize_window()
        driver.get(
            "https://www.arbety.com/games/double")
        input('ENTER PARA COMECAR')
        self.saldo = self.pegar_saldo()
        self.win = float(self.saldo) + float(self.stop_win)
        self.stop = float(self.saldo) - float(self.stop_loss)

        print(f'Saldo R${self.saldo}')
        print(f'Stop Win: R${self.win}')
        print(f'Stop Loss R${self.stop}\n')

        @self.client.on(events.NewMessage(chats=-1001865945986))
        async def my_event_handler(event):

            if isinstance(event.message, telethon.tl.custom.message.Message):
                text = event.message.message
                if self.saldo >= self.win or self.saldo <= self.stop:
                    if self.saldo >= self.win:
                        print(f"Atingiu seu Stop Win de R${self.win}")

                    elif self.saldo <= self.stop:
                        print(f"Atingiu seu Stop Loss de R${self.stop}")

                else:
                    if "🔴 VERMELHA 🔴" in text and (self.ok == 0 and float(self.valor_cobrir) > 0):

                        self.jogar_vermelho(
                            float(self.valor_banca*1), float(self.valor_cobrir*1))
                        return
                    elif "🔴 VERMELHA 🔴" in text and (self.ok == 0 and float(self.valor_cobrir) == 0):

                        self.jogar_vermelho_sem_cobrir(
                            float(self.valor_banca*1))
                        return
                    if "🟢 VERDE 🟢" in text and (self.ok == 0 and float(self.valor_cobrir) > 0):

                        self.jogar_verde(
                            float(self.valor_banca*1), float(self.valor_cobrir*1))
                        return
                    elif "🟢 VERDE 🟢" in text and (self.ok == 0 and float(self.valor_cobrir) == 0):

                        self.jogar_verde_sem_cobrir(
                            float(self.valor_banca*1))
                        return

                    if "🤞🏻 Façam a primeira proteção" in text and self.ok == 3:
                        self.gale(1)
                        return

                    if "Façam o CONTROLE DE PERDA 🔄🟠" in text and self.ok == 3:

                        self.martingale("LOSS")
                        return

                    if "✅✅✅" in text and self.ok == 3:

                        self.martingale("WIN")
                        return

        self.client.start()
        self.client.run_until_disconnected()

    def executar(self):

        self.valor_banca = self.combo.get()
        self.stop_win = self.combo2.get()
        self.stop_loss = self.combo3.get()
        self.valor_cobrir = self.combo5.get()
        self.start()


scraper = WebScraper()
scraper.start()
