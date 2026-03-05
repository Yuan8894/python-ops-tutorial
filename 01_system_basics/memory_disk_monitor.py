"""
第一课 (补充)：免第三方库的系统监控方案
由于服务器环境各异，有时无法顺利安装第三方库（如 psutil）。
此时运维人员可以通过 Python 的 `subprocess` 模块，巧妙调用操作系统自带的命令来获取信息。
"""
import subprocess
import shutil

def get_disk_usage():
    print("=" * 40)
    print("💾 磁盘利用率 (使用 shutil 模块)")
    print("=" * 40)
    
    # 使用 Python 标准库获取磁盘空间信息 (单位：字节)
    total, used, free = shutil.disk_usage("/")
    
    # 转换为 GB
    gb_total = total / (2**30)
    gb_used = used / (2**30)
    gb_free = free / (2**30)
    percent = (used / total) * 100
    
    print(f"[Disk] 总容量:  {gb_total:.2f} GB")
    print(f"[Disk] 已使用:  {gb_used:.2f} GB ({percent:.1f}%)")
    print(f"[Disk] 可用剩余: {gb_free:.2f} GB")
    print("=" * 40)

def get_memory_linux():
    print("=" * 40)
    print("🧠 内存状态 (Linux 特供：读取 /proc/meminfo 文件)")
    print("=" * 40)
    
    try:
        mem_info = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    # 剥离 kB 单位并转为整数
                    val_str = parts[1].split()[0]
                    mem_info[key] = int(val_str)
                    
        total_kb = mem_info.get('MemTotal', 0)
        free_kb = mem_info.get('MemFree', 0)
        # Linux 可用内存不仅仅是 Free，还包含 Buffers 和 Cached (简单计算)
        available_kb = mem_info.get('MemAvailable', free_kb)
        
        total_mb = total_kb / 1024
        available_mb = available_kb / 1024
        used_mb = total_mb - available_mb
        percent = (used_mb / total_mb) * 100 if total_mb > 0 else 0
        
        print(f"[Memory] 总内存: {total_mb:.0f} MB")
        print(f"[Memory] 已使用: {used_mb:.0f} MB ({percent:.1f}%)")
        print(f"[Memory] 可用(估算): {available_mb:.0f} MB")
    
    except Exception as e:
        print(f"获取 Linux 内存失败: {e}")
    print("=" * 40)

def get_memory_windows():
    print("=" * 40)
    print("🧠 内存状态 (Windows 特供：调用 systeminfo 指令)")
    print("=" * 40)
    
    try:
        # 调用 Windows 内置命令获取内存信息
        result = subprocess.run(
            ['systeminfo'], capture_output=True, text=True, check=True
        )
        
        total_mb = 0
        free_mb = 0
        
        # 逐行解析 systeminfo 输出
        for line in result.stdout.split('\n'):
            if "Total Physical Memory" in line or "物理内存总量" in line:
                # 提取数字，去除逗号和 MB
                num_str = ''.join(filter(str.isdigit, line))
                total_mb = int(num_str) if num_str else 0
            elif "Available Physical Memory" in line or "可用的物理内存" in line:
                num_str = ''.join(filter(str.isdigit, line))
                free_mb = int(num_str) if num_str else 0
                
        if total_mb > 0:
            used_mb = total_mb - free_mb
            percent = (used_mb / total_mb) * 100
            
            print(f"[Memory] 总内存: {total_mb} MB")
            print(f"[Memory] 已使用: {used_mb} MB ({percent:.1f}%)")
            print(f"[Memory] 空闲中: {free_mb} MB")
        else:
            print("未能成功解析内存信息")
            
    except Exception as e:
        print(f"获取 Windows 内存失败: {e}")
    print("=" * 40)

def get_memory_auto():
    import platform
    os_name = platform.system().lower()
    if os_name == "windows":
        get_memory_windows()
    elif os_name == "linux":
        get_memory_linux()
    else:
        print(f"⚠️ 暂未适配操作系统: {os_name}")

if __name__ == "__main__":
    get_disk_usage()
    get_memory_auto()
    print("\n💡 提示: 第二课我们将学习如何利用 pathlib 批量管理服务器日志文件！")
