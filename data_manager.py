"""
Veri Yönetim Modülü
Konfigürasyon ve veri dosyalarının yönetimini sağlar
"""

import json
import logging
import os
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class DataManager:
    def __init__(self, config_file: str = 'config.json'):
        """
        Veri Yöneticisini başlat
        
        Args:
            config_file: Konfigürasyon dosyası yolu
        """
        self.config_file = config_file
        self.config_path = Path(config_file)
        self.config = {}
    
    def load_config(self) -> Dict[str, Any]:
        """
        Konfigürasyon dosyasını yükle
        
        Returns:
            Konfigürasyon sözlüğü
        """
        try:
            if self.config_path.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"Konfigürasyon yüklendi: {self.config_file}")
            else:
                logger.warning(f"Konfigürasyon dosyası bulunamadı: {self.config_file}")
                self.config = self._get_default_config()
                self.save_config()
        except json.JSONDecodeError as e:
            logger.error(f"Konfigürasyon dosyası parse hatası: {e}")
            self.config = self._get_default_config()
        except Exception as e:
            logger.error(f"Konfigürasyon yükleme hatası: {e}")
            self.config = self._get_default_config()
        
        return self.config
    
    def save_config(self) -> bool:
        """
        Konfigürasyonu dosyaya kaydet
        
        Returns:
            Başarı durumu
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info("Konfigürasyon kaydedildi")
            return True
        except Exception as e:
            logger.error(f"Konfigürasyon kaydetme hatası: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Konfigürasyon değeri al
        
        Args:
            key: Anahtar
            default: Varsayılan değer
        
        Returns:
            Değer
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        Konfigürasyon değeri ayarla
        
        Args:
            key: Anahtar
            value: Değer
        
        Returns:
            Başarı durumu
        """
        try:
            self.config[key] = value
            return self.save_config()
        except Exception as e:
            logger.error(f"Değer ayarlama hatası: {e}")
            return False
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Varsayılan konfigürasyon döndür"""
        return {
            'keyword': 'python programming tutorial',
            'target_url': 'https://example.com',
            'visit_count': 10,
            'delay_between_visits': 3600,
            'google_url': 'https://www.google.com',
            'search_result_timeout': 10,
            'enable_proxies': True,
            'random_click_probability': 0.4,
            'page_change_probability': 0.6,
            'min_visit_duration': 120,
            'max_visit_duration': 600
        }
    
    def validate_config(self) -> bool:
        """
        Konfigürasyonu doğrula
        
        Returns:
            Geçerlillik durumu
        """
        required_keys = ['keyword', 'target_url', 'visit_count']
        
        for key in required_keys:
            if key not in self.config:
                logger.error(f"Gerekli konfigürasyon anahtarı eksik: {key}")
                return False
        
        if not isinstance(self.config['visit_count'], int) or self.config['visit_count'] < 1:
            logger.error("visit_count 1'den büyük bir tam sayı olmalıdır")
            return False
        
        return True
    
    def print_config(self):
        """Konfigürasyonu yazdır"""
        print("\n" + "="*50)
        print("KONFIGÜRASYON")
        print("="*50)
        for key, value in self.config.items():
            print(f"{key}: {value}")
        print("="*50 + "\n")
