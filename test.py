#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

good_leagues = {"CHN 1", "MEX 1", "GER 1", "FRA 1", "ESP 1", "ENG 1", "ENG 2" "ITA 1",
                "MLS", "BEL 1", "SAU 1", "NED", "POR 1", "LIB", "SUD"}
class BPM():
    def __init__(self, num_transfer_slots_filled, chrome_profile=None):
        super().__init__()
        self.num_transfer_slots_filled = num_transfer_slots_filled
        self.chrome_profile = chrome_profile
        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        if chrome_profile is not None:
            options.add_argument("user-data-dir=" + chrome_profile)
        self.browser = webdriver.Chrome(chrome_options=options)
        self.web_app_url = 'https://www.easports.com/fifa/ultimate-team/web-app/'
        self.browser.get(self.web_app_url)
        self.login_button_class = 'btn-standard.call-to-action'
        self.store_button_class = 'ut-tab-bar-item.icon-store'
        self.bronze_pack_class = 'currency call-to-action coins'
        self.info_change_button = 'ut-iteminfochange-button-control'

    def login(self):
        body = self.browser.find_element_by_tag_name('body')
        self.browser.implicitly_wait(30)
        # try:
        #     login_button = WebDriverWait(self.browser, 40).until(
        #         EC.element_to_be_clickable((By.CLASS_NAME, self.login_button_class))
        #     )
        # finally:
        #     self.browser.quit()
        
        time.sleep(5)
        login_button = body.find_element_by_class_name(self.login_button_class)
        
        login_button.click()
        if self.chrome_profile is None:
            print("Please login to your EA Account on the browser.")
            input("Press enter after logging in.")
            time.sleep(1)
            self.browser.fullscreen_window()

    
    def click_store(self):
        body = self.browser.find_element_by_tag_name('body')
        self.browser.implicitly_wait(30)
        store_button = body.find_element_by_class_name(self.store_button_class)
        store_button.click()
        # WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, self.store_button_class)))
    
    def click_bronze_tab(self):
        body = self.browser.find_element_by_tag_name('body')
        self.browser.implicitly_wait(30)
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "BRONZE"))).click()
    
    def click_my_packs_tab(self):
        body = self.browser.find_element_by_tag_name('body')
        self.browser.implicitly_wait(30)
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "MY PACKS"))).click()
            
    def open_my_pack(self):
        packs = bpm.browser.find_element_by_tag_name('body'
            ).find_elements_by_xpath("//*[contains(text(), 'Open')]")
        packs[0].click()
    
    def sort_my_pack(self):
        lists = self.browser.find_element_by_tag_name('body'
             ).find_elements_by_class_name('sectioned-item-list')
        self.store_all_in_club()
        if len(lists) == 2:
            time.sleep(1.5)
            self.quick_sell_all()
        else:
            return
        
    def purchase_bronze_pack(self):
        body = self.browser.find_element_by_tag_name('body')
        self.browser.implicitly_wait(30)
        buttons = body.find_element_by_class_name('ut-store-hub-view--content').find_elements_by_tag_name('button')
        buttons[2].click()
        time.sleep(1.5)
        body = self.browser.find_element_by_class_name('dialog-body'
            ).find_elements_by_tag_name('button')[0].click()

    def sort_pack(self):
        self.store_all_in_club()
        time.sleep(1.5)
        if len(self.browser.find_element_by_tag_name('body'
             ).find_elements_by_class_name('sectioned-item-list')) == 0:
            return
        time.sleep(.25)
        self.process_coins()
        if len(self.browser.find_element_by_tag_name('body'
             ).find_elements_by_class_name('sectioned-item-list')) == 0:
            return
        time.sleep(1.5)
        self.handle_duplicates()

    def store_all_in_club(self):
        # Store everything we can
        body = self.browser.find_element_by_tag_name('body')
        store_all_button = body.find_element_by_class_name("ut-navigation-container-view--content"
            ).find_element_by_class_name('ut-section-header-view'
            ).find_element_by_tag_name('button')
        store_all_button.click()
    
    def handle_duplicates(self):
        fut_items = self.get_duplicate_items()
        num_items = len(fut_items)
        for i in range(num_items):
            item = self.get_duplicate_items()[0]
            self.process_item(item)
            time.sleep(1)

    def process_coins(self):
        unprocessed_item_lists = self.browser.find_element_by_tag_name('body'
             ).find_elements_by_class_name('sectioned-item-list')
        if len(unprocessed_item_lists) > 1:
            # Process packs/coins
            items = unprocessed_item_lists[0].find_elements_by_class_name('listFUTItem')
            num_items = len(items)
            for i in range(num_items):
                item = unprocessed_item_lists[0].find_elements_by_class_name('listFUTItem')[0]
                self.process_pack_or_coin(item)

    def get_duplicate_items(self):
        return self.browser.find_element_by_tag_name('body'
            ).find_element_by_class_name('ut-content'
            ).find_elements_by_class_name('listFUTItem')

    def process_item(self, fut_item):
        l = fut_item.text.split('\n')
        # Not a player
        if len(l) < 12:
            # Quick Sell
            print('not a player')
            self.quick_sell_item()
        # Is a player
        else:
            league = l[1]
            if league in good_leagues:
                print('good player')
                self.num_transfer_slots_filled += 1
                self.send_item_to_transfers()
            else:
                print('bad player')
                self.quick_sell_item()
    
    def process_pack_or_coin(self, item):
        if item.text.find('Coin') != -1:
            self.browser.find_element_by_tag_name('body'
                ).find_element_by_xpath("//*[contains(text(), 'Redeem Coins')]").click()
        if item.text.find('Pack') != -1 :
            self.browser.find_element_by_tag_name('body'
                ).find_element_by_xpath("//*[contains(text(), 'Redeem Pack')]").click()

            
    def quick_sell_item(self):
        self.browser.find_element_by_tag_name('body'
            ).find_elements_by_xpath("//*[contains(text(), 'Quick Sell')]")[1].click()
        time.sleep(.75)
        self.browser.find_element_by_tag_name('body'
            ).find_element_by_class_name('dialog-body'
            ).find_element_by_tag_name('button').click()
    
    def quick_sell_all(self):
        self.browser.find_element_by_tag_name('body'
            ).find_elements_by_xpath("//*[contains(text(), 'Quick Sell')]")[0].click()
        time.sleep(.75)
        self.browser.find_element_by_tag_name('body'
            ).find_element_by_class_name('dialog-body'
            ).find_element_by_tag_name('button').click()
    
    def change_info(self):
        self.browser.find_element_by_tag_name('body'
            ).find_element_by_class_name(self.info_change_button).click()
    
    def send_item_to_transfers(self):
        self.browser.find_element_by_tag_name('body'
            ).find_elements_by_xpath("//*[contains(text(), 'Send to Transfer List')]")[1].click()
    
    def pack_loop(self):
        self.click_store()
        time.sleep(2)
        self.click_bronze_tab()
        time.sleep(1)
        self.purchase_bronze_pack()
        time.sleep(3)
        self.sort_pack()
    
    def open_my_pack_loop(self):
        self.click_store()
        time.sleep(1)
        self.open_my_pack()
        time.sleep(3)
        self.sort_my_pack()

    def pack_opener(self):
        self.click_store()
        packs_remaining = len(self.browser.find_element_by_tag_name('body'
            ).find_elements_by_xpath("//*[contains(text(), 'Open')]"))
        for i in range(packs_remaining):
            print('Packs Remaining: ' + str(packs_remaining - i) + '/' + str(packs_remaining))
            time.sleep(1)
            self.open_my_pack_loop()

    def run(self):
        self.change_info()
        num_packs_opened = 0
        while self.num_transfer_slots_filled < 98:
            print("Transfer Slots Remaining: " + str(self.num_transfer_slots_filled) + "/100")
            time.sleep(1)
            self.pack_loop()
            num_packs_opened += 1
            print('Number of Packs Opened: ' + str(num_packs_opened))
    
    def run_n(self, n):
        num_packs_opened = 0
        while num_packs_opened < n and self.num_transfer_slots_filled < 98:
            print("Transfer Slots Remaining: " + str(self.num_transfer_slots_filled) + "/100")
            time.sleep(1)
            self.pack_loop()
            num_packs_opened += 1
            print('Number of Packs Remaining: ', str(n-num_packs_opened))
    
#%%
slots = int(input('Please enter the number of filled transfer slots: '))

bpm = BPM(slots, chrome_profile='C:\\Users\\aluru\\AppData\\Local\\Google\\Chrome\\User Data')
# bpm.login()
time.sleep(30)
bpm.change_info()
time.sleep(1)
bpm.pack_opener()

#bpm.run_n(50)
# %%
