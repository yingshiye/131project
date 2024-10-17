from intbase import InterpreterBase
from brewparse import parse_program

class Interpreter(InterpreterBase):

    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase's constructor

    def run(self, program):
        parsed_program = parse_program(program)
        program_node = parsed_program.elem_type
        if (program_node == 'program'):
            # parsed_program.dict['functions'] is not None
            # print(program_node['functions'])
            functions = parsed_program.dict.get('functions', [])
            print(functions)

        
        # c = parsed_program.get()
        # print(c)
        # function_code = get_main_function_code(parsed_program)
        # print(parsed_program)
        # print(Element.get( 'functions'))

        # this.variable_name_to_value = Map()  # dict to hold variables
		# main_func_node = get_main_func_node(ast)
		# run_func(main_func_node)

    # def run_function(self, func_Code):
    
    # def run_statment(self, statement_node):

    # Note: parsed_program is Element, that has 
    # <Element>.elem_type -> if value is program, it means this node is program node 
        # if value is func -> funciton node
    # <Element>.dict contains key 
    # <Element>.get(<key>)







program_source = """func main() {
    var x;
    x = 5 + 6;
    print("The sum is: ", x);
}
"""


a = Interpreter
a.run(a, program_source)