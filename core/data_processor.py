"""
电池数据处理模块
"""

from typing import Dict, Any, Tuple
from config.settings import settings
import psutil

class DataProcessor:
    """电池数据处理器"""
    
    def process_battery_data(self, battery_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理电池数据
        
        Args:
            battery_data: 原始电池数据
            
        Returns:
            处理后的电池数据
        """
        if not battery_data:
            return self._get_default_data()
        
        percent = battery_data['percent']
        plugged = battery_data['plugged']
        secsleft = battery_data['secsleft']
        
        # 获取颜色级别
        color_level = self._get_battery_color(percent)
        
        # 获取状态文本
        status_text, time_text = self._get_status_texts(percent, plugged, secsleft)
        
        return {
            'percent': percent,
            'plugged': plugged,
            'secsleft': secsleft,
            'color': color_level,
            'status_text': status_text,
            'time_text': time_text,
            'raw_data': battery_data
        }
    
    def _get_battery_color(self, percent: int) -> str:
        """根据电量百分比获取对应的颜色"""
        if percent > settings.battery_levels['high']:
            return settings.colors['level_high']
        elif percent > settings.battery_levels['medium']:
            return settings.colors['level_medium']
        elif percent > settings.battery_levels['low']:
            return settings.colors['level_low']
        else:
            return settings.colors['level_critical']
    
    def _get_status_texts(self, percent: int, plugged: bool, secsleft: int) -> Tuple[str, str]:
        """获取状态文本和时间文本"""
        # 状态文本 - 简化为空字符串，因为我们不再显示状态
        status_text = ""
        
        # 时间文本 - 简化为空字符串，因为我们不再显示时间
        time_text = ""
        
        return status_text, time_text
    
    def _get_default_data(self) -> Dict[str, Any]:
        """获取默认数据（当无法读取电池信息时）"""
        return {
            'percent': 0,
            'plugged': False,
            'secsleft': psutil.POWER_TIME_UNKNOWN,
            'color': settings.colors['level_critical'],
            'status_text': "❌ 无法检测",
            'time_text': "检查电池状态",
            'raw_data': None
        }


# 全局数据处理器实例
data_processor = DataProcessor()