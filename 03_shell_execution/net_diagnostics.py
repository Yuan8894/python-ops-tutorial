"""
第三课：强大的 Subprocess (子进程管理与诊断)
在运维中，我们常需要调用系统命令(如 ping, netstat)并根据结果执行下一步操作。
这个脚本演示了如何捕获命令的标准输出和错误。
"""
import subprocess
import platform

def check_ping(host="8.8.8.8"):
    print("=" * 40)
    print(f"🌐 网络连通性测试 (Ping: {host})")
    print("=" * 40)
    
    # 区分 Windows 和 Linux 的 ping 参数
    # Windows 下 -n 表示次数，Linux 下 -c 表示次数
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    
    try:
        # capture_output=True 让我们能拿到 stdout 字符串
        # text=True 将输出自动解码为字符串而不是 bytes格式
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        
        # 很多系统命令执行成功返回 0，失败返回 1 或其他非零状态码
        if result.returncode == 0:
            print(f"✅ [{host}] 访问正常！")
            
            # 简单从输出中找到耗时信息 (粗略演示)
            for line in result.stdout.split('\n'):
                if "ms" in line and ("time=" in line or "时间=" in line or "时间<" in line):
                    print(f"  详细回复: {line.strip()}")
        else:
            print(f"❌ [{host}] 网络不通！可以检查防火墙或网络配置。")
            if result.stderr:
                print(f"  错误信息: {result.stderr.strip()}")
            
    except Exception as e:
        print(f"执行 Ping 测试时发生异常: {e}")
    print("=" * 40)

def check_active_ports():
    print("=" * 40)
    print("🔌 端口监听状态扫描 (netstat)")
    print("=" * 40)
    
    command = ['netstat', '-an']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # 统计在监听 (LISTENING) 的 TCP 端口数量
        listen_count = 0
        print("发现以下本地监听的服务端口 (前 5 个):")
        for line in result.stdout.split('\n'):
            if 'LISTENING' in line or 'LISTENING' in line.upper(): # 兼容中英文
                listen_count += 1
                if listen_count <= 5: 
                    # 摘取包含 IP 和端口的部分
                    parts = line.split()
                    if len(parts) >= 2:
                        print(f"  -> {parts[1]}")
                        
        print(f"... (总计正在监听中的端口数量: {listen_count})")
        
    except Exception as e:
        print(f"执行 netstat 时发生异常: {e}")
    print("=" * 40)


if __name__ == "__main__":
    check_ping("1.1.1.1")
    check_active_ports()
    print("\n💡 提示: 第四课我们将学习如何用正则表达式强大的功能去提取复杂日志中的报错信息！")
