"""
第一课：系统探针与基础信息获取
目标：掌握 os, sys, platform 模块的基本用法，了解如何获取服务器的基础环境信息。
"""
import os
import sys
import platform

def get_basic_system_info():
    print("=" * 40)
    print("🖥️  服务器/本机 基础运维信息探针")
    print("=" * 40)
    
    # 1. 获取操作系统类型与版本
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    print(f"[OS] 操作系统: {os_name} {os_release} ({os_version})")
    
    # 2. 获取计算机网络名称
    hostname = platform.node()
    print(f"[Network] 主机名: {hostname}")
    
    # 3. 获取 Python 环境信息
    py_version = sys.version.split()[0]
    py_path = sys.executable
    print(f"[Python] 版本: {py_version}")
    print(f"[Python] 解释器路径: {py_path}")
    
    # 4. 获取当前工作目录路径
    cwd = os.getcwd()
    print(f"[FS] 当前工作目录: {cwd}")
    
    # 5. 获取 CPU 逻辑核心数
    cpu_count = os.cpu_count()
    print(f"[Hardware] CPU 逻辑核心数: {cpu_count}")
    print("=" * 40)

if __name__ == "__main__":
    get_basic_system_info()
    print("\n💡 提示: 接下来我们可以引入 psutil 库来获取更详细的内存和磁盘利用率！")
