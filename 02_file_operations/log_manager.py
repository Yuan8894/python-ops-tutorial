"""
第二课：文件与目录的批量化操作
运维日常离不开备份和清理。这个脚本将演示如何使用 `pathlib` 和 `shutil` 自动寻找并备份特定格式的日志。
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

def setup_dummy_logs(base_dir):
    """(这只是为了演示准备数据的函数) 在指定目录下创建一些假日志文件"""
    log_dir = base_dir / "app_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 建立几个测试日志
    (log_dir / "server_access.log").write_text("ok")
    (log_dir / "server_error.log").write_text("error")
    (log_dir / "database.log").write_text("db ok")
    (log_dir / "old_backup.txt").write_text("old stuff")
    
    print(f"✅ 生成了测试日志目录: {log_dir}")
    return log_dir

def backup_and_cleanup_logs(log_dir):
    print("=" * 40)
    print("📁 日志自动化备份与归档系统")
    print("=" * 40)
    
    # 1. 创建备份目标文件夹 (加盖时间戳)
    today_str = datetime.now().strftime("%Y%m%d")
    backup_dir = log_dir.parent / f"backup_{today_str}"
    backup_dir.mkdir(exist_ok=True)
    print(f"-> 准备备份目录: {backup_dir}")
    
    # 2. 查找并处理所有 .log 结尾的文件
    log_count = 0
    # rglob 可以递归查询子文件夹下的特定格式文件
    for log_file in log_dir.rglob("*.log"):
        # 复制文件到备份目录
        dest_file = backup_dir / log_file.name
        shutil.copy2(log_file, dest_file)
        
        # 假设我们需要清空原日志的内容以释放空间 (日志轮转的思想)
        # 用空字符覆盖
        log_file.write_text("")
        
        print(f"  [备份成功] {log_file.name} -> {dest_file.name} (原日志已截断清空)")
        log_count += 1
        
    print(f"\n🎉 归档完成！共处理了 {log_count} 个日志文件")
    print("=" * 40)

if __name__ == "__main__":
    # 我们将被执行的工作目录设为 base
    current_cwd = Path(os.getcwd())
    
    print("\n[环境准备阶段]")
    test_log_folder = setup_dummy_logs(current_cwd / "02_file_operations")
    
    print("\n[运维执行阶段]")
    backup_and_cleanup_logs(test_log_folder)
    
    print("\n💡 提示: 第三课我们将学习利用 subprocess 优雅地执行系统 Shell 指令 (如 ping/netstat)，并解析它们的输出！")
