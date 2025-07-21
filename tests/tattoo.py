import os
import yaml
import platform
import subprocess


ENVIRONMENT_INSTALLER = "ovo.yaml"
ETAP_1 = "# todo!\n"
ETAP_2 = "## install-environment\n"
ETAP_3 = "## run-hello-world\n"
ETAPS = [ETAP_1,ETAP_2,ETAP_3]
PLATFORMS = ["centos","macos","windows","rhel"]

def add_ovos():
    for root, dirs, files in os.walk("hello_worlds"):
        for dir_name in dirs:
            ovo = os.path.join(root, dir_name)
            path = str(ovo)
            if len(path.split("/")) == 2:
                if not (ENVIRONMENT_INSTALLER in list(os.listdir(ovo))):
                    print("\t\t", "ovo-needed..")
                    with open(os.path.join(ovo, ENVIRONMENT_INSTALLER), "w") as wf:
                        for e in ETAPS:
                            wf.write(e)
                else:
                    with open(os.path.join(ovo, ENVIRONMENT_INSTALLER), "r") as rf:
                        [print(o, end="") for o in rf.readlines()]

def remover_ovos():
    for root, dirs, files in os.walk("hello_worlds"):
        for dir_name in dirs:
            ovo = os.path.join(root, dir_name)
            path = str(ovo)
            installer_path = os.path.join(ovo, ENVIRONMENT_INSTALLER)
            if len(path.split("/")) == 2 and ENVIRONMENT_INSTALLER in os.listdir(ovo):
                try:
                    os.remove(installer_path)
                    print(f"Removed {installer_path}")
                except Exception as e:
                    print(f"Error removing {installer_path}: {e}")


def lir_ovos():
    for root, dirs, files in os.walk("hello_worlds"):
        for dir_name in dirs:
            ovo = os.path.join(root, dir_name)
            path = str(ovo)
            if len(path.split("/")) == 2 and ENVIRONMENT_INSTALLER in list(
                os.listdir(ovo)
            ):
                with open(os.path.join(ovo, ENVIRONMENT_INSTALLER), "r") as rf:
                    acc_str = [o for o in rf.readlines()]
                    if not any(a in ETAPS for a in acc_str): 
                        # non-default
                        print('*',path)
                        [print('\t'+o, end="") for o in acc_str]
                        print()

def device_to_cmd_family(device, cfs=PLATFORMS):
    """Identify which os to use..."""
    device_tokes = device.split('-')
    for dt in device_tokes:
        for cf in cfs:
            if dt.lower().strip() in cf:
                return cf

def chocar_ovos(chocar=False):
    for root, dirs, files in os.walk("hello_worlds"):
        for dir_name in dirs:
            ovo = os.path.join(root, dir_name)
            path = str(ovo)
            if len(path.split("/")) == 2 and ENVIRONMENT_INSTALLER in list(
                os.listdir(ovo)
            ):
                with open(os.path.join(ovo, ENVIRONMENT_INSTALLER), "r") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict):
                        device = platform.platform()
                        for cmd in (data[ETAP_2.replace("#","").strip()][device_to_cmd_family(device)]):
                            print("Attempting...",cmd)
                            if chocar:
                                try:
                                    subprocess.run(cmd, shell=True, check=True)
                                except Exception as e:
                                    print(f"Error running command '{cmd}': {e}")
lir_ovos()
chocar_ovos(chocar=True)
