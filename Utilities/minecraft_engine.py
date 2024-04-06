import os, json, time, subprocess, minecraft_launcher_lib
from Utilities.general import *
import minecraft_launcher_lib

current_max = 0

def set_status(status: str):
    print(status)


def set_progress(progress: int):
    if current_max != 0:
        print(f"{progress}/{current_max}")


def set_max(new_max: int):
    global current_max
    current_max = new_max

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}

def readjson(file) -> dict:
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {} 
    
def writejson(file, datos) -> None:
    with open(file, "w") as f:
        json.dump(datos, f, indent=4)

def install_minecraft(version: str, directory: str, callback: dict, versionsPath: str, start=False, mode='Vanilla') -> None:
    if mode == "Vanilla":
        minecraft_launcher_lib.install.install_minecraft_version(
            version, directory, callback=callback)
    elif mode == "Forge":
        forge = minecraft_launcher_lib.forge.find_forge_version(version)
        minecraft_launcher_lib.forge.install_forge_version(
            forge, directory, callback=callback)
    elif mode == "Fabric":
        fabric_supor_ver = minecraft_launcher_lib.fabric.is_minecraft_version_supported(version)
        if not fabric_supor_ver:
            ErrorMsg(
                'Version error',
                f'The Minecraft version "{version}" does not support Fabric.'
            )
        else:
            fabric = minecraft_launcher_lib.fabric.install_fabric(version, directory, callback=callback)
    else:
        ErrorMsg(
            'Game mode error',
            'The game mode only can be Vanilla, Forge or Fabric'
        )
    
    # Obtener la ID de la versión instalada
    installed_version_id = ""
    if mode == "Vanilla":
        installed_version_id = version
    elif mode == "Forge":
        installed_version_id = forge['id']
    elif mode == "Fabric":
        installed_version_id = fabric['id']

    # Actualizar el archivo JSON con la nueva versión instalada
    data = readjson(versionsPath)
    data["id"] = installed_version_id
    writejson(versionsPath, data)

    # Mensaje de confirmación
    if start:
        AdvMsg(
            f'{mode} version {version} installed',
            'The game will now start in a few seconds...'
        )
    else:
        AdvMsg(
            f'Version {version} installed',
            f'{mode} version {version} installed correctly.'
        )

        
def start_mine(file, username, directory, version):
    data = readjson(file)   
    if 'RAM' in data and 'JAVA' in data:
        ram = data['RAM']
        javaPath = data['JAVA']
    else:
        ErrorMsg(
            'ConfigError',
            'Java or Ram missing in config.'
        )
        return False

    options = {
        'username': username,
        'uuid': '',
        'token': '',
        'executablePath':f'{javaPath}',
        'defaultExecutablePath':f'{javaPath}',

        "jvmArguments": [
            f"-Xmx{ram}G",
            f"-Xms{ram}G",
            ], 
        "launcherVersion": "1.0.3",
    }
    command = minecraft_launcher_lib.command.get_minecraft_command(
        version, directory, options)
    subprocess.run(command)


def run(minePath, configPath, versionsPath, username, version, mode):
    dataVersions = readjson(versionsPath)
    if f"{mode}-{version}" in dataVersions.keys():
        if  version in dataVersions["id"]:
            print()
            start_mine(
                file=configPath,
                username=username,
                version=version,
                directory=minePath
                )
        else:
            install_minecraft(version=version, mode=mode, directory=minePath, versionsPath=versionsPath, callback=callback)