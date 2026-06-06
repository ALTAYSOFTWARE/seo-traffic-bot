"""
Google Arama Modülü
Google'da arama yapıp hedef siteyi bulur ve tıklar
"""

import logging
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class GoogleSearcher:
    """Google arama işlemleri"""
    
    GOOGLE_URL = "https://www.google.com"
    SEARCH_BOX_SELECTOR = "textarea.gLFyf"
    SEARCH_BUTTON_SELECTOR = "button[aria-label='Google Arama']"
    
    def __init__(self, google_url: str = GOOGLE_URL):
        """
        Google Searcher'ı başlat
        
        Args:
            google_url: Google URL'i
        """
        self.google_url = google_url
        logger.debug("GoogleSearcher başlatıldı")
    
    def go_to_google(self, driver: webdriver.Chrome) -> bool:
        """
        Google'a git
        
        Args:
            driver: WebDriver
        
        Returns:
            Başarı durumu
        """
        try:
            logger.info("Google'a gidiliyor...")
            driver.get(self.google_url)
            
            # Sayfanın yüklenmesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_BOX_SELECTOR))
            )
            
            time.sleep(1)
            logger.info("Google sayfası yüklendi")
            return True
        
        except TimeoutException:
            logger.error("Google sayfası yükleme zaman aşımı")
            return False
        except Exception as e:
            logger.error(f"Google sayfasına gitme hatası: {e}")
            return False
    
    def search_keyword(self, driver: webdriver.Chrome, keyword: str) -> bool:
        """
        Google'da anahtar kelime ara
        
        Args:
            driver: WebDriver
            keyword: Arama anahtar kelimesi
        
        Returns:
            Başarı durumu
        """
        try:
            logger.info(f"'{keyword}' aranıyor...")
            
            # Arama kutusunu bul
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.SEARCH_BOX_SELECTOR))
            )
            
            # Tıkla ve temizle
            search_box.click()
            search_box.clear()
            time.sleep(0.5)
            
            # Anahtar kelimeyi yaz
            search_box.send_keys(keyword)
            time.sleep(1)
            
            # Enter'e bas veya arama düğmesine tıkla
            search_box.send_keys(Keys.RETURN)
            
            # Sonuçların yüklenmesini bekle
            time.sleep(3)
            logger.info(f"Arama sonuçları yüklendi")
            return True
        
        except TimeoutException:
            logger.error("Arama kutusu bulma zaman aşımı")
            return False
        except Exception as e:
            logger.error(f"Arama hatası: {e}")
            return False
    
    def find_and_click_url(self, driver: webdriver.Chrome, target_url: str) -> bool:
        """
        Arama sonuçlarında hedef URL'yi bul ve tıkla
        
        Args:
            driver: WebDriver
            target_url: Hedef URL
        
        Returns:
            Başarı durumu
        """
        try:
            logger.info(f"'{target_url}' aranıyor...")
            
            # Arama sonuçlarını al
            search_results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href]"))
            )
            
            # Hedef URL'yi ara
            found = False
            for result in search_results:
                href = result.get_attribute('href')
                
                if href and target_url in href:
                    logger.info(f"Hedef URL bulundu: {href}")
                    
                    # Linke tıkla
                    driver.execute_script("arguments[0].scrollIntoView();", result)
                    time.sleep(1)
                    
                    # Yeni sekme açılmasını engelle
                    result.click()
                    
                    # Sayfanın yüklenmesini bekle
                    time.sleep(3)
                    found = True
                    logger.info("URL başarıyla tıklandı")
                    break
            
            if not found:
                logger.warning(f"Hedef URL bulunamadı: {target_url}")
                return False
            
            return True
        
        except TimeoutException:
            logger.error("Arama sonuçları yükleme zaman aşımı")
            return False
        except Exception as e:
            logger.error(f"URL bulma/tıklama hatası: {e}")
            return False
    
    def search_and_click(self, driver: webdriver.Chrome, keyword: str, 
                         target_url: str, timeout: int = 30) -> bool:
        """
        Google'da ara ve hedef URL'ye tıkla
        
        Args:
            driver: WebDriver
            keyword: Arama anahtar kelimesi
            target_url: Hedef URL
            timeout: Zaman aşımı (saniye)
        
        Returns:
            Başarı durumu
        """
        try:
            start_time = time.time()
            
            # Google'a git
            if not self.go_to_google(driver):
                return False
            
            # Anahtar kelimeyi ara
            if not self.search_keyword(driver, keyword):
                return False
            
            # Hedef URL'yi bul ve tıkla
            if not self.find_and_click_url(driver, target_url):
                return False
            
            elapsed_time = time.time() - start_time
            logger.info(f"Arama ve tıklama işlemi {elapsed_time:.1f} saniyede tamamlandı")
            return True
        
        except Exception as e:
            logger.error(f"Arama ve tıklama işlemi hatası: {e}")
            return False
    
    def get_search_result_count(self, driver: webdriver.Chrome) -> Optional[str]:
        """
        Arama sonuç sayısını al
        
        Args:
            driver: WebDriver
        
        Returns:
            Sonuç sayısı string'i
        """
        try:
            # Sonuç sayısını bul
            result_stats = driver.find_element(By.ID, "result-stats")
            count_text = result_stats.text
            logger.info(f"Arama sonuç sayısı: {count_text}")
            return count_text
        
        except NoSuchElementException:
            logger.warning("Sonuç sayısı bulunamadı")
            return None
        except Exception as e:
            logger.error(f"Sonuç sayısı alma hatası: {e}")
            return None
    
    def get_search_results_links(self, driver: webdriver.Chrome, limit: int = 10) -> list:
        """
        Arama sonuçlarındaki linkleri al
        
        Args:
            driver: WebDriver
            limit: Alınacak maksimum link sayısı
        
        Returns:
            Link listesi
        """
        try:
            links = []
            search_results = driver.find_elements(By.CSS_SELECTOR, "a[href]")
            
            for result in search_results[:limit]:
                href = result.get_attribute('href')
                title = result.text
                
                if href and title and not href.startswith('javascript'):
                    links.append({'url': href, 'title': title})
            
            logger.info(f"{len(links)} link alındı")
            return links
        
        except Exception as e:
            logger.error(f"Link alma hatası: {e}")
            return []
