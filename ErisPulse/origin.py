import asyncio
import aiohttp
from .envManager import env

class OriginManager:
    def __init__(self):
        self._init_origins()

    def _init_origins(self):
        if not env.get('origins'):
            env.set('origins', [])

    async def _validate_url(self, url):
        if not url.startswith(('http://', 'https://')):
            protocol = input("未指定协议，请输入使用的协议 (http 或 https): ").strip().lower()
            if protocol not in ['http', 'https']:
                print("无效的协议类型，必须是 http 或 https。")
                return None
            url = f"{protocol}://{url}"
        
        if not url.endswith('.json'):
            url = f"{url}/map.json"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    if response.headers.get('Content-Type', '').startswith('application/json'):
                        return url
                    else:
                        print(f"源 {url} 返回的内容不是有效的 JSON 格式。")
                        return None
        except Exception as e:
            print(f"访问源 {url} 失败: {e}")
            return None


    def add_origin(self, value):
        validated_url = asyncio.run(self._validate_url(value))
        if not validated_url:
            print("提供的源不是一个有效源，请检查后重试。")
            return

        origins = env.get('origins')
        if validated_url not in origins:
            origins.append(validated_url)
            env.set('origins', origins)
            print(f"源 {validated_url} 已成功添加。")
        else:
            print(f"源 {validated_url} 已存在，无需重复添加。")

    def update_origins(self):
        origins = env.get('origins')
        providers = {}
        modules = {}
        module_alias = {}
        
        print("\033[1m{:<10} | {:<20} | {:<50}\033[0m".format("源", "模块", "地址"))
        print("-" * 85)

        async def fetch_origin_data():
            async with aiohttp.ClientSession() as session:
                for origin in origins:
                    print(f"\n\033[94m正在获取 {origin}\033[0m")
                    try:
                        async with session.get(origin) as response:
                            response.raise_for_status()
                            if response.headers.get('Content-Type', '').startswith('application/json'):
                                content = await response.json()
                                providers[content["name"]] = content["base"]
                                
                                for module in list(content["modules"].keys()):
                                    module_content = content["modules"][module]
                                    modules[f'{module}@{content["name"]}'] = module_content
                                    module_origin_name = module_content["path"]
                                    module_alias_name = module
                                    module_alias[f'{module_origin_name}@{content["name"]}'] = module_alias_name

                                    print("{:<10} | {:<20} | {:<50}".format(
                                        content['name'], 
                                        module, 
                                        f"{providers[content['name']]}{module_origin_name}"
                                    ))
                            else:
                                print(f"\033[91m源 {origin} 返回的内容不是有效的 JSON 格式。\033[0m")
                    except Exception as e:
                        print(f"\033[91m获取 {origin} 时出错: {e}\033[0m")

        # 使用 asyncio.run 调用异步任务
        asyncio.run(fetch_origin_data())

        env.set('providers', providers)
        env.set('modules', modules)
        env.set('module_alias', module_alias)
        
        print("\n\033[92m{}\033[0m".format("完成".center(85, "-")))

    def list_origins(self):
        origins = env.get('origins')
        for origin in origins:
            print(origin)

    def del_origin(self, value):
        origins = env.get('origins')
        if value in origins:
            origins.remove(value)
            env.set('origins', origins)
            print(f"源 {value} 已删除。")
        else:
            print(f"源 {value} 不存在。")

origin_manager = OriginManager()