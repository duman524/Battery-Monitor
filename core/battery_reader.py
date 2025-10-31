"""
电池数据读取模块
"""

import psutil
from typing import Optional, Dict, Any
import time


class BatteryReader:
    """电池数据读取器"""
    
    def __init__(self):
        self.last_read_time = None
        self.cached_data = None
        self.cache_duration = 2  # 缓存时间(秒)
    
    def get_battery_info(self) -> Optional[Dict[str, Any]]:
        """
        获取电池信息
        
        Returns:
            Dict包含电池信息，如果无法获取返回None
        """
        try:
            # 检查缓存
            current_time = time.time()
            if (self.cached_data and self.last_read_time and 
                current_time - self.last_read_time < self.cache_duration):
                return self.cached_data
            
            battery = psutil.sensors_battery()
            
            if battery is None:
                return None
            
            data = {
                'percent': round(battery.percent),
                'plugged': battery.power_plugged,
                'secsleft': battery.secsleft,
                'timestamp': current_time
            }
            
            # 更新缓存
            self.cached_data = data
            self.last_read_time = current_time
            
            return data
            
        except Exception as e:
            print(f"读取电池信息时出错: {e}")
            return None
    
    def is_battery_available(self) -> bool:
        """检查电池是否可用"""
        try:
            battery = psutil.sensors_battery()
            return battery is not None
        except:
            return False


# 全局电池读取器实例
battery_reader = BatteryReader()