import requests
from typing import Any
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin import ToolProvider


class Crawl4AIProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            server_url = credentials.get("server_url")
            api_token = credentials.get("api_token")
            
            # 验证URL格式
            if not server_url or not server_url.startswith("http"):
                raise ToolProviderCredentialValidationError("服务器URL无效，必须以http或https开头")
            
            # 使用/crawl端点测试API连接
            test_url = f"{server_url.rstrip('/')}/crawl"
            
            # 准备请求数据
            payload = {
                "urls": ["https://example.com"],
                "priority": 10
            }
            
            # 设置请求头
            headers = {}
            if api_token:
                headers["Authorization"] = f"Bearer {api_token}"
            
            try:
                # 发送测试请求
                response = requests.post(
                    test_url,
                    headers=headers,
                    json=payload,
                    timeout=5
                )
                
                if response.status_code != 200:
                    raise ToolProviderCredentialValidationError(f"连接到Crawl4AI服务器失败，状态码：{response.status_code}")
                
                # 验证响应是否包含task_id
                result = response.json()
                if "task_id" not in result:
                    raise ToolProviderCredentialValidationError("无效的API响应格式，缺少task_id")
                
            except requests.exceptions.RequestException as e:
                raise ToolProviderCredentialValidationError(f"连接到Crawl4AI服务器失败：{str(e)}")
                
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
