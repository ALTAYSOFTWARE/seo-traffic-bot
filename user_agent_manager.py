"""
User-Agent Yönetim Modülü
Farklı cihazlar için User-Agent'ları yönetir
"""

import random
import logging

logger = logging.getLogger(__name__)


class UserAgentManager:
    """User-Agent yöneticisi"""
    
    MOBILE_USER_AGENTS = [
        'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 11; ONEPLUS A6013) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 14; SM-A540F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; Redmi Note 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    ]
    
    TABLET_USER_AGENTS = [
        'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 13; SM-T870) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; SM-T820) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 14; Tab S9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    
    DESKTOP_USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]
    
    def __init__(self):
        """User-Agent Yöneticisini başlat"""
        logger.debug("UserAgentManager başlatıldı")
    
    def get_random_user_agent(self) -> str:
        """
        Rastgele bir User-Agent döndür
        
        Returns:
            User-Agent string'i
        """
        all_agents = self.MOBILE_USER_AGENTS + self.TABLET_USER_AGENTS + self.DESKTOP_USER_AGENTS
        return random.choice(all_agents)
    
    def get_mobile_user_agent(self) -> str:
        """
        Rastgele bir mobil User-Agent döndür
        
        Returns:
            Mobil User-Agent string'i
        """
        return random.choice(self.MOBILE_USER_AGENTS)
    
    def get_tablet_user_agent(self) -> str:
        """
        Rastgele bir tablet User-Agent döndür
        
        Returns:
            Tablet User-Agent string'i
        """
        return random.choice(self.TABLET_USER_AGENTS)
    
    def get_desktop_user_agent(self) -> str:
        """
        Rastgele bir masaüstü User-Agent döndür
        
        Returns:
            Masaüstü User-Agent string'i
        """
        return random.choice(self.DESKTOP_USER_AGENTS)
    
    @staticmethod
    def get_browser_from_user_agent(user_agent: str) -> str:
        """
        User-Agent'tan tarayıcı adını çıkar
        
        Args:
            user_agent: User-Agent string'i
        
        Returns:
            Tarayıcı adı
        """
        if 'Firefox' in user_agent:
            return 'Firefox'
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            return 'Safari'
        elif 'Chrome' in user_agent:
            return 'Chrome'
        elif 'Edge' in user_agent:
            return 'Edge'
        else:
            return 'Unknown'
