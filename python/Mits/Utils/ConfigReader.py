import xmltodictimport os

class ScriptConfigObject(object) :    """    Configuration object for tester script    This class is being created by the ConfigReader class.    the configuration variables are being add dynamicly to instance of this class
    usage example (when "debug" is a script configuration parameter):        reader = ConfigReader()        script_config_object = reader.get_config()        is_debug = script_config_object.debug    """    def __init__(self) :        pass
    @classmethod    def eval_bool_value(cls, value_) :        if value_.lower() == 'false' :            v = False        elif value_.lower() == 'true' :            v = True        else :            raise ValueError("Parsing error for attr(%s) - type(%s) with value (%s) is ilegal" % (name, type_, value_))        return v
    @classmethod    def eval_config_value(cls, value_) :        v = value_        if value_.lower() == 'true' or value_.lower() == 'false' :            v = cls.eval_bool_value(value_)        else :            try :                v = eval(value_)            except :                v = str(value_)                        return v

class ConfigReader(object) :    """    Configuration Reader Object    This class is reader the configuration for XML, the following structure is expected :        <dataroot xmlns:od="urn:schemas-microsoft-com:officedata" generated="2005-05-18T13:59:36">          <PHONE>            <CGuid>0</CGuid>            <argName1>ARGVALUE1</argName1>            <argName2>ARGVALUE2</argName2>              </PHONE>        </dataroot>        The type is evaluated by the class, numbers will be converted to int,     true/false to bool...     """
    MAIN_NODE_NAME1 = 'dataroot'    MAIN_NODE_NAME2 = 'PHONE'        def __init__(self) :        self.config = None        self.xml_dict = None        # this dictionary holds the configuration in the following way :        # {param name: value, ... }        self.configuration_dict = {}        self.argument_validation_list = {}

    def _set_argument_validation_list(self, args_list) :        """        This method used to initialize the known arguments that are expected to be at the XML        - it is not a must to initilize it in order to use the class but it is recomended
        * if an argument is found at the XML but not at the args_list - a warning will be printed        * if an argument is found at the args_list but not at the XML - an exception will be raised        """        self.argument_validation_list = dict(zip(args_list,[False]*len(args_list)))


    def get_config(self, file_name, argument_list) :        if self.config is None :            self._set_argument_validation_list(argument_list)            self._read_file(file_name)            self._create_config()
        return self.config

    def _read_file(self, file_name) :        """        Read file - translate it to xml dictionary        """        fn = os.path.join(os.path.dirname(__file__), '..', 'Configuration', file_name)        xml_file_ = file(fn, "r")        xml_data = xml_file_.read()        xml_file_.close()
        self.xml_dict = xmltodict.parse(xml_data)        self.xml_dict = self.xml_dict[self.MAIN_NODE_NAME1][self.MAIN_NODE_NAME2]
        def _add_config_value(self, k, v_):        v = ScriptConfigObject.eval_config_value(v_)        self.configuration_dict[k] = v        print "Configuration : %s --> %s" % (k, v)        self.config.__setattr__(k, v)        try:                        value = self.argument_validation_list[k]            self.argument_validation_list[k] = True                    except KeyError :            print "Warning : Key %s found at the XML but was not expected!" % (k)
    def _validate(self):        for k, is_found in self.argument_validation_list.iteritems() :            if not is_found :                raise KeyError("Configuration '%s' was not found at the XML !" % (k))        
    def _create_config(self) :        if self.xml_dict is None :            raise RuntimeError("No file was initilized !")
        self.config = ScriptConfigObject()        for key, value in self.xml_dict.iteritems() :            k = str(key) # change from unicode to str            value_str = value            if value_str == dict :                try :                                    value_str = value['#text']                except (TypeError, KeyError) :                    raise ValueError("Parsing error for attr('%s') - format should be as follows : <param>value<param>" % (k))                        self._add_config_value(k, value_str)        self._validate()



if __name__ == '__main__' :    r = ConfigReader(r"D:\Cellebrite\projects\UFED\Br\UFEDPython\Genesis\XML DB\DataFiles\Scripts\SamsungDefaultScriptConfig.xml")    c = r.get_config()    print c    print dir(c)    print type(c.lcd_off)