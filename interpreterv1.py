from intbase import InterpreterBase, ErrorType
from brewparse import parse_program

class Interpreter(InterpreterBase):

    variables = []

    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase's constructor

    def evaluate_expression(self, expression):
        if (expression.elem_type('+')): #expression operator node
            # pass #temp
            operator1 = self.evaluate_expression(self, expression.dict.get('op1', []))
            operator2 = self.evaluate_expression(self, expression.dict.get('op2', []))
            expression_result = operator1 + operator2
            return expression_result

        elif (expression.elem_type('-')):
            operator1 = self.evaluate_expression(self, expression.dict.get('op1', []))
            operator2 = self.evaluate_expression(self, expression.dict.get('op2', []))
            expression_result = operator1 - operator2
            return expression_result
        
        elif (expression.elem_type('var')): # variable node
            # return self.elaluate_expression(self, expression.dict.get('name'))
            for var in self.variables: 
                if (var[0] == expression.dict.get('name', [])): # find variable
                    if (var[1] is not None):
                        return var[1]
                    # else variable empty error
            # pass

        elif (expression.elem_type('string')): #value node
            return expression.dict.get('val', [])
        
        elif (expression.elem_type('int')): #value node
            return expression.dict.get('val', [])
        

    def run_fcall(self, fcall_Node): #print() and inputi()
        if (fcall_Node.elem_type == "print"):
            pass
        if (fcall_Node.elem_type == "inputi"):
            pass

    def run_statement(self, statement_node):
        if (statement_node.elem_type == 'vardef'): # variable definition
            self.variables.append((statement_node.dict.get('name'), None))
            # print(self.variables)
        if (statement_node.elem_type == '='):
            # print(statement_node.dict.get('name', []))
            for var in self.variables: 
                if (var[0] == statement_node.dict.get('name', [])): # find variable
                    expression = statement_node.dict.get('expression', []) #get the expression arguement for the variables 
                    # print(expression)
                    result = self.evaluate_expression(self, expression)
                # else , which is the variable not exist
        if (statement_node.elem_type == 'fcall'):
            self.run_fcall(self, statement_node)

    def run_function(self, func_Code): 
        # print(func_Code)
        statements_Node = func_Code.dict.get('statements', [])
        for statements in statements_Node: 
            # print(statements.elem_type)
            self.run_statement(self, statements)
            

    def run(self, program):
        parsed_program = parse_program(program)
        program_node = parsed_program.elem_type
        if (program_node == 'program'):
            # parsed_program.dict['functions'] is not None
            # print(program_node['functions'])
            functions = parsed_program.dict.get('functions', [])
            if (functions is not None):
                for func in functions:
                    self.run_function(self, func)
            else:
                super().error(ErrorType.NAME_ERROR, "No main() function was found",)

                    
            # print(functions)
            # print(type(functions))
            # print(functions[0].elem_type)


        
        # c = parsed_program.get()
        # print(c)
        # function_code = get_main_function_code(parsed_program)
        # print(parsed_program)
        # print(Element.get( 'functions'))

        # this.variable_name_to_value = Map()  # dict to hold variables
		# main_func_node = get_main_func_node(ast)
		# run_func(main_func_node)


    


    # Note: parsed_program is Element, that has 
    # <Element>.elem_type -> if value is program, it means this node is program node 
        # if value is func -> funciton node
    # <Element>.dict contains key 
    # <Element>.get(<key>)







program_source = """func main() {
    var x;
    x = 5 + 6 + 7;
    print("The sum is: ", x);
}
"""


a = Interpreter
a.run(a, program_source)