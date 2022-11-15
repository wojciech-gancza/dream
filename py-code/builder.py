#-------------------------------------------------------------------------
# DREAM (C) WGan 2020
#-------------------------------------------------------------------------

""" Builder provides construction of objects from files definition """

from errors    import error
from tools     import translator
from data      import location, \
                      name, \
                      description, \
                      properties, \
                      actions, \
                      item, \
                      items, \
                      realm
from compiler  import compiler

#-------------------------------------------------------------------------

class file_data_source(object):

    """ File data source returns file content as tokenizers which can be used
        in object builders and factories """

    def __init__(self, directory):
        self._directory = directory

    def get_data_set(self, name):
        unified_name = translator.make_identifier(name)
        filename = self._directory + "/" + unified_name + ".def"
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines

#-------------------------------------------------------------------------

class array_tokenizer(object):

    """ Array tokenizer reads array returning lines one by one
        When no more lines are avialable - getter return None
        It strips leading and trailing spaces from array elements """
    
    def __init__(self, data_array):
        self._data_array = data_array
        self._position = 0
        self._size = len(self._data_array)

    def get_token(self):
        if self._position >= self._size:
            return None
        else:
            result = self._data_array[self._position]
            self._position = self._position+1
            result = result.strip()
            if result != "":
                result = result.strip()
                if result[0] == "[":
                    return (True, result[1:-1])
                else:
                    return (False, result)
            else:
                return self.get_token()

#-------------------------------------------------------------------------

class buffered_token_source(object):

    """ Buffered data source adds 'rollback_token' to data source it is 
        based on. It has the same methods as data source, but allow also
        returning one (and only one) element to data source to take it
        once again by 'get_token' """

    def __init__(self, tokenizer):
        self._tokenizer = tokenizer
        self._use_buffered_value = True
        self._buffered_value = self._tokenizer.get_token()

    def get_token(self):
        if self._use_buffered_value:
            self._use_buffered_value = False
        else:
            self._buffered_value = self._tokenizer.get_token()
        return self._buffered_value
        
    def revert_laset_token(self):
        if self._use_buffered_value:
            raise error("Cannot rollback when data was not read")
        else:
            self._use_buffered_value = True

#-------------------------------------------------------------------------

class data_reader(object):

    """ data reader allow to read tokens or sources dependin of the need """
    
    def __init__(self, tokens):
        self._tokens = tokens
        
    def get_token(self, expects):
        data = self._tokens.get_token()
        if data is None:
            raise error("Expects " + expects + " but found end of data")
        data_is_token = data[0]
        data_value = data[1]
        if not data_is_token:
            raise error("Expects " + expects + " but found data '" + data_value + "'")
        return data_value
       
    def get_token_or_eof(self, expects):
        data = self._tokens.get_token()
        if data is None:
            return None
        data_is_token = data[0]
        data_value = data[1]
        if not data_is_token:
            raise error("Expects " + expects + " but found data '" + data_value + "'")
        return data_value
       
    def get_data(self, expects):
        data = self._tokens.get_token()
        if data is None:
            raise error("Expects " + expects + " but found end of data")
        data_is_token = data[0]
        data_value = data[1]
        if data_is_token:
            raise error("Expects " + expects + " but found token '[" + data_value + "]'")
        return data_value    

    def try_get_data(self):
        data = self._tokens.get_token()
        if data is None:
            return None
        data_is_token = data[0]
        data_value = data[1]
        if data_is_token:
            self._tokens.revert_laset_token()
            return None
        else:
            return data_value

#-------------------------------------------------------------------------

