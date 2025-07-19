import os


ENVIRONMENT_INSTALLER = "ovo.sh"
ETAP_1 = "# todo!\n"
ETAP_2 = "## install-environment\n"
ETAP_3 = "## run-hello-world\n"


def add_ovos():
    for root, dirs, files in os.walk("hello_worlds"):
        for dir_name in dirs:
            ovo = os.path.join(root, dir_name)
            path = str(ovo)
            if len(path.split("/")) == 2:
                if not (ENVIRONMENT_INSTALLER in list(os.listdir(ovo))):
                    print("\t\t", "ovo-needed..")
                    with open(os.path.join(ovo, ENVIRONMENT_INSTALLER), "w") as wf:
                        wf.write(ETAP_1)
                        wf.write(ETAP_2)
                        wf.write(ETAP_3)
                else:
                    with open(os.path.join(ovo, ENVIRONMENT_INSTALLER), "r") as rf:
                        [print(o, end="") for o in rf.readlines()]


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
                    if not any("todo" in a for a in acc_str):
                        [print(o, end="") for o in acc_str]


lir_ovos()

# TODO:
# ovo.sh -> yaml
#
