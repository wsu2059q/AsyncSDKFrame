import argparse
import os
import sys
import shutil
import aiohttp
import zipfile
import asyncio
from .envManager import env
from .origin import origin_manager

def enable_module(module_name):
    module_info = env.get_module(module_name)
    if module_info:
        env.set_module_status(module_name, True)
        print(f"模块 {module_name} 已启用")
    else:
        print(f"模块 {module_name} 不存在")

def disable_module(module_name):
    module_info = env.get_module(module_name)
    if module_info:
        env.set_module_status(module_name, False)
        print(f"模块 {module_name} 已禁用")
    else:
        print(f"模块 {module_name} 不存在")
async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.read()
    except Exception as e:
        print(f"请求失败: {e}")
        return None
def extract_and_setup_module(module_name, module_url, zip_path, module_dir):
    try:
        print(f"正在从 {module_url} 下载模块...")
        
        async def download_module():
            async with aiohttp.ClientSession() as session:
                content = await fetch_url(session, module_url)
                if content is None:
                    return False
                
                with open(zip_path, 'wb') as zip_file:
                    zip_file.write(content)

                if not os.path.exists(module_dir):
                    os.makedirs(module_dir)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(module_dir)
                
                init_file_path = os.path.join(module_dir, '__init__.py')
                if not os.path.exists(init_file_path):
                    sub_module_dir = os.path.join(module_dir, module_name)
                    m_sub_module_dir = os.path.join(module_dir, f"m_{module_name}")
                    for sub_dir in [sub_module_dir, m_sub_module_dir]:
                        if os.path.exists(sub_dir) and os.path.isdir(sub_dir):
                            for item in os.listdir(sub_dir):
                                source_item = os.path.join(sub_dir, item)
                                target_item = os.path.join(module_dir, item)
                                if os.path.exists(target_item):
                                    os.remove(target_item)
                                shutil.move(source_item, module_dir)
                            os.rmdir(sub_dir)

                print(f"模块 {module_name} 文件已成功解压并设置")
                return True
        
        return asyncio.run(download_module())

    except Exception as e:
        print(f"处理模块 {module_name} 文件失败: {e}")
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except Exception as cleanup_error:
                print(f"清理失败: {cleanup_error}")
        return False

    finally:
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except Exception as cleanup_error:
                print(f"清理失败: {cleanup_error}")

def install_module(module_name, force=False):
    module_info = env.get_module(module_name)
    if module_info and not force:
        print(f"模块 {module_name} 已存在，使用 --force 参数强制重装")
        return

    providers = env.get('providers', {})
    if isinstance(providers, str):
        providers = json.loads(providers)
    module_info = []

    for provider, url in providers.items():
        module_key = f"{module_name}@{provider}"
        modules_data = env.get('modules', {})
        if isinstance(modules_data, str):
            modules_data = json.loads(modules_data)

        if module_key in modules_data:
            module_data = modules_data[module_key]
            module_info.append({
                'provider': provider,
                'url': url,
                'path': module_data.get('path', ''),
                'version': module_data.get('version', '未知'),
                'description': module_data.get('description', '无描述'),
                'author': module_data.get('author', '未知'),
                'dependencies': module_data.get('dependencies', []),
                'optional_dependencies': module_data.get('optional_dependencies', [])
            })

    if not module_info:
        print(f"未找到模块 {module_name}")
        return

    if len(module_info) > 1:
        print(f"找到 {len(module_info)} 个源的 {module_name} 模块：")
        for i, info in enumerate(module_info):
            print(f"{i+1}. 源: {info['provider']}")
            print(f"   版本: {info['version']}")
            print(f"   描述: {info['description']}")
            print(f"   作者: {info['author']}")
            print(f"   依赖: {', '.join(info['dependencies']) if info['dependencies'] else '无'}")
            print()

        while True:
            try:
                choice = int(input("请选择要安装的源 (输入编号): "))
                if 1 <= choice <= len(module_info):
                    selected_module = module_info[choice-1]
                    break
                else:
                    print("输入无效，请重新选择")
            except ValueError:
                print("请输入有效的数字")
    else:
        selected_module = module_info[0]

    for dep in selected_module['dependencies']:
        print(f"正在安装依赖模块 {dep}...")
        install_module(dep)

    if selected_module['optional_dependencies']:
        optional_deps_message = []
        for dep in selected_module['optional_dependencies']:
            if isinstance(dep, list):
                optional_deps_message.append(f"组合: {' + '.join(dep)}")
            else:
                optional_deps_message.append(f"模块: {dep}")
        print("\033[93m\033[1m" + f"模块 {module_name} 有可选依赖：{', '.join(optional_deps_message)}，请稍后手动选择安装！" + "\033[0m")
    module_url = selected_module['url'] + selected_module['path']
    script_dir = os.path.dirname(os.path.abspath(__file__))
    module_dir = os.path.join(script_dir, 'modules', module_name)
    zip_path = os.path.join(script_dir, f"{module_name}.zip")

    if not extract_and_setup_module(
        module_name=module_name,
        module_url=module_url,
        zip_path=zip_path,
        module_dir=module_dir
    ):
        return
    env.set_module(module_name, {
        'status': True,
        'info': {
            'version': selected_module['version'],
            'description': selected_module['description'],
            'author': selected_module['author'],
            'dependencies': selected_module['dependencies'],
            'optional_dependencies': selected_module['optional_dependencies']
        }
    })
    print(f"模块 {module_name} 安装成功")

def uninstall_module(module_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    module_path = os.path.join(script_dir, 'modules', module_name)

    module_file_path = module_path + '.py'
    if os.path.exists(module_file_path):
        try:
            os.remove(module_file_path)
        except Exception as e:
            print(f"删除模块文件 {module_name} 时出错: {e}")
    elif os.path.exists(module_path) and os.path.isdir(module_path):
        try:
            shutil.rmtree(module_path)
        except Exception as e:
            print(f"删除模块目录 {module_name} 时出错: {e}")
    else:
        print(f"模块 {module_name} 不存在")
        return

    if env.remove_module(module_name):
        print(f"模块 {module_name} 已删除")
    else:
        print(f"模块 {module_name} 不存在")

def upgrade_all_modules(force=False):
    all_modules = env.get_all_modules()
    if not all_modules:
        print("未找到任何模块，无法更新")
        return

    providers = env.get('providers', {})
    if isinstance(providers, str):
        providers = json.loads(providers)

    modules_data = env.get('modules', {})
    if isinstance(modules_data, str):
        modules_data = json.loads(modules_data)

    updates_available = []
    for module_name, module_info in all_modules.items():
        local_version = module_info['info'].get('version', '0.0.0')
        for provider, url in providers.items():
            module_key = f"{module_name}@{provider}"
            if module_key in modules_data:
                remote_module = modules_data[module_key]
                remote_version = remote_module.get('version', '0.0.0')
                if remote_version > local_version:
                    updates_available.append({
                        'name': module_name,
                        'local_version': local_version,
                        'remote_version': remote_version,
                        'provider': provider,
                        'url': url,
                        'path': remote_module.get('path', ''),
                    })

    if not updates_available:
        print("所有模块已是最新版本，无需更新")
        return

    print("\n以下模块有可用更新：")
    for update in updates_available:
        print(f"模块: {update['name']}")
        print(f"当前版本: {update['local_version']}")
        print(f"最新版本: {update['remote_version']}")
        print(f"源: {update['provider']}")
        print()

    if not force:
        confirm = input("\033[93m\033[1m警告：更新模块可能会导致兼容性问题，请在更新前查看插件作者的相关声明。\n"
                        "是否继续？(y/n): \033[0m").strip().lower()
        if confirm != 'y':
            print("更新已取消")
            return

    for update in updates_available:
        print(f"正在更新模块 {update['name']}...")
        module_url = update['url'] + update['path']
        script_dir = os.path.dirname(os.path.abspath(__file__))
        module_dir = os.path.join(script_dir, 'modules', update['name'])
        zip_path = os.path.join(script_dir, f"{update['name']}.zip")

        if not extract_and_setup_module(
            module_name=update['name'],
            module_url=module_url,
            zip_path=zip_path,
            module_dir=module_dir
        ):
            continue

        all_modules[update['name']]['info']['version'] = update['remote_version']
        env.set_all_modules(all_modules)
        print(f"模块 {update['name']} 已更新至版本 {update['remote_version']}")

def list_modules(module_name=None, page_size=5):
    all_modules = env.get_all_modules()
    if not all_modules:
        print("正在初始化模块列表...")
        from . import init as init_module
        init_module()
        all_modules = env.get_all_modules()
    
    modules = [{"name": name, **info} for name, info in all_modules.items()]

    if module_name:
        module = next((m for m in modules if m['name'] == module_name), None)
        if module:
            status = "启用" if module.get("status", True) else "禁用"
            print(f"模块: {module['name']}")
            print(f"状态: {status}")
            print(f"版本: {module['info'].get('version', '未知')}")
            print(f"描述: {module['info'].get('description', '无描述')}")
            print(f"作者: {module['info'].get('author', '未知')}")
            print(f"依赖: {', '.join(module['info'].get('dependencies', [])) if module['info'].get('dependencies') else '无'}")
        else:
            print(f"模块 {module_name} 不存在")
    else:
        total_modules = len(modules)
        total_pages = (total_modules + page_size - 1) // page_size
        current_page = 1

        try:
            while True:
                print("\033c", end="")

                start_index = (current_page - 1) * page_size
                end_index = min(start_index + page_size, total_modules)
                print(f"\n--- 模块列表 (第 {current_page}/{total_pages} 页) ---")

                for i in range(start_index, end_index):
                    module = modules[i]
                    status = "启用" if module.get("status", True) else "禁用"
                    dependencies = ', '.join(module['info'].get('dependencies', [])) if module['info'].get('dependencies') else '无'
                    print(f"{i+1}. 模块: {module['name']} | 状态: {status} | 版本: {module['info'].get('version', '未知')}")
                    print(f"    描述: {module['info'].get('description', '无描述')}")
                    print(f"    依赖: {dependencies}\n")

                print("\n输入页码直接跳转，或输入 'e' 下一页, 'q' 上一页 | 使用 Ctrl+C 退出")
                user_input = input("> ").strip().lower()
                if user_input.isdigit():
                    target_page = int(user_input)
                    if target_page < 1:
                        current_page = 1
                    elif target_page > total_pages:
                        current_page = total_pages
                    else:
                        current_page = target_page
                elif user_input == 'e' and current_page < total_pages:
                    current_page += 1
                elif user_input == 'q' and current_page > 1:
                    current_page -= 1
        except KeyboardInterrupt:
            print("\n")
            sys.exit(0)
def main():
    parser = argparse.ArgumentParser(
        description="ErisPulse 命令行工具",
        prog="python -m ErisPulse"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    enable_parser = subparsers.add_parser('enable', help='启用指定模块')
    enable_parser.add_argument('module_name', type=str, help='要启用的模块名称')
    enable_parser.add_argument('--init', action='store_true', help='在启用模块前初始化模块数据库')

    disable_parser = subparsers.add_parser('disable', help='禁用指定模块')
    disable_parser.add_argument('module_name', type=str, help='要禁用的模块名称')
    disable_parser.add_argument('--init', action='store_true', help='在禁用模块前初始化模块数据库')

    list_parser = subparsers.add_parser('list', help='列出所有模块信息')
    list_parser.add_argument('--init', action='store_true', help='在列出模块前初始化模块数据库')
    list_parser.add_argument('--module', '-m', type=str, help='指定要展示的模块名称')

    update_parser = subparsers.add_parser('update', help='更新模块列表')

    upgrade_parser = subparsers.add_parser('upgrade', help='升级模块列表')
    upgrade_parser.add_argument('--force', action='store_true', help='跳过二次确认，强制更新')

    uninstall_parser = subparsers.add_parser('uninstall', help='删除指定模块')
    uninstall_parser.add_argument('module_name', type=str, help='要删除的模块名称')

    install_parser = subparsers.add_parser('install', help='安装指定模块（支持多个模块，用逗号分隔）')
    install_parser.add_argument('module_name', type=str, help='要安装的模块名称')
    install_parser.add_argument('--force', action='store_true', help='强制重新安装模块')
    install_parser.add_argument('--init', action='store_true', help='在安装模块前初始化模块数据库')

    origin_parser = subparsers.add_parser('origin', help='管理模块源')
    origin_subparsers = origin_parser.add_subparsers(dest='origin_command', help='源管理命令')

    add_origin_parser = origin_subparsers.add_parser('add', help='添加模块源')
    add_origin_parser.add_argument('url', type=str, help='要添加的模块源URL')

    list_origin_parser = origin_subparsers.add_parser('list', help='列出所有模块源')

    del_origin_parser = origin_subparsers.add_parser('del', help='删除模块源')
    del_origin_parser.add_argument('url', type=str, help='要删除的模块源URL')

    args = parser.parse_args()

    if hasattr(args, 'init') and args.init:
        print("正在初始化模块列表...")
        from . import init as init_module
        init_module()

    # 全部指令：enable, disable, list, uninstall, install, update, origin(add, list, del)
    if args.command == 'enable':
        enable_module(args.module_name)
    elif args.command == 'disable':
        disable_module(args.module_name)
    elif args.command == 'list':
        list_modules(args.module)
    elif args.command == 'uninstall':
        uninstall_module(args.module_name)
    elif args.command == 'install':
        module_names = args.module_name.split(',')
        for module_name in module_names:
            module_name = module_name.strip()
            if module_name:
                install_module(module_name, args.force)
    elif args.command == 'update':
        origin_manager.update_origins()
    elif args.command == 'upgrade':
        upgrade_all_modules(args.force)
    elif args.command == 'origin':
        if args.origin_command == 'add':
            origin_manager.add_origin(args.url)
        elif args.origin_command == 'list':
            origin_manager.list_origins()
        elif args.origin_command == 'del':
            origin_manager.del_origin(args.url)
        else:
            origin_parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()