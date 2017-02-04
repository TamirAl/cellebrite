from Mits.Families.Qualcomm.DLoadMode import *from Mits.Clients.ClientQcDownloadInternal import ClientQcDownloadInternalfrom Mits.Utils.ConfigReader import ConfigReaderfrom Mits.Utils.upy import upy
# Set this to true if phone is in diag mode upon connection, and we have to# switch from diag to dload_mode#PHONE_CONNECTED_IN_DIAG_MODE = True# When switching from diag to dload, should I reconnect automatically? If set to# False, user is prompted.#AUTO_WAIT = False
##### Achtung!# When switching from diag mode to dload mode and the serial port number is not# the same after the switch, family.connect() function will fail. Hence# reconnect will not work.# You can just run the test again after setting PHONE_CONNECTED_IN_DIAG_MODE = False###
configuration_file_name = r"__script_lg_qc_internal.xml" configuration_params = ['PHONE_CONNECTED_IN_DIAG_MODE', 'AUTO_WAIT']
config = upy.get_config(configuration_file_name, configuration_params)

upy.ui_async_operation("Connecting", "Please wait")# Choose family:f = FamilyQcDownload_ReadEmmc(_timeout = 0.5)##f = FamilyQcDownload_ReadNand()
c = ClientQcDownloadInternal(f)
if config.PHONE_CONNECTED_IN_DIAG_MODE:    c.enter_dload_mode(config.AUTO_WAIT)
c.dump()