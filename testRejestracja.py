#import biblioteki

import unittest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from faker import Faker


class RejestracjaNowegoUzytkownika(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://eobuwie.com.pl/")
        self.driver.implicitly_wait(10)
        # Zamykam monit o ciasteczkach
        self.driver.find_element(By.CSS_SELECTOR, "button.button.base-button.primary.normal.green").click()
        # Ustawienie maksymalnego czasu bezarunkowego oczekiwania na elementy
        self.driver.implicitly_wait(10)
        # stworzenie instancji klasy Faker
        self.fake = Faker("pl_PL")

    def testNoEmailEntered(self):
        # KROKI
        # 1. Kliknij "Załóż konto"
        self.driver.find_element(By.XPATH, '(//button[@class="link"])[2]').click()
        # 2. Wpisz imię
        self.driver.implicitly_wait(10)
        sleep(5)
        imie_input = self.driver.find_element(By.NAME, "firstname")
        imie_input.send_keys(self.fake.first_name())
        # (3. Kliknij e-mail)
        self.driver.implicitly_wait(10)
        sleep(5)
        email_input = self.driver.find_element(By.ID, "email-register")
        email_input.click()
        # 4. Wpisz hasło
        self.driver.implicitly_wait(10)
        sleep(10)
        haslo_input = self.driver.find_element(By.ID, "password-register")
        haslo_input.send_keys(self.fake.password())
        # UWAGA! TUTAJ BĘDZIE TEST!
        # Oczekiwany rezultat:
        # Użytkownik otrzymuje informację „To pole jest wymagane” pod emailem
        # a) Szukam wszystkich wiadomości o błędzie użytkownika
        error_messages = self.driver.find_elements(By.CLASS_NAME, "error-msg")
        # b) Sprawdzam, czy jest tylko jeden błąd
        self.assertEqual(1, len(error_messages))
        # c) Sprawdzam treść i widoczność komunikatu („To pole jest wymagane”)
        self.assertEqual("To pole jest wymagane", error_messages[0].text)
        # d) Sprawdzam położenie komunikatu (czy jest pod emailem)
        # Odszukujemy lokator elementu względem innego elementu
        error_msg_locator = locate_with(By.CLASS_NAME, "error-msg") \
            .below({By.ID: "email-register"}).above({By.ID: "password-register"})
        # Szukamy (ponownie) komunikatu o błędzie (tym razem względem pola e-mail)
        error_message = self.driver.find_element(error_msg_locator)
        # Upewniam się, że komunikat o błędzie szukany dwoma metodami ten sam obiekt
        self.assertEqual(error_messages[0].id, error_message.id)

        # Poczekaj chwilę, żeby było można zobaczyć, co się dzieje. Do usunięcia po ukończeniu testu.
        sleep(3)

    def tearDown(self):
        self.driver.quit()




