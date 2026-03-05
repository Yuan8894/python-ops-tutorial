"""
第五课：服务存活探测与 Webhook 告警
运维系统需要时刻知道各种对外服务是否存活。
我们在这里使用 Python 内置库 urllib 去请求网页，如果发现宕机，就模拟发送一条告警消息。
(在真实场景下，你通常会使用强大的 requests 库，并通过钉钉/飞书的 webhook URL 发送真正的 HTTP POST 告警)
"""
import urllib.request
import urllib.error
import json
import time

def send_mock_webhook_alert(service_name, error_msg):
    """模拟向办公软件机器人发送 Webhook 告警"""
    print("\n   [🚨 触发告警] -------------------")
    print(f"   | 目标服务: {service_name}")
    print(f"   | 错误详情: {error_msg}")
    print("   | 动作: 正在组装 JSON 消息体...")
    
    # 真实场景中，你会用 urllib.request.urlopen(req) 将这段数据 POST 到 webhook 地址
    payload = {
        "msgtype": "text",
        "text": {
            "content": f"【故障告警】\n服务: {service_name}\n详情: {error_msg}\n时间: {time.ctime()}"
        }
    }
    print(f"   | Payload: {json.dumps(payload, ensure_ascii=False)}")
    print("   --------------------------------\n")

def check_service_health(name, url):
    print(f"➤ 正在探测服务 [{name}] : {url}")
    try:
        # GET 请求目标 URL，设置超时为 3 秒
        response = urllib.request.urlopen(url, timeout=3)
        status_code = response.getcode()
        
        if status_code == 200:
            print(f"   ✅ [OK] 状态码: {status_code}，服务运行正常。")
        else:
            print(f"   ⚠️ [WARNING] 状态码异常: {status_code}")
            send_mock_webhook_alert(name, f"HTTP状态码非200 ({status_code})")
            
    except urllib.error.URLError as e:
        print(f"   ❌ [DOWN] 无法建立连接或请求报错。")
        send_mock_webhook_alert(name, f"连接失败: {e.reason}")
    except Exception as e:
        print(f"   ❌ [ERROR] 发生未知异常: {e}")
        send_mock_webhook_alert(name, str(e))

if __name__ == "__main__":
    print("=" * 40)
    print("📡 简易服务健康监控中心")
    print("=" * 40)
    
    # 测试一个正常的网址
    check_service_health("阿里本地 DNS", "http://223.5.5.5")
    
    # 测试一个肯定不存在或无法访问的错误网址
    check_service_health("内部支付前端网站", "http://192.168.99.99:8080")
    
    print("=" * 40)
    print("\n💡 提示: 最后一课(第六课)，我们将用 argparse 库把前面的知识封装成可以在终端灵活调用的 CLI 工具！")
