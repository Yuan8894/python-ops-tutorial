"""
第四课：基于正则的日志错误提取与分析
当面对成百上千行的服务器日志时，手工排查是不现实的。
利用 `re` 模块，我们可以精准抓取带有 ERROR 或特定模式的崩溃日志。
"""
import re
from collections import Counter

def generate_sample_log():
    """生成一段模拟的 Nginx/应用服务器日志数据"""
    return [
        "2023-10-01 10:00:01 INFO [Auth] User admin logged in successfully",
        "2023-10-01 10:05:22 WARNING [DB] Connection to 192.168.1.100 is slow (1000ms)",
        "2023-10-01 10:06:05 ERROR [Payment] Timeout waiting for gateway response",
        "2023-10-01 10:15:30 INFO [User] Profile updated for ID: 88392",
        "2023-10-01 10:20:11 ERROR [Auth] Failed to authenticate user: session expired",
        "2023-10-01 10:25:00 ERROR [Payment] Timeout waiting for gateway response",
    ]

def analyze_logs():
    print("=" * 40)
    print("🔍 基于正则的智能日志错误提取")
    print("=" * 40)
    
    logs = generate_sample_log()
    
    # 编译一个正则表达式
    # 解释: 捕捉以日期时间开头，包含 ERROR 的行，并提取 [] 中的模块名
    # (?P<time>...) 命名捕获组，方便提取特定数据
    error_pattern = re.compile(r"^(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ERROR \[(?P<module>[a-zA-Z]+)\] (?P<msg>.*)$")
    
    error_count = 0
    module_counter = Counter()
    
    print("【发现的错误详情】")
    for line in logs:
        match = error_pattern.match(line)
        if match:
            error_count += 1
            time_str = match.group("time")
            module_name = match.group("module")
            msg = match.group("msg")
            
            # 记录哪个模块出错了，用来统计频率
            module_counter[module_name] += 1
            
            print(f"  -> [{time_str}] 模块: {module_name} | 详情: {msg}")
            
    print("\n【错误模块频率统计】")
    if error_count > 0:
        for mod, count in module_counter.most_common():
            print(f"  - {mod} : {count} 次报警")
    else:
        print("  - 太棒了！今天没有错误日志。")
        
    print("=" * 40)

if __name__ == "__main__":
    analyze_logs()
    print("\n💡 提示: 第五课我们将学习如何用 HTTP 发送监控告警 (如飞书/钉钉机器人的 Webhook)！")