class object_builder(object):

    """ Object builder created objects based on data source content.
        It is used to construct elements fron text files. This class
        assume, that first element in data source is object name, and then
        all items are subobjects """
        
    @classmethod
    def get_object(class_object, token_source, repository = None):
        data_source = data_reader( buffered_token_source(token_source) )
        header = data_source.get_token("type")
        if header != 'type':
            raise error("Wrong type of first line - must be '[type]'")
        object_type_name = data_source.get_data("name of type")
        construction_code = translator.make_identifier(object_type_name) + "()"
        try:
            object = eval(construction_code)
        except:
            raise error("Cannot create object of type '" + object_type_name + "'")
        element_type = data_source.get_token_or_eof("with element name")
        while not element_type is None:
            if element_type == "description":
                element = object_builder._create_description(data_source)
            elif element_type == "name":
                element = object_builder._create_name(data_source)
            elif element_type == "properties":
                element = object_builder._create_properties(data_source)
            elif element_type == "items":
                element = object_builder._create_items(data_source, repository)
            elif element_type == "actions":
                element = object_builder._create_actions(data_source)
            elif element_type == "realm":
                element = object_builder._create_realm(data_source, repository)
            else:
                raise error("Unknows element type '" + element_type + "'")
            statement = "object._" + element_type + " = element"
            exec(statement)
            
            element_type = data_source.get_token_or_eof("with element name")
        
        return object
        
    @classmethod
    def _create_description(self, data_source):
        short_description = data_source.get_data("short description")
        long_description = data_source.get_data("long description")
        value = description()
        value.set_description(short_description, long_description)
        return value      
        
    @classmethod
    def _create_name(self, data_source):
        names = []
        name_text = data_source.try_get_data()
        while not name_text is None:
            names.append(name_text)
            name_text = data_source.try_get_data()
        value = name()
        value.set_names(names)
        return value      

    @classmethod
    def _create_properties(self, data_source):
        read_properties = properties()
        expression_text = data_source.try_get_data()
        while not expression_text is None: 
            elements = expression_text.split("=")
            if len(elements) != 2:
                raise error("Wrong format of property definition. Should be 'name = value', but is '" + expression_text + "'")
            property_name = elements[0].strip()
            try:
                property_value = int(elements[1].strip())
            except ValueError:
                raise error("Value of property must be integer, but is '" + elements[1].strip() + "'")
            read_properties.add(property_name, property_value)
            expression_text = data_source.try_get_data()
        return read_properties
        
    @classmethod
    def _create_actions(self, data_source):
        expression_text = data_source.try_get_data()
        acts = actions()
        comp = compiler()
        while not expression_text is None: 
            exe = comp.compile(expression_text)
            acts.add_action(exe)
            expression_text = data_source.try_get_data()
        return acts

    @classmethod
    def _create_realm(self, data_source, repository):
        name = data_source.try_get_data()
        if name is None:
            raise exception("Realm should not be empty.")
        obj = repository.get_object(name)
        return obj

    @classmethod
    def _create_items(self, data_source, repository):
        name = data_source.try_get_data()
        result = items()
        while not name is None:
            obj = repository.get_object(name)
            result.put_item(obj)
            name = data_source.try_get_data()
        return result

#-------------------------------------------------------------------------
 
class object_factory(object):

    """ Ready to use object factory crteating objects from data files 
        located in given directory """

    def __init__(self, directory):
        self._files_access = file_data_source(directory)

    def get_object(self, name):
        try:
            return object_builder.get_object(
                        array_tokenizer(
                            self._files_access.get_data_set(name) ), self )  
        except Exception as ex:
            raise error("Cannot create object named '" + name + "'")

#-------------------------------------------------------------------------

class factory_realm_cache(object):

    """ Factoried object cache - keeps realm object as long as it is 
        requested. Only one realm is kept in the cache, bacause 
        cache is changed rarely """
        
    def __init__(self, factory):
        self._factory = factory
        self._cached_object = None
        self._cached_object_name = ""
        
    def get_object(self, name):
        if self._cached_object_name == name:
            return self._cached_object
        obj = self._factory.get_object(name)
        if type(obj) is realm:
            self._cached_object = obj
            self._cached_object_name = name
        return obj
 
#-------------------------------------------------------------------------
 
class factory_location_cache(object):

    """ Factoried object cache - keeps last few accessible locations """
        
    def __init__(self, size, factory):
        self._factory = factory
        self._cache_size = size
        self._cached_objects_with_names = [ ]
        
    def get_object(self, name):
        for pair in self._cached_objects_with_names:
            if pair[0] == name:
                obj = pair[1]
                self._cached_objects_with_names.remove(pair)
                self._cached_objects_with_names.append((name, obj))
                return obj
        obj = self._factory.get_object(name)
        if type(obj) is location:
            if len(self._cached_objects_with_names) >= self._cache_size:
                self._cached_objects_with_names = self._cached_objects_with_names[1:]
            self._cached_objects_with_names.append( (name, obj) )
        return obj

#-------------------------------------------------------------------------


