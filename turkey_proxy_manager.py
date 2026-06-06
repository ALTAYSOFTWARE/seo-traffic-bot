"""
Türkiye Proxy Yönetim Modülü
Türkiye kaynaklı proxy IP'lerini yönetir
"""

import random
import logging
import requests
from typing import List, Optional

logger = logging.getLogger(__name__)


class TurkeyProxyManager:
    """Türkiye proxy yöneticisi"""
    
    # Türkiye kaynaklı muhtemel proxy listesi
    # NOT: Gerçek proxy IP'lerini buraya eklemek gerekir
    TURKEY_PROXIES = [
        # Format: "IP:PORT"
        # Türkiye'de hizmet veren proxy IP'leri
        # Ücretsiz proxy kaynaklarından alabilir veya ücretli hizmetler kullanabilirsiniz
    ]
    
    # Alternatif proxy kaynakları
    PROXY_SOURCES = [
        'https://www.proxy-list.download/api/v1/get?type=http',
        'https://www.proxy-list.download/api/v1/get?type=socks4',
    ]
    
    def __init__(self):
        """Türkiye Proxy Yöneticisini başlat"""
        self.proxies = self.TURKEY_PROXIES.copy()
        self.current_index = 0
        logger.debug("TurkeyProxyManager başlatıldı")
    
    def get_random_proxy(self) -> Optional[str]:
        """
        Rastgele bir Türkiye proxy'si döndür
        
        Returns:
            Proxy adresi (IP:PORT) veya None
        """
        if not self.proxies:
            logger.warning("Kullanılabilir proxy bulunmuyor")
            return None
        
        proxy = random.choice(self.proxies)
        logger.debug(f"Seçilen proxy: {proxy}")
        return proxy
    
    def get_next_proxy(self) -> Optional[str]:
        """
        Sıradaki proxy'yi döndür (round-robin)
        
        Returns:
            Proxy adresi (IP:PORT) veya None
        """
        if not self.proxies:
            logger.warning("Kullanılabilir proxy bulunmuyor")
            return None
        
        proxy = self.proxies[self.current_index % len(self.proxies)]
        self.current_index += 1
        logger.debug(f"Sıradaki proxy: {proxy}")
        return proxy
    
    def add_proxy(self, proxy: str) -> bool:
        """
        Proxy listesine yeni proxy ekle
        
        Args:
            proxy: Proxy adresi (IP:PORT formatında)
        
        Returns:
            Başarı durumu
        """
        try:
            if proxy not in self.proxies:
                self.proxies.append(proxy)
                logger.info(f"Proxy eklendi: {proxy}")
                return True
            else:
                logger.warning(f"Proxy zaten var: {proxy}")
                return False
        except Exception as e:
            logger.error(f"Proxy ekleme hatası: {e}")
            return False
    
    def remove_proxy(self, proxy: str) -> bool:
        """
        Proxy listesinden proxy kaldır
        
        Args:
            proxy: Proxy adresi
        
        Returns:
            Başarı durumu
        """
        try:
            if proxy in self.proxies:
                self.proxies.remove(proxy)
                logger.info(f"Proxy kaldırıldı: {proxy}")
                return True
            else:
                logger.warning(f"Proxy bulunamadı: {proxy}")
                return False
        except Exception as e:
            logger.error(f"Proxy kaldırma hatası: {e}")
            return False
    
    def fetch_proxies_from_source(self) -> bool:
        """
        Online kaynaktan Türkiye proxy'lerini getir
        
        Returns:
            Başarı durumu
        """
        try:
            logger.info("Proxy kaynağından veri çekiliyor...")
            
            for source in self.PROXY_SOURCES:
                try:
                    response = requests.get(source, timeout=5)
                    if response.status_code == 200:
                        proxies = response.text.strip().split('\r\n')
                        self.proxies.extend([p for p in proxies if p])
                        logger.info(f"{len(proxies)} proxy eklendi")
                        return True
                except Exception as e:
                    logger.debug(f"Kaynak hatası ({source}): {e}")
                    continue
            
            logger.warning("Hiçbir kaynaktan proxy getirilemedi")
            return False
        
        except Exception as e:
            logger.error(f"Proxy getirme hatası: {e}")
            return False
    
    def test_proxy(self, proxy: str, timeout: int = 5) -> bool:
        """
        Proxy'nin çalışıp çalışmadığını test et
        
        Args:
            proxy: Proxy adresi
            timeout: Zaman aşımı (saniye)
        
        Returns:
            Çalışıp çalışmadığı
        """
        try:
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            response = requests.get('https://www.google.com', 
                                   proxies=proxies, 
                                   timeout=timeout)
            
            if response.status_code == 200:
                logger.info(f"Proxy çalışıyor: {proxy}")
                return True
            else:
                logger.warning(f"Proxy hata döndü: {proxy} (Status: {response.status_code})")
                return False
        
        except requests.exceptions.Timeout:
            logger.warning(f"Proxy zaman aşımı: {proxy}")
            return False
        except Exception as e:
            logger.warning(f"Proxy test hatası ({proxy}): {e}")
            return False
    
    def validate_proxies(self) -> int:
        """
        Tüm proxy'leri test et ve çalışmayanları kaldır
        
        Returns:
            Çalışan proxy sayısı
        """
        logger.info("Proxy'ler test ediliyor...")
        working_proxies = []
        
        for proxy in self.proxies:
            if self.test_proxy(proxy):
                working_proxies.append(proxy)
        
        self.proxies = working_proxies
        logger.info(f"{len(working_proxies)} çalışan proxy bulundu")
        return len(working_proxies)
    
    def get_proxy_count(self) -> int:
        """
        Mevcut proxy sayısını döndür
        
        Returns:
            Proxy sayısı
        """
        return len(self.proxies)
    
    def list_proxies(self) -> List[str]:
        """
        Tüm proxy'leri listele
        
        Returns:
            Proxy listesi
        """
        return self.proxies.copy()
    
    @staticmethod
    def is_valid_proxy_format(proxy: str) -> bool:
        """
        Proxy formatını kontrol et (IP:PORT)
        
        Args:
            proxy: Proxy string'i
        
        Returns:
            Geçerli olup olmadığı
        """
        try:
            parts = proxy.split(':')
            if len(parts) != 2:
                return False
            
            ip, port = parts
            port = int(port)
            
            if not (0 < port < 65535):
                return False
            
            ip_parts = ip.split('.')
            if len(ip_parts) != 4:
                return False
            
            for part in ip_parts:
                num = int(part)
                if not (0 <= num <= 255):
                    return False
            
            return True
        except (ValueError, AttributeError):
            return False
