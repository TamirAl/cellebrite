import osimport PythonExtfrom Mits.Utils.Iupy import Iupy
ABORT_EXCEPTION = "User aborted the operation"
class UfedUpy(Iupy):    instance = None    ir_mode = None    usb_probing_mode = None    usb_transfer_mode = None    side = None
    @classmethod    def initialize(cls):        cls.instance = PythonExt.upy()        cls.ir_mode = PythonExt.ir_mode()        cls.usb_probing_mode = PythonExt.usb_probing_mode()        cls.usb_transfer_mode = PythonExt.usb_transfer_mode()        cls.side = PythonExt.side()
    @classmethod    def com_init_link(cls, mode = None, usb_probing = None):        if mode is None :            mode = PythonExt.ir_mode.com        if usb_probing is None :            usb_probing = PythonExt.usb_probing_mode.at_probing        return cls.instance.com_init_link(mode, usb_probing)
    @classmethod    def com_shutdown_link(cls):        cls.instance.com_shutdown_link()
    @classmethod    def com_set_timeout(cls, value):        cls.instance.com_set_timeout(value)
    @classmethod    def com_reset_timeout(cls):        cls.instance.com_reset_timeout()
    @classmethod    def com_get_link_type(cls):        return cls.instance.com_get_link_type()
    @classmethod    def com_set_zero_transaction(cls, mode):        cls.instance.com_set_zero_transaction(mode)
    @classmethod    def com_usb_control_transfer(cls, type_, request, value, index, buf = ""):        return cls.instance.com_usb_control_transfer(type_, request, value, index, buf, len(buf))
    @classmethod    def io_send(cls, buf):        return cls.instance.io_send(buf, len(buf))
    @classmethod    def io_receive(cls, buf, size = -1):        if size < 0:            size = len(buf)
        return cls.instance.io_receive(cls, buf, size)
    @classmethod    def io_flush_rx(cls, buf):        cls.instance.io_flush_rx()
    @classmethod    def db_get_str(cls, key, default = ""):        return cls.instance.db_get_str(str(key), str(default))
    @classmethod    def db_get_int(cls, key, default = 0):        return cls.instance.db_get_int(str(key), default)
    @classmethod    def db_get_uint(cls, key, default = 0):        return cls.instance.db_get_uint(str(key), default)
    @classmethod    def target_set_file_size(cls, file_, size = 0):        return cls.instance.target_set_file_size(file_, size)
    @classmethod    def target_write_chunk(cls, buf, chunk_offset, file_ = ""):        return cls.instance.target_write_chunk(buf, chunk_offset, len(buf), file_)
    @classmethod    def target_finalize_write(cls, file_ = ""):        if (file_ == ""):            file_ = cls.instance.target_default_dump_file()        return cls.instance.target_finalize_write(file_)
    @classmethod    def target_add_desc_set(cls, s1, s2, s3):        return cls.instance.target_add_desc_set(s1,s2,s3)



    @classmethod    def ui_connecting(cls):        return cls.instance.ui_connecting()
    @classmethod    def ui_create_progress_bar(cls, file_, size, file_number = 0, progress = 0):        return cls.instance.ui_create_progress_bar(file_, size, file_number, progress)
    @classmethod    def ui_update_progress(cls, current):        return cls.instance.ui_update_progress(current)

    """    Returns True if the user presses continue, and raises exception if the user pressed abort. if the user pressed abort.    If you want to catch the exception and handle an abortion. please rethrow it so the UFED could handle the abort as well.    """    @classmethod    def ui_msg_continue(cls, msg, title="Continue"):        if not cls.instance.ui_msg_continue(title, msg):            raise Exception (ABORT_EXCEPTION)        return True
    @classmethod    def ui_error_msg(cls, error = "An error accord"):        return cls.instance.ui_error_msg(error)
    @classmethod    def ui_print_during_dump(cls, msg):        return cls.instance.ui_print_during_dump(msg)
    @classmethod    def ui_async_operation(cls, title, msg):        return cls.instance.ui_async_operation(title, msg)
    @classmethod    def ui_read_password_message(cls):        return cls.instance.ui_read_password_message()
    @classmethod    def ui_extract_or_remove_password(cls):        return cls.instance.ui_extract_or_remove_password()
    @classmethod    def ui_yes_no(cls):        return cls.instance.yes_no()
    @classmethod    def get_config(cls, file_name, expected_config_arguments) :        #Note the import Must be inside the method and not as a global import !        from Mits.Utils.ConfigReaderUFED import ConfigReaderUFED
        config_reader = ConfigReaderUFED()        #fn = os.path.join(cls.instance.get_config_path(), cls.instance.get_config_file_name())        return config_reader.get_config(None, expected_config_arguments)