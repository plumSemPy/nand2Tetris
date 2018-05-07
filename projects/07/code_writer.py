class CodeWriter(object):
    def __init__(self, filename):
        self.file_object = open(filename, 'wb')
        self.counter = 0

    def write_init(self):
       assembly="""
       @SP
       M=256  // initialize the stack
       call Sys.init 0
       """
       self.file_object.write(assembly)

    def write_arithmetic(self, command):
        assembly = ''
        self.counter += 1
        if command == 'add':
            assembly = """
            ///////
            //ADD//
            //////
            @SP  // get the stack
            M=M-1 // the current stack position is empty
            A=M  // go to the top of the stack

            D=M  // save that number

            // I decided not to clean up the stack to zero
            // cause I don't think that is necessary

            @SP  // decrease the stack pointer
            M=M-1

            A=M  // go to the next number
            D=D+M // add

            M=D  // put it back in the stack

            @SP
            M=M+1
            """
        if command == 'sub':
            assembly = """
            ///////
            //SUB//
            //////
            @SP  // get the stack
            M=M-1 // the current stack position is empty
            A=M  // go to the top of the stack

            D=-M  // save that number

            // I decided not to clean up the stack to zero
            // cause I don't think that is necessary

            @SP  // decrease the stack pointer
            M=M-1

            A=M  // go to the next number
            D=D+M // add

            M=D  // put it back in the stack

            @SP
            M=M+1
            """
        if command == 'neg':
            assembly = """
            ///////
            //NEG//
            //////
            @SP  // get the stack
            M=M-1 // the current stack position is empty
            A=M  // go to the top of the stack

            M=-M  // save that number

            @SP
            M=M+1
            """
        if command == 'eq':
            assembly = """
            ///////
            //EQ//
            //////
            @SP  // get the stack
            M=M-1 // the current stack position is empty
            A=M  // go to the top of the stack

            D=M  // save that number

            // I decided not to clean up the stack to zero
            // cause I don't think that is necessary

            @SP  // decrease the stack pointer
            M=M-1
            A=M  // go to the next number

            D=D-M
            @TRUE{0}
            D;JEQ
            @SP  // return false
            A=M
            M=0
            @END{0}
            0;JMP

            (TRUE{0})
              @SP  // return true
              A=M
              M=-1
              @END{0}
              0;JMP

            (END{0})
              @SP
              M=M+1
            """.format(self.counter)
        if command == 'gt':
            assembly = """
            ///////
            //GT//
            //////
            @SP  // get the stack
            M=M-1 // the current stack position is empty
            A=M  // go to the top of the stack

            D=M  // save that number

            // I decided not to clean up the stack to zero
            // cause I don't think that is necessary

            @SP  // decrease the stack pointer
            M=M-1
            A=M  // go to the next number

            D=D-M
            @TRUE{0}
            D;JLT
            @SP  // return false
            A=M
            M=0
            @END{0}
            0;JMP

            (TRUE{0})
              @SP  // return true
              A=M
              M=-1
              @END{0}
              0;JMP

            (END{0})
              @SP
              M=M+1
            """.format(self.counter)
        if command == 'lt':
            assembly = """
            ///////
            //LT//
            //////
            @SP  // get the stack
            M=M-1 // the current stack position is empty
            A=M  // go to the top of the stack

            D=M  // save that number

            // I decided not to clean up the stack to zero
            // cause I don't think that is necessary

            @SP  // decrease the stack pointer
            M=M-1
            A=M  // go to the next number

            D=D-M
            @TRUE{0}
            D;JGT
            @SP  // return false
            A=M
            M=0
            @END{0}
            0;JMP

            (TRUE{0})
              @SP  // return true
              A=M
              M=-1
              @END{0}
              0;JMP

            (END{0})
              @SP
              M=M+1
            """.format(self.counter)
        if command == 'and':
            assembly = """
            ///////
            //AND//
            //////
            @SP  // get the stack
            M=M-1 // the current stack position is empty
            A=M  // go to the top of the stack

            D=M  // save that number

            // I decided not to clean up the stack to zero
            // cause I don't think that is necessary

            @SP  // decrease the stack pointer
            M=M-1

            A=M  // go to the next number
            D=D&M

            M=D  // put it back in the stack

            @SP
            M=M+1
            """
        if command == 'or':
            assembly = """
            ///////
            //OR//
            //////
            @SP  // get the stack
            M=M-1 // the current stack position is empty
            A=M  // go to the top of the stack

            D=M  // save that number

            // I decided not to clean up the stack to zero
            // cause I don't think that is necessary

            @SP  // decrease the stack pointer
            M=M-1

            A=M  // go to the next number
            D=D|M

            M=D  // put it back in the stack

            @SP
            M=M+1
            """
        if command == 'not':
            assembly = """
            ///////
            //NOT//
            //////
            @SP  // get the stack
            M=M-1 // the current stack position is empty
            A=M  // go to the top of the stack

            M=!M  // save that number

            @SP
            M=M+1
            """

        self.file_object.write(assembly)


    def write_push_pop(self, command, segment, index):
        SEGMENT_MAPPING = {
            'constant': 'SP',
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'static': 'NOT',
        }
        assembly = ''
        if command == 'C_PUSH':
            assembly= """
            //////////
            // PUSH //
            //////////
        """
            # get the value to be pushed
            if segment == 'constant':
                assembly += """
            @{}
            D=A
                """.format(index)
            elif segment == 'temp':
                TEMP_MAPPING = {
                    0: 5,
                    1: 6,
                    2: 7,
                    3: 8,
                    4: 9,
                    5: 10,
                    6: 11,
                    7: 12
                }
                assembly += """
            @R{}
            D=M
            """.format(TEMP_MAPPING[int(index)])

            elif segment == 'static':
                address = 16 + int(index)
                assembly += """
            @{}
            D=M
            """.format(address)

            elif segment == 'pointer':
                POINTER_MAPPING = {
                    0: 'THIS',
                    1: 'THAT'
                }
                assembly="""
            @{}
            D=M
            """.format(POINTER_MAPPING[int(index)])

            else:
                assembly += """
            @{0}  // get the offset
            D=A
            @{1}  // get the memory
            A=M+D // go to the index
            D=M   // get the value
                """.format(index, SEGMENT_MAPPING[segment])


            assembly +="""
            @SP  // get the stack
            A=M   // go to that address

            M=D   // save the value

            @SP
            M=M+1  // increase the stack pointer
        """

        if command == 'C_POP':
            assembly="""
            ///////
            //POP//
            ///////
            """
            if segment == 'temp':
                TEMP_MAPPING = {
                    0: 5,
                    1: 6,
                    2: 7,
                    3: 8,
                    4: 9,
                    5: 10,
                    6: 11,
                    7: 12
                }
                assembly += """
            @SP   // get the stack
            M=M-1 // decreas the stack pointer
            A=M   // go to that address

            D=M   // save the value

            @R{}
            M=D   // put the stack value there
            """.format(TEMP_MAPPING[int(index)])

            elif segment == 'static':
                address = 16 + int(index)
                assembly += """
            @SP   // get the stack
            M=M-1 // decreas the stack pointer
            A=M   // go to that address

            D=M   // save the value

            @{}
            M=D   // put the stack value there
            """.format(address)

            elif segment == 'pointer':
                POINTER_MAPPING = {
                   0: 'THIS',
                   1: 'THAT'
                }
                assembly += """
            @SP   // get the stack
            M=M-1 // decreas the stack pointer
            A=M   // go to that address

            D=M   // save the value

            @{}
            M=D   // put the stack value there
            """.format(POINTER_MAPPING[int(index)])

            else:
                assembly += """
            @{0}  // get the offset
            D=A
            @{1}  // get the memory
            D=M+D // save the address

            @R13
            M=D   // put the address in a general register

            @SP   // get the stack
            M=M-1 // decreas the stack pointer
            A=M   // go to that address

            D=M   // save the value

            @R13
            A=M   // go to the saved address
            M=D   // put the stack value there
            """.format(index, SEGMENT_MAPPING[segment])


        self.file_object.write(assembly)

    def write_label(self, label):
        self.file_object.write(
        """({})""".format(label)
        )

    def write_goto(self,label):
        self.file_object.write("""
        @{}    // load the label address and jump to it
        0;JMP
        """.format(label)
        )

    def write_if(self, label):
       self.file_object.write("""
       @SP    // get the stack
       M=M-1  // decrease the pointer
       A=M    // go to that address

       D=M    // save the value

       @{}    // load the label address
       D;JNE  // jump if D is not equal to zero
       """.format(label)
       )

    def write_call(function_name, num_args):
        pass

    def write_return(self):
        assembly="""
        @5
        D=A
        @LCL
        A=M-D // go to the return
        D=M   // save the return address in R13
        @R13
        M=D

        // put the top of the stack in arg 0 which will be the top of the stack for the caller
        @SP   // get the stack
        M=M-1 // decrease the stack pointer
        A=M   // go to that address

        D=M   // save the value

        @ARG // go to ARG
        A=M   // go to the saved address
        M=D   // put the stack value there

        @ARG
        D=M
        @SP
        M=D+1   // reposition the stack

        @LCL    // restore THAT
        A=M-1
        D=M
        @THAT
        M=D

        @2
        D=A
        @LCL    // restore THIS
        A=M-D
        D=M
        @THIS
        M=D

        @3
        D=A
        @LCL    // restore ARG
        A=M-D
        D=M
        @ARG
        M=D

        @4
        D=A
        @LCL    // restore LCL
        A=M-D
        D=M
        @LCL
        M=D

        @R13    // go to the saved RET
        A=M
        """
        self.file_object.write(assembly)

    def write_function(self, function_name, num_locals):
        assembly="""
        ({0})
        """.format(function_name)

        self.file_object.write(assembly)
        for i in range(int(num_locals)): # initialize all local vars to zero
            self.write_push_pop('C_PUSH', 'constant', 0)
            self.write_push_pop('C_POP', 'local', i)

    def close(self):
        self.file_object.write("""
            (INFINITE_LOOP)
              @INFINITE_LOOP
              0;JMP""")
        self.file_object.close()
