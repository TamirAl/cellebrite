
from Mits.Clients.ClientBcmUploadMode import ClientBcmUploadModepassword = ""c = ClientBcmUploadMode()try :    c.connect()    password = str(c.read_password(phone_already_booted = False))
    print "password: " + str(password)except :    err = 1finally :    c.close()