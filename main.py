#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google SEO Traffic Simulator
Özellikleri:
- Google'da anahtar kelimeyle arama yapıp sitenizi bulup tıklama
- Her ziyarette farklı cihaz, tarayıcı, konum simülasyonu
- Mobil, tablet, masaüstü karışık trafik
- Gerçek gezinme süresi ve sayfa geçişleri
- Türkiye kaynaklı gerçek IP'ler
- Ziyaret logları
- Bot imzası bırakmaz
"""

import time
import logging
import json
from datetime import datetime
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from data_manager import DataManager
from user_agent_manager import UserAgentManager
from turkey_proxy_manager import TurkeyProxyManager
from google_searcher import GoogleSearcher
from traffic_logger import TrafficLogger

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SEOTrafficSimulator:
    def __init__(self, config_file: str = 'config.json'):
        """
        SEO Traffic Simulator'ı başlat
        
        Args:
            config_file: Konfigürasyon dosyası
        """
        self.data_manager = DataManager(config_file)
        self.config = self.data_manager.load_config()
        self.user_agent_manager = UserAgentManager()
        self.proxy_manager = TurkeyProxyManager()
        self.google_searcher = GoogleSearcher()
        self.traffic_logger = TrafficLogger()
        self.visits = []
        
        logger.info("SEO Traffic Simulator başlatıldı")
    
    def _get_random_device(self) -> Dict:
        """Rastgele cihaz tipi seç"""
        devices = [
            {
                'type': 'mobile',
                'name': 'Samsung Galaxy S21',
                'width': 360,
                'height': 800,
                'user_agent': self.user_agent_manager.get_mobile_user_agent()
            },
            {
                'type': 'tablet',
                'name': 'iPad Pro',
                'width': 1024,
                'height': 1366,
                'user_agent': self.user_agent_manager.get_tablet_user_agent()
            },
            {
                'type': 'desktop',
                'name': 'Windows 10',
                'width': 1920,
                'height': 1080,
                'user_agent': self.user_agent_manager.get_desktop_user_agent()
            }
        ]
        return random.choice(devices)
    
    def _setup_chrome_driver(self, device: Dict, proxy: str) -> webdriver.Chrome:
        """
        Chrome WebDriver'ı konfigüre et
        
        Args:
            device: Cihaz bilgisi
            proxy: Proxy adresi (IP:PORT formatında)
        
        Returns:
            WebDriver örneği
        """
        chrome_options = Options()
        
        # User-Agent ayarı
        chrome_options.add_argument(f'user-agent={device["user_agent"]}')
        
        # Proxy ayarı
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
        
        # Bot tespit edici ayarları devre dışı bırak
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Başka bot buluştur ayarları
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        
        # Window boyutu
        chrome_options.add_argument(f'--window-size={device["width"]},{device["height"]}')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            # JavaScript bot algılamasını engelle
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
            return driver
        except Exception as e:
            logger.error(f"Chrome driver kurulum hatası: {e}")
            return None
    
    def _human_like_delay(self, min_delay: float = 1, max_delay: float = 5):
        """İnsana benzer gecikmeler ekle"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def _scroll_page(self, driver: webdriver.Chrome):
        """Sayfayı insan gibi kaydır"""
        # Rastgele scroll sayısı
        scroll_count = random.randint(2, 5)
        
        for _ in range(scroll_count):
            scroll_height = driver.execute_script("return window.innerHeight;")
            driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            self._human_like_delay(2, 4)
    
    def _visit_website(self, driver: webdriver.Chrome, url: str) -> bool:
        """
        Web sitesini ziyaret et
        
        Args:
            driver: WebDriver
            url: Ziyaret edilecek URL
        
        Returns:
            Başarılı olup olmadığı
        """
        try:
            logger.info(f"Ziyaret ediliyor: {url}")
            driver.get(url)
            
            # Sayfanın yüklenmesini bekle
            self._human_like_delay(3, 5)
            
            # Sayfayı oku ve kaydır
            self._scroll_page(driver)
            
            # Rastgele linklere tıkla
            if random.random() < 0.4:  # %40 ihtimalle başka sayfaya git
                self._click_random_link(driver)
            
            return True
        except Exception as e:
            logger.error(f"Ziyaret hatası: {e}")
            return False
    
    def _click_random_link(self, driver: webdriver.Chrome):
        """Sayfada rastgele bir linke tıkla"""
        try:
            links = driver.find_elements(By.TAG_NAME, "a")
            if links:
                random_link = random.choice(links)
                driver.execute_script("arguments[0].scrollIntoView();", random_link)
                self._human_like_delay(1, 2)
                random_link.click()
                self._human_like_delay(2, 4)
                logger.info("Rastgele linke tıklandı")
        except Exception as e:
            logger.debug(f"Link tıklatma hatası: {e}")
    
    def simulate_visit(self, keyword: str, target_url: str) -> Dict:
        """
        Tekil bir ziyareti simüle et
        
        Args:
            keyword: Arama anahtar kelimesi
            target_url: Hedef URL
        
        Returns:
            Ziyaret bilgileri
        """
        device = self._get_random_device()
        proxy = self.proxy_manager.get_random_proxy()
        
        visit_info = {
            'timestamp': datetime.now().isoformat(),
            'device_type': device['type'],
            'device_name': device['name'],
            'browser': 'Chrome',
            'ip_address': proxy.split(':')[0] if proxy else 'N/A',
            'keyword': keyword,
            'target_url': target_url,
            'success': False,
            'duration': 0,
            'pages_visited': 1
        }
        
        driver = None
        start_time = time.time()
        
        try:
            driver = self._setup_chrome_driver(device, proxy)
            if not driver:
                return visit_info
            
            # Google'da ara
            logger.info(f"'{keyword}' için Google araması yapılıyor")
            search_success = self.google_searcher.search_and_click(
                driver, keyword, target_url
            )
            
            if search_success:
                # Hedef URL'ye tıklandıktan sonra sayfayı gezin
                self._human_like_delay(2, 4)
                self._scroll_page(driver)
                
                # Ekstra sayfalar ziyaret et
                pages_visited = 1
                if random.random() < 0.6:  # %60 ihtimalle başka sayfaya git
                    try:
                        self._click_random_link(driver)
                        pages_visited += 1
                    except:
                        pass
                
                visit_info['success'] = True
                visit_info['pages_visited'] = pages_visited
                logger.info(f"Ziyaret başarılı: {pages_visited} sayfa")
            
        except Exception as e:
            logger.error(f"Ziyaret simülasyonu hatası: {e}")
        
        finally:
            if driver:
                driver.quit()
            
            visit_info['duration'] = time.time() - start_time
            self.visits.append(visit_info)
            self.traffic_logger.log_visit(visit_info)
        
        return visit_info
    
    def run_campaign(self, keyword: str, target_url: str, 
                    visit_count: int = 10, delay_between_visits: int = 3600):
        """
        Trafik kampanyası çalıştır
        
        Args:
            keyword: Arama anahtar kelimesi
            target_url: Hedef URL
            visit_count: Toplam ziyaret sayısı
            delay_between_visits: Ziyaretler arası gecikme (saniye)
        """
        logger.info(f"Kampanya başlatılıyor: '{keyword}' -> {target_url}")
        logger.info(f"Toplam ziyaret: {visit_count}")
        
        for i in range(visit_count):
            logger.info(f"Ziyaret {i+1}/{visit_count}")
            
            try:
                result = self.simulate_visit(keyword, target_url)
                
                if result['success']:
                    logger.info(f"Başarılı ziyaret: {result['device_type']}")
                else:
                    logger.warning(f"Başarısız ziyaret")
                
            except Exception as e:
                logger.error(f"Kampanya hatası: {e}")
            
            # Son ziyaret değilse bekle
            if i < visit_count - 1:
                logger.info(f"{delay_between_visits} saniye bekleniyor...")
                time.sleep(delay_between_visits)
        
        logger.info("Kampanya tamamlandı!")
        self.print_statistics()
    
    def print_statistics(self):
        """İstatistikleri yazdır"""
        if not self.visits:
            logger.info("Henüz ziyaret kaydı yok")
            return
        
        successful = sum(1 for v in self.visits if v['success'])
        total_duration = sum(v['duration'] for v in self.visits)
        
        logger.info("\n" + "="*50)
        logger.info("ZIYARET İSTATİSTİKLERİ")
        logger.info("="*50)
        logger.info(f"Toplam ziyaret: {len(self.visits)}")
        logger.info(f"Başarılı ziyaret: {successful}/{len(self.visits)}")
        logger.info(f"Başarı oranı: {(successful/len(self.visits)*100):.1f}%")
        logger.info(f"Toplam süre: {total_duration:.0f} saniye ({total_duration/60:.1f} dakika)")
        
        if self.visits:
            devices = {}
            for visit in self.visits:
                device = visit['device_type']
                devices[device] = devices.get(device, 0) + 1
            logger.info(f"Cihaz dağılımı: {devices}")
        
        logger.info("="*50 + "\n")


if __name__ == "__main__":
    simulator = SEOTrafficSimulator()
    
    # Konfigürasyondan kampanya ayarlarını oku
    config = simulator.config
    
    # Kampanyayı çalıştır
    simulator.run_campaign(
        keyword=config.get('keyword', 'python tutorial'),
        target_url=config.get('target_url', 'https://example.com'),
        visit_count=config.get('visit_count', 10),
        delay_between_visits=config.get('delay_between_visits', 3600)
    )
