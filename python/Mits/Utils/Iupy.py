import osfrom Mits.Utils.ConfigReader import ConfigReader
# define a stub class - doesn't do anythingclass Iupy(object):
    @classmethod    def initialize(cls):        return True
    @classmethod    def com_init_link(cls, mode = "", usb_probing = ""):        return True
    @classmethod    def com_shutdown_link(cls):        return True
    @classmethod    def com_set_timeout(cls, value):        return True
    @classmethod    def com_reset_timeout(cls):        return True
    @classmethod    def com_get_link_type(cls):        return True
    @classmethod    def com_set_zero_transaction(cls, mode):        return True
    @classmethod    def com_usb_control_transfer(type_, request, value, index, buf_ = ""):        return True
    @classmethod    def io_send(cls, buf):        return True
    @classmethod    def io_receive(cls, buf, size = -1):        return True    @classmethod    def io_flush_rx(cls, buf):        return True
    @classmethod    def db_get_str(cls, key, default = ""):        return True
    @classmethod    def db_get_int(cls, key, default = 0):        return True
    @classmethod    def db_get_uint(cls, key, default = 0):        return True
    @classmethod    def target_set_file_size(cls, file_, size = 0):        return True
    @classmethod    def target_write_chunk(cls, buf, chunk_offset, file_ = ""):        return True
    @classmethod    def target_finalize_write(cls, file_ = ""):        return True

    @classmethod    def target_add_desc_set(cls, s1, s2, s3):        return True
    @classmethod    def ui_connecting(cls):        return True
    @classmethod    def ui_create_progress_bar(cls, file_, size, file_number = 0, progress = 0):        return True
    @classmethod    def ui_update_progress(cls, current):        return True
    @classmethod    def ui_close_progress_bar(cls):        pass        #return cls.instance.ui_close_progress_bar()

    @classmethod    def ui_msg_continue(cls, msg, title="Continue"):        raw_input("%s: %s" % (title, msg))
    @classmethod    def ui_error_msg(cls, error = "An error accord"):        return True
    @classmethod    def ui_print_during_dump(cls, msg):        return True
    @classmethod    def ui_async_operation(cls, title, msg):        print "%s: %s" % (title, msg)

    @classmethod    def ui_read_password_message(cls):        return True
    @classmethod    def ui_extract_or_remove_password(cls):        return True
    @classmethod    def save_password_and_exit(cls, password):        return True
    @classmethod    def get_config(cls, file_name, expected_config_arguments) :        config_reader = ConfigReader()        return config_reader.get_config(file_name, expected_config_arguments)