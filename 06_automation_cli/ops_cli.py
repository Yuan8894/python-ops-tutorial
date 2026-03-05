"""
第六课：用 Python 打造专业的运维 CLI 工具
将散落的脚本整合成一个命令行工具（CLI: Command-Line Interface），
这是高级运维必备的技能！我们将使用内置的 `argparse` 模块。
"""
import argparse
import sys
import os
from pathlib import Path

# 获取项目根目录，以便导入其他独立课程模块
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

import importlib

# 动态加载带有数字开头文件名的模块
system_insight = importlib.import_module("01_system_basics.system_insight")
memory_monitor = importlib.import_module("01_system_basics.memory_disk_monitor")
log_manager = importlib.import_module("02_file_operations.log_manager")
net_diag = importlib.import_module("03_shell_execution.net_diagnostics")

def task_sysinfo():
    print("▶ 执行任务: 获取系统真实基础信息")
    # 调用第一课的方法
    system_insight.get_basic_system_info()
    memory_monitor.get_disk_usage()
    memory_monitor.get_memory_auto()
    print("✅ 系统信息获取完毕。")

def task_cleanlogs(path):
    print(f"▶ 执行任务: 清理 {path} 下的过期日志")
    target_dir = Path(path)
    if not target_dir.exists():
        print(f"目录不存在，自动生成测试目录: {target_dir}")
        target_dir = log_manager.setup_dummy_logs(target_dir.parent)
    
    # 调用第二课的方法
    log_manager.backup_and_cleanup_logs(target_dir)

def task_ping(host):
    print(f"▶ 执行任务: 测试 {host} 的网络连通性")
    # 调用第三课的方法
    net_diag.check_ping(host)


def main():
    # 1. 初始化解析器
    parser = argparse.ArgumentParser(
        prog="ops_tool",
        description="🚀 专属 Server 运维瑞士军刀 (Python CLI 演示)",
        epilog="例子: python ops_cli.py sysinfo"
    )
    
    # 2. 添加子命令解析器
    subparsers = parser.add_subparsers(dest="command", help="支持的运维指令")
    
    # 子命令: sysinfo
    subparsers.add_parser("sysinfo", help="获取服务器 CPU, 内存, 磁盘等状态")
    
    # 子命令: clean
    clean_parser = subparsers.add_parser("clean", help="清空指定目录下的过期日志")
    clean_parser.add_argument("-p", "--path", default="/var/log", help="指定要清理的目录路径 (默认: /var/log)")
    
    # 子命令: ping
    ping_parser = subparsers.add_parser("ping", help="测试目标 IP/域名的网络连通性")
    ping_parser.add_argument("target", help="必填：需要 PING 的目标地址, 例如 8.8.8.8")
    
    # 3. 解析用户在终端输入的参数
    args = parser.parse_args()
    
    # 4. 根据不同命令派发任务
    if args.command == "sysinfo":
        task_sysinfo()
    elif args.command == "clean":
        task_cleanlogs(args.path)
    elif args.command == "ping":
        task_ping(args.target)
    else:
        # 如果用户什么都没输入，就打印帮助文档
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
