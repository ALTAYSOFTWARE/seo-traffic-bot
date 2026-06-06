"""
Trafik Günlüğü Modülü
Ziyaret bilgilerini günlüğe kaydeder
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


class TrafficLogger:
    """Trafik günlüğü kaydedicisi"""
    
    def __init__(self, log_file: str = 'visits.json'):
        """
        Trafik Günlüğünü başlat
        
        Args:
            log_file: Günlük dosyası
        """
        self.log_file = log_file
        self.log_path = Path(log_file)
        self.visits = self._load_visits()
        logger.debug("TrafficLogger başlatıldı")
    
    def log_visit(self, visit_info: Dict) -> bool:
        """
        Ziyaret bilgisini günlüğe kaydet
        
        Args:
            visit_info: Ziyaret bilgileri sözlüğü
        
        Returns:
            Başarı durumu
        """
        try:
            self.visits.append(visit_info)
            return self._save_visits()
        except Exception as e:
            logger.error(f"Ziyaret günlüğe kaydetme hatası: {e}")
            return False
    
    def log_multiple_visits(self, visits: List[Dict]) -> bool:
        """
        Çoklu ziyareti günlüğe kaydet
        
        Args:
            visits: Ziyaret listesi
        
        Returns:
            Başarı durumu
        """
        try:
            self.visits.extend(visits)
            return self._save_visits()
        except Exception as e:
            logger.error(f"Çoklu ziyaret günlüğe kaydetme hatası: {e}")
            return False
    
    def _load_visits(self) -> List[Dict]:
        """
        Mevcut ziyaretleri yükle
        
        Returns:
            Ziyaret listesi
        """
        try:
            if self.log_path.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    visits = json.load(f)
                logger.info(f"{len(visits)} ziyaret yüklendi")
                return visits
            else:
                logger.debug("Günlük dosyası henüz oluşturulmadı")
                return []
        except json.JSONDecodeError:
            logger.warning("Günlük dosyası parse hatası, yeni dosya oluşturulacak")
            return []
        except Exception as e:
            logger.error(f"Ziyaret yükleme hatası: {e}")
            return []
    
    def _save_visits(self) -> bool:
        """
        Ziyaretleri dosyaya kaydet
        
        Returns:
            Başarı durumu
        """
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.visits, f, indent=2, ensure_ascii=False)
            logger.debug(f"Ziyaretler kaydedildi ({len(self.visits)} ziyaret)")
            return True
        except Exception as e:
            logger.error(f"Ziyaret kaydetme hatası: {e}")
            return False
    
    def get_visits(self) -> List[Dict]:
        """
        Tüm ziyaretleri al
        
        Returns:
            Ziyaret listesi
        """
        return self.visits.copy()
    
    def get_visits_by_device(self, device_type: str) -> List[Dict]:
        """
        Cihaz türüne göre ziyaretleri al
        
        Args:
            device_type: Cihaz türü (mobile, tablet, desktop)
        
        Returns:
            Filtrelenmiş ziyaret listesi
        """
        return [v for v in self.visits if v.get('device_type') == device_type]
    
    def get_visits_by_date(self, date: str) -> List[Dict]:
        """
        Tarihe göre ziyaretleri al
        
        Args:
            date: Tarih (YYYY-MM-DD formatında)
        
        Returns:
            Filtrelenmiş ziyaret listesi
        """
        return [v for v in self.visits if v.get('timestamp', '').startswith(date)]
    
    def get_successful_visits(self) -> List[Dict]:
        """
        Başarılı ziyaretleri al
        
        Returns:
            Başarılı ziyaretler
        """
        return [v for v in self.visits if v.get('success', False)]
    
    def get_failed_visits(self) -> List[Dict]:
        """
        Başarısız ziyaretleri al
        
        Returns:
            Başarısız ziyaretler
        """
        return [v for v in self.visits if not v.get('success', False)]
    
    def get_statistics(self) -> Dict:
        """
        İstatistikleri hesapla
        
        Returns:
            İstatistik sözlüğü
        """
        total = len(self.visits)
        successful = len(self.get_successful_visits())
        failed = total - successful
        
        total_duration = sum(v.get('duration', 0) for v in self.visits)
        avg_duration = total_duration / total if total > 0 else 0
        
        device_distribution = {}
        for visit in self.visits:
            device = visit.get('device_type', 'unknown')
            device_distribution[device] = device_distribution.get(device, 0) + 1
        
        browser_distribution = {}
        for visit in self.visits:
            browser = visit.get('browser', 'unknown')
            browser_distribution[browser] = browser_distribution.get(browser, 0) + 1
        
        return {
            'total_visits': total,
            'successful_visits': successful,
            'failed_visits': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'total_duration': total_duration,
            'average_duration': avg_duration,
            'device_distribution': device_distribution,
            'browser_distribution': browser_distribution
        }
    
    def print_statistics(self):
        """İstatistikleri yazdır"""
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("ZIYARET İSTATİSTİKLERİ")
        print("="*60)
        print(f"Toplam Ziyaret: {stats['total_visits']}")
        print(f"Başarılı: {stats['successful_visits']}")
        print(f"Başarısız: {stats['failed_visits']}")
        print(f"Başarı Oranı: {stats['success_rate']:.1f}%")
        print(f"Toplam Süre: {stats['total_duration']:.0f} saniye ({stats['total_duration']/60:.1f} dakika)")
        print(f"Ortalama Ziyaret Süresi: {stats['average_duration']:.1f} saniye")
        
        print("\nCihaz Dağılımı:")
        for device, count in stats['device_distribution'].items():
            print(f"  {device}: {count}")
        
        print("\nTarayıcı Dağılımı:")
        for browser, count in stats['browser_distribution'].items():
            print(f"  {browser}: {count}")
        
        print("="*60 + "\n")
    
    def export_to_csv(self, csv_file: str = 'visits.csv') -> bool:
        """
        Ziyaretleri CSV formatında dışa aktar
        
        Args:
            csv_file: CSV dosyası
        
        Returns:
            Başarı durumu
        """
        try:
            import csv
            
            if not self.visits:
                logger.warning("Dışa aktarılacak ziyaret yok")
                return False
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'timestamp', 'device_type', 'device_name', 'browser',
                    'ip_address', 'keyword', 'target_url', 'success', 'duration', 'pages_visited'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.visits)
            
            logger.info(f"CSV dosyasına dışa aktarıldı: {csv_file}")
            return True
        
        except Exception as e:
            logger.error(f"CSV dışa aktarma hatası: {e}")
            return False
    
    def clear_logs(self) -> bool:
        """
        Tüm günlükleri sil
        
        Returns:
            Başarı durumu
        """
        try:
            self.visits = []
            return self._save_visits()
        except Exception as e:
            logger.error(f"Günlük temizleme hatası: {e}")
            return False
