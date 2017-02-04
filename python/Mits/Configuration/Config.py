import osimport sysimport platform as plat
#this is the path in which all the dumps will be saved to.if "Darwin" in plat.system():    DUMP_PATH = os.path.expanduser("~/Work/dumps/")else:    DUMP_PATH = "C:\\dumps\\"
# RETEAM_ROOT_PATH if "Darwin" in plat.system():    RETEAM_ROOT_PATH = os.path.expanduser("~/Work/RETeam/")else:    RETEAM_ROOT_PATH = "C:\\RETeam"
# BOOTLOADER_ROOT_PATH BOOTLOADER_ROOT_PATH = os.path.join(RETEAM_ROOT_PATH, "Deliverables")
# MITS PATHif "Darwin" in plat.system():    MITS_PATH = os.path.expanduser("~/Work/Mits")else:    MITS_PATH = "C:\\Python%s%s\\Lib\\site-packages\\Mits" % (sys.version_info[0], sys.version_info[1])

#set this to True to make logs. logs saved to DUMP_PATHLOGS_ENABLED = True
IS_UFED = False
