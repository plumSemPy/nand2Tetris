KEYWORD_CONSTANTS = ['true', 'false', 'null', 'this']
# TODO: potentially gotta replace & with &amp;
OPERATIONS = ['+', '-', '*', '/', '&', '|', '&lt;', '&gt;', '=']
UNARY_OPERATIONS = ['-', '~']



class Compiler(object):
    def __init__(self, file_address, compile_address):
        self.here = False
        self.file_object = open(file_address, 'rb')
        self.compiled = open(compile_address, 'wb')
        first_line = self.advance()
        self.current_line = first_line
        self.nest_level = 0

    def format_and_write_line(self):
       return self.compiled.write("{0}{1}\n".format(" "*self.nest_level*2, self.current_line))

    def words_exist(self, words):
        for word in words:
            if self.current_line.replace('</', '').find(word) != -1:
                continue
            else:
                return False
        return True

    def open_tag(self, tag_name):
        self.compiled.write("{0}{1}\n".format(" "*self.nest_level*2,"<{}>".format(tag_name)))
        self.nest_level += 1

    def close_tag(self, tag_name):
        self.nest_level -= 1
        self.compiled.write("{0}{1}\n".format(" "*self.nest_level*2,"</{}>".format(tag_name)))

    def advance(self):
        new_line = self.file_object.readline()
        if new_line == '':
            return
        else:
            self.current_line = new_line.strip()
            return
    def compileClass(self):
        self.open_tag("class")
        self.advance()

        if self.words_exist(['keyword','class']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['identifier']): # gotta regex for the name too
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['symbol', '{']):
            self.format_and_write_line()
            self.advance()
        else:
            raise

        while self.words_exist(['keyword', 'static']) or self.words_exist(['keyword', 'field']):
            self.compileClassVarDec()

        while self.words_exist(['keyword', 'function']) or self.words_exist(['keyword', 'constructor']) or self.words_exist(['keyword', 'method']):
            self.compileSubroutine()

        if self.words_exist(['symbol', '}']):
            self.format_and_write_line()
            self.advance()
        else:
            raise

        self.close_tag("class")

    def compileClassVarDec(self):
        self.open_tag("classVarDec")

        if self.words_exist(['keyword', 'static']) or self.words_exist(['keyword', 'field']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['int']) or self.words_exist(['char']) or self.words_exist(['boolean']) or self.words_exist(['identifier']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['identifier']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        has_next = lambda: self.current_line.find(',') != -1
        while has_next():
            if self.words_exist(['symbol', ',']):
                self.format_and_write_line()
                self.advance()
            if self.words_exist(['identifier']):
                self.format_and_write_line()
                self.advance()
        if self.words_exist(['symbol', ';']):
            self.format_and_write_line()
            self.advance()

        self.close_tag('classVarDec')


    def compileSubroutine(self):
        self.open_tag("subroutineDec")
        if self.words_exist(['keyword', 'constructor']) or self.words_exist(['keyword', 'function']) or self.words_exist(['keyword', 'method']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        # void, int etc are keywords, class names are identifiers
        if self.words_exist(['keyword']) or self.words_exist(['identifier']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['identifier']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['symbol', '(' ]):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        # no raise needed here cause its optional
        if self.words_exist(['keyword']): # we have parameters
            self.compileParameterList()
        else:
            self.open_tag('parameterList')
            self.close_tag('parameterList')
        if self.words_exist(['symbol',')']):
            self.format_and_write_line()
            self.advance()
        if self.words_exist(['{']):
            self.compileSubroutineBody()

        self.close_tag("subroutineDec")

    def compileParameterList(self):
        self.open_tag('parameterList')

        has_next = True
        while has_next:
            if self.words_exist(['identifier']) or self.words_exist(['keyword']):
                self.format_and_write_line()
                self.advance()
            else:
                raise
            if self.words_exist(['identifier']):
                self.format_and_write_line()
                self.advance()
            else:
                raise
            has_next = False
            if self.words_exist([',']):
                self.format_and_write_line()
                self.advance()
                has_next = True

        self.close_tag('parameterList')

    def compileSubroutineBody(self):
        self.open_tag('subroutineBody')

        if self.words_exist(['{']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        while self.words_exist(['keyword','var']):
            self.compileVarDec()
        while  self.words_exist(['if']) or self.words_exist(['let']) or self.words_exist(['while']) or self.words_exist(['do']) or self.words_exist(['return']):
            self.compileStatements()
        if self.words_exist(['}']):
            self.format_and_write_line()
            self.advance()

        self.close_tag('subroutineBody')

    def compileVarDec(self):
        self.open_tag('varDec')

        if self.words_exist(['var']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['keyword']) or self.words_exist(['identifier']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        has_next = True
        while has_next:
            if self.words_exist(['identifier']):
                self.format_and_write_line()
                self.advance()
                has_next = False
            if self.words_exist(['symbol', ',']):
                self.format_and_write_line()
                self.advance()
                has_next = True
        if self.words_exist(['symbol', ';']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        self.close_tag('varDec')

    def compileStatements(self):
        self.open_tag('statements')

        while self.words_exist(['keyword', 'let']) or self.words_exist(['keyword', 'if']) or self.words_exist(['keyword', 'while']) or self.words_exist(['keyword', 'do'] or self.words_exist(['keyword', 'return'])):
            if self.words_exist(['keyword', 'let']):
                self.compileLet()
            if self.words_exist(['keyword', 'if']):
                self.compileIf()
            if self.words_exist(['keyword', 'while']):
                self.compileWhile()
            if self.words_exist(['keyword', 'do']):
                self.compileDo()
            if self.words_exist(['keyword', 'return']):
                self.compileReturn()
        self.close_tag('statements')

    def compileDo(self):
        self.open_tag('doStatement')

        if self.words_exist(['keyword', 'do']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['identifier']):
            self.compileSubroutineCall()
        if self.words_exist(['symbol',';']):
            self.format_and_write_line()
            self.advance()

        self.close_tag('doStatement')

    def compileSubroutineCall(self, identifier_compiled = False):
        # no tags
        if self.words_exist(['identifier']) and not identifier_compiled:
            self.format_and_write_line()
            self.advance()
        if self.words_exist(['symbol','(']):
            # subroutine call
            self.format_and_write_line()
            self.advance()
            self.compileExpressionList()
            if self.words_exist(['symbol', ')']):
                self.format_and_write_line()
                self.advance()
        elif self.words_exist(['symbol', '.']):
            self.format_and_write_line()
            self.advance()
            if self.words_exist(['identifier']):
                self.format_and_write_line()
                self.advance()
            if self.words_exist(['symbol','(']):
                # subroutine call
                self.format_and_write_line()
                self.advance()
            # always compile expresionLists cause nothing is an expressionList
            self.compileExpressionList()
            if self.words_exist(['symbol', ')']):
                self.format_and_write_line()
                self.advance()
        else:
            raise

    def compileLet(self):
        self.open_tag('letStatement')
        if self.words_exist(['keyword', 'let']):
            self.format_and_write_line()
            self.advance()
        if self.words_exist(['identifier']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['symbol', '[']):
            self.format_and_write_line()
            self.advance()
            self.compileExpression()
            if self.words_exist(['symbol', ']']):
                self.format_and_write_line()
                self.advance()
            else:
                raise
        if self.words_exist(['symbol', '=']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        self.compileExpression()
        if self.words_exist(['symbol', ';']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        self.close_tag('letStatement')

    def compileWhile(self):
        self.open_tag('whileStatement')
        if self.words_exist(['while', 'keyword']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['symbol', '(']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        self.compileExpression()
        if self.words_exist(['symbol', ')']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['symbol', '{']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        self.compileStatements()
        if self.words_exist(['symbol', '}']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        self.close_tag('whileStatement')

    def compileReturn(self):
        self.open_tag('returnStatement')
        if self.words_exist(['return', 'keyword']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if not self.words_exist([';']):
            self.compileExpression()
        if self.words_exist([';', 'symbol']):
            self.format_and_write_line()
            self.advance()
        self.close_tag('returnStatement')

    def compileIf(self):
        self.open_tag('ifStatement')
        if self.words_exist(['if', 'keyword']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['symbol', '(']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        self.compileExpression()
        if self.words_exist(['symbol', ')']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['symbol', '{']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        self.compileStatements()
        if self.words_exist(['symbol', '}']):
            self.format_and_write_line()
            self.advance()
        else:
            raise
        if self.words_exist(['else', 'keyword']):
            self.here = True
            self.format_and_write_line()
            self.advance()
            if self.words_exist(['symbol', '{']):
                self.format_and_write_line()
                self.advance()
            else:
                raise
            self.compileStatements()
            if self.words_exist(['symbol', '}']):
                self.format_and_write_line()
                self.advance()
            else:
                raise
        self.close_tag('ifStatement')

    def compileExpression(self):
        def get_condition():
            res_list = []
            for op in OPERATIONS:
                res_list.append(self.words_exist([op]))
            res = False
            for r in res_list:
                res = res or r
            return res

        self.open_tag('expression')
        self.compileTerm()

        while get_condition():
            self.format_and_write_line()
            self.advance()
            self.compileTerm()
        self.close_tag('expression')

    def compileTerm(self):
        def get_condition():
            res_list = []
            for k in KEYWORD_CONSTANTS:
                res_list.append(self.words_exist([k]))
            res = False
            for r in res_list:
                res = res or r
            return res

        self.open_tag('term')
        if self.words_exist(['integerConstant']) or self.words_exist(['stringConstant']) or get_condition():
            self.format_and_write_line()
            self.advance()
        elif self.words_exist(['identifier']):
            self.format_and_write_line()
            self.advance()
            # if there is a [ next
            if self.words_exist(['symbol', '[']):
                self.format_and_write_line()
                self.advance()
                self.compileExpression()
                if self.words_exist(['symbol', ']']):
                    self.format_and_write_line()
                    self.advance()
                else:
                    raise
            # if there is a ( next subroutine call
            elif self.words_exist(['(']) or self.words_exist(['.']):
                self.compileSubroutineCall(identifier_compiled=True)

        elif self.words_exist(['(', 'symbol']):
            self.format_and_write_line()
            self.advance()
            self.compileExpression()
            if self.words_exist([')', 'symbol']):
                self.format_and_write_line()
                self.advance()
            else:
                raise
        elif self.words_exist(['-']) or self.words_exist(['~']):
            self.format_and_write_line()
            self.advance()
            self.compileTerm()
        else:
            raise
        self.close_tag('term')

    def compileExpressionList(self):
        self.open_tag('expressionList')
        has_next = (self.current_line.find(')') == -1)
        while has_next:
            self.compileExpression()
            has_next = False
            if self.words_exist([',']):
                self.format_and_write_line()
                self.advance()
                has_next = True

        self.close_tag('expressionList')
