"""
    ConnectionUSB
"""


# usb probing for UFED conection
class USBProbing(object):
    fbus_probing = 0
    at_probing = 1
    at_with_vendor_probing = 2
    generic_obex_probing = 3
    nok7160_obex_probing = 4
    nokS40_obex_probing = 5
    CDC_at_probing = 6
    Client_probing = 7
    vendor_no_probing = 8
    qcp_info_probing = 9
    vendor_interval_no_probing = 10
    vendor_BB_find_Endpoint = 11
    zte_info_probing = 12
    no_probing_use_previous_info = 13
    qcp_filesystem_probing = 14
    p2k_probing = 15
    unknown_no_probing = 16
    generic_obex_probing_no_disconnect = 17
    at_probing_control_interface = 18
    at_probing_ctl_with_interrupt = 19
    at_probing_thuraya_class = 20
    com_control_no_probing = 21
    com_data_no_probing = 22
    printer_no_probing = 23
    at_probing_thuraya_interrupt = 24
    mass_storage_no_probing = 25
    android_adb_probe = 26
    qcp_status_probing = 27
    obex_linux_probing = 28
    at_no_ctrl_lines_probing = 29
    at_zte_u210_probing = 30
    android_adb_probe_with_clear = 31
    at_willcom_with_vendor_probing = 32
    Nexperia_protocol_probing = 33
    qcp_info_com_control = 34
    qcp_download_mode_probing = 35
    at_LG_probing = 36     

