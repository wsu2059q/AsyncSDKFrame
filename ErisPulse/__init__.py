import os
import sys
from . import sdk
from . import util
from . import errors
from . import logger
from .envManager import env

setattr(sdk, "env", env)
# setattr(sdk, "logger", logger)
setattr(sdk, "util", util)

env.load_env_file()

def init():
    try:
        sdkModulePath = os.path.join(os.path.dirname(__file__), "modules")
        
        if not os.path.exists(sdkModulePath):
            os.makedirs(sdkModulePath)

        sys.path.append(sdkModulePath)

        TempModules = [
            x for x in os.listdir(sdkModulePath)
            if os.path.isdir(os.path.join(sdkModulePath, x))
        ]

        sdkInstalledModuleNames: list[str] = []
        disabledModules: list[str] = []

        for module_name in TempModules:
            try:
                moduleObj = __import__(module_name)
                if not hasattr(moduleObj, "moduleInfo") or not isinstance(moduleObj.moduleInfo, dict):
                    logger.warning(f"模块 {module_name} 缺少有效的 'moduleInfo' 字典.")
                    continue
                if "name" not in moduleObj.moduleInfo:
                    logger.warning(f"模块 {module_name} 的 'moduleInfo' 字典 缺少必要 'name' 键.")
                    continue
                if not hasattr(moduleObj, "Main"):
                    logger.warning(f"模块 {module_name} 缺少 'Main' 类.")
                    continue
                
                module_info = env.get_module(moduleObj.moduleInfo["name"])
                if module_info is None:
                    module_info = {
                        "status": True,
                        "info": moduleObj.moduleInfo
                    }
                    env.set_module(moduleObj.moduleInfo["name"], module_info)
                    logger.info(f"模块 {moduleObj.moduleInfo['name']} 信息已初始化并存储到数据库")
                
                if not module_info.get('status', True):
                    disabledModules.append(module_name)
                    logger.warning(f"模块 {moduleObj.moduleInfo['name']} 已禁用，跳过加载")
                    continue
                    
                required_deps = moduleObj.moduleInfo.get("dependencies", [])
                missing_required_deps = [dep for dep in required_deps if dep not in TempModules]
                if missing_required_deps:
                    logger.error(f"模块 {module_name} 缺少必需依赖: {missing_required_deps}")
                    raise errors.MissingDependencyError(f"模块 {module_name} 缺少必需依赖: {missing_required_deps}")

                optional_deps = moduleObj.moduleInfo.get("optional_dependencies", [])
                available_optional_deps = []

                for dep in optional_deps:
                    if isinstance(dep, list):
                        if all(d in TempModules for d in dep):
                            available_optional_deps.extend(dep)
                    elif dep in TempModules:
                        available_optional_deps.append(dep)

                if optional_deps and not available_optional_deps:
                    logger.warning(f"模块 {module_name} 缺少所有可选依赖: {optional_deps}")
                    continue

                sdkInstalledModuleNames.append(module_name)
            except Exception as e:
                logger.warning(f"模块 {module_name} 加载失败: {e}")
                continue

        sdkModuleDependencies = {}
        for module_name in sdkInstalledModuleNames:
            moduleObj = __import__(module_name)
            moduleDependecies: list[str] = moduleObj.moduleInfo.get("dependencies", [])

            optional_deps = moduleObj.moduleInfo.get("optional_dependencies", [])
            available_optional_deps = [dep for dep in optional_deps if dep in sdkInstalledModuleNames]
            moduleDependecies.extend(available_optional_deps)

            for dep in moduleDependecies:
                if dep in disabledModules:
                    logger.warning(f"模块 {module_name} 的依赖模块 {dep} 已禁用，跳过加载")
                    continue
            
            if not all(dep in sdkInstalledModuleNames for dep in moduleDependecies):
                raise errors.InvalidDependencyError(
                    f"模块 {module_name} 的依赖无效: {moduleDependecies}"
                )
            sdkModuleDependencies[module_name] = moduleDependecies

        sdkInstalledModuleNames: list[str] = sdk.util.topological_sort(
            sdkInstalledModuleNames, sdkModuleDependencies, errors.CycleDependencyError
        )

        all_modules_info = {}
        for module_name in sdkInstalledModuleNames:
            moduleObj = __import__(module_name)
            moduleInfo: dict = moduleObj.moduleInfo

            module_info = env.get_module(moduleInfo["name"])
            env.set_module(moduleInfo["name"], {
                "status": True,
                "info": moduleInfo
            })
        logger.debug("所有模块信息已加载并存储到数据库")

        for module_name in sdkInstalledModuleNames:
            moduleObj = __import__(module_name)
            moduleInfo = moduleObj.moduleInfo
            module_status = env.get_module_status(moduleInfo["name"])
            if not module_status:
                continue
            
            moduleMain = moduleObj.Main(sdk, logger)
            setattr(moduleMain, "moduleInfo", moduleInfo)
            setattr(sdk, moduleInfo["name"], moduleMain)
            logger.debug(f"模块 {moduleInfo['name']} 正在初始化")
    except Exception as e:
        logger.error(f"初始化失败: {e}")
        raise e

sdk.init = init
