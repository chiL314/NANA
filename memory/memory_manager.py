# memory/memory_manager.py
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class MemoryManager:
    """
    分层记忆管理系统
    - 短期记忆：最近的对话历史（内存）
    - 长期记忆：重要事件和用户信息（持久化）
    """
    
    def __init__(self, memory_file="memory_data.json", max_short_term=15):
        self.memory_file = memory_file
        self.max_short_term = max_short_term
        
        # 短期记忆：最近的对话
        self.short_term_history: List[Dict] = []
        
        # 长期记忆：重要事件
        self.long_term_events: Dict[str, str] = {}
        
        # 用户事实库：持久化的用户信息
        self.user_facts: Dict[str, str] = {}
        
        # 加载历史记忆
        self.load_from_disk()
    
    def add_conversation(self, role: str, content: str):
        """添加一条对话到短期记忆"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.short_term_history.append(message)
        
        # 保持短期记忆在限制范围内
        if len(self.short_term_history) > self.max_short_term:
            self.short_term_history.pop(0)
        
        # 自动保存
        self.save_to_disk()
    
    def get_context_for_llm(self) -> List[Dict]:
        """
        获取用于 LLM 的上下文
        返回标准的 OpenAI 消息格式
        """
        # 只返回 role 和 content，去掉 timestamp
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.short_term_history
        ]
    
    def get_memory_summary(self) -> str:
        """
        获取记忆摘要，用于增强 system prompt
        使用紧凑格式以减少 token 消耗
        """
        summary_parts = []
        
        # 用户信息（紧凑格式）
        if self.user_facts:
            facts_str = ", ".join([f"{k}:{v}" for k, v in self.user_facts.items()])
            summary_parts.append(f"用户: {facts_str}")
        
        # 重要事件（只显示最近 3 个）
        if self.long_term_events:
            recent_events = list(self.long_term_events.items())[-3:]
            events_str = "; ".join([f"{date}:{event}" for date, event in recent_events])
            summary_parts.append(f"事件: {events_str}")
        
        return " | ".join(summary_parts) if summary_parts else ""
    
    def extract_important_info(self, llm_analysis: Dict):
        """
        从 LLM 分析结果中提取重要信息
        
        参数:
            llm_analysis: {
                "user_facts": {"职业": "程序员"},
                "events": {"2026-01-15": "今天有重要面试"}
            }
        """
        if "user_facts" in llm_analysis:
            self.user_facts.update(llm_analysis["user_facts"])
        
        if "events" in llm_analysis:
            self.long_term_events.update(llm_analysis["events"])
        
        self.save_to_disk()
    
    def save_to_disk(self):
        """持久化记忆到磁盘"""
        data = {
            "user_facts": self.user_facts,
            "long_term_events": self.long_term_events,
            "short_term_history": self.short_term_history[-50:],  # 只保存最近 50 条
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[!] 保存记忆失败: {e}")
    
    def load_from_disk(self):
        """从磁盘加载记忆"""
        if not os.path.exists(self.memory_file):
            return
        
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.user_facts = data.get("user_facts", {})
            self.long_term_events = data.get("long_term_events", {})
            self.short_term_history = data.get("short_term_history", [])
            
            print(f"✅ 已加载历史记忆（{len(self.short_term_history)} 条对话）")
        except Exception as e:
            print(f"[!] 加载记忆失败: {e}")
    
    def clear_old_events(self, days=30):
        """清理超过指定天数的旧事件"""
        from datetime import timedelta
        
        cutoff_date = (datetime.now() - timedelta(days=days)).date()
        
        old_events = {}
        for date_str, event in self.long_term_events.items():
            try:
                event_date = datetime.fromisoformat(date_str).date()
                if event_date >= cutoff_date:
                    old_events[date_str] = event
            except:
                # 保留无法解析日期的事件
                old_events[date_str] = event
        
        self.long_term_events = old_events
        self.save_to_disk()
