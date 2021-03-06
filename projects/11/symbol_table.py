class SymbolTable(object):
    # symboles of a scope: ['name', 'type', 'kind', '#']
    def __init__(self):
        self.class_scope={}
        self.subroutine_scope ={} 
        self.class_index = 0
        self.subroutine_index = 0
        self.class_name = None
        self.subroutine_name = 'main'

    def start_subroutine(self):
        self.subroutine_scope = {} 
        self.subroutine_index = 0

    def define(self, name, type_, kind, index=None):
        # for compile let:
        # vars are first declared and then when defined, they are assigned an 
        # index. Args already have a defined value, so in case we are overwritting
        # and arg, there is no index changing
        if name in self.subroutine_scope:
            # if this is a var and its index is not None, then this is a mutation,
            # do not alter the index
            if kind != 'arg' and self.subroutine_scope[name]['index'] is None:
                self.subroutine_scope[name]['index'] = self.subroutine_index
                self.subroutine_index += 1
        elif name in self.class_scope:
            self.class_scope[name]['index'] = self.class_index
            self.class_index += 1
        elif kind in ('static', 'field'):
            self.class_scope[name] = {'type': type_, 'kind': kind, 'index': None}
        elif kind in ('arg', 'var'):
            index_ = self.subroutine_index
            if kind =='arg':
                # only index arguments when they are named, for variables, wait
                # until they are initialized and not just declared
                index_ = index
            self.subroutine_scope[name] = {'type': type_, 'kind': kind, 'index': index_}

            if kind == 'var':
                self.subroutine_index += 1

    def var_count(self, kind):
        assert kind in ('static', 'field', 'arg', 'var')
        # cannot mix the class and subroutine scope
        if kind in ('arg', 'var'):
            return len(filter(lambda x: x[1]['kind'] == kind.lower(), self.subroutine_scope.iteritems()))
        elif kind in ('static', 'field'):
            return len(filter(lambda x: x[1]['kind'] == kind.lower(), self.class_scope.iteritems()))
        
    def kind_of(self, name): # look up the scopes from bottom up
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['kind']
        elif name in self.class_scope:
            return self.class_scope[name]['kind']
        else:
            return None

    def type_of(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['type_']
        elif name in self.class_scope:
            return self.class_scope[name]['type_']

    def index_of(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['index']
        elif name in self.class_scope: 
            return self.class_scope[name]['index']
        else:
            return None