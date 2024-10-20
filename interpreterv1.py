from intbase import InterpreterBase, ErrorType
from brewparse import parse_program

class Interpreter(InterpreterBase):

    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase's constructor
        self.variables = []


    def evaluate_expression(self, expression):
        if (expression.elem_type == '+'): #expression operator node
            # pass #temp
            # need to check type
            operator1 = self.evaluate_expression(expression.dict.get('op1', []))
            operator2 = self.evaluate_expression(expression.dict.get('op2', []))
            if (type(operator1) is type(operator2)):
                expression_result = operator1 + operator2
                return expression_result
            else:
                super().error(ErrorType.TYPE_ERROR, "not the same type of variables for operation")

        elif (expression.elem_type == '-'):
            operator1 = self.evaluate_expression(expression.dict.get('op1', []))
            operator2 = self.evaluate_expression(expression.dict.get('op2', []))
            # print(type(operator2))
            # print(type(operator1))
            if (type(operator1) is type(operator2)):
                expression_result = operator1 - operator2
                return expression_result
            else:
                super().error(ErrorType.TYPE_ERROR, "not the same type of variables for operation")

        elif (expression.elem_type == 'var'): # variable node
            # return self.elaluate_expression(self, expression.dict.get('name'))
            expression_variable = expression.dict.get('name', [])
            for var in self.variables: 
                if (var[0] == expression_variable): # find variable
                    if (var[1] is not None):
                        return var[1]
                    # else variable empty error
            super().error(ErrorType.NAME_ERROR, "variable is not defined")

        elif (expression.elem_type == 'string'): #value node
            return expression.dict.get('val', [])
        
        elif (expression.elem_type == 'int'): #value node
            return expression.dict.get('val', [])
        
        elif (expression.dict.get('name') == "inputi"):
            return self.run_fcall(expression)
        

    def run_fcall(self, fcall_Node): #print() and inputi()
        argsNode = fcall_Node.dict.get('args', [])
        if (fcall_Node.dict.get('name') == "print"): # can't in the expression
            result = str(self.evaluate_expression(argsNode[0]))
            for i in range(1, len(argsNode)):
                if (type(self.evaluate_expression(argsNode[i]) is int)):
                    result += str(self.evaluate_expression(argsNode[i]))
                else:
                    result += self.evaluate_expression(argsNode[i])
            super().output(result)

        elif (fcall_Node.dict.get('name') == "inputi"): # only one or no parameters, need to get input
            if (len(argsNode) > 1):
                super().error(ErrorType.NAME_ERROR, f"No inputi() function found that takes > 1 parameter")
            if (len(argsNode) == 1):
                argsStr = argsNode[0].dict.get('val')
                super().output(argsStr);
            user_input = super().get_input()
            user_input = int(user_input)
            return user_input
        else: 
            super().error(ErrorType.NAME_ERROR, f"Function has not been defined")



    def run_statement(self, statement_node):
        if (statement_node.elem_type == 'vardef'): # variable definition
            varName = statement_node.dict.get('name')
            for var in self.variables: 
                if (var[0] == varName):
                    # print("double defined")
                    super().error(ErrorType.NAME_ERROR, f"Variable is defined more than once")
            self.variables.append((statement_node.dict.get('name'), None))
            # print(self.variables)
        elif (statement_node.elem_type == '='):
            # print(statement_node.dict.get('name', []))
            for i, var in enumerate(self.variables): # asked gpt about how to chagne tuple inside of the list while looping it 
                if (var[0] == statement_node.dict.get('name', [])): # find variable
                    # print(statement_node.dict.get('name', []))
                    expression = statement_node.dict.get('expression', []) #get the expression arguement for the variables 
                    # print(expression)
                    result = self.evaluate_expression(expression)
                    self.variables[i] = (statement_node.dict.get('name', []), result)
                    return
                    # print(self.variables)
            super().error(ErrorType.NAME_ERROR, "variable is not defined")
                # else , which is the variable not exist
        elif (statement_node.elem_type == 'fcall' and statement_node.dict.get('name') == "print"):
            self.run_fcall(statement_node)
        else:
            super().error(ErrorType.NAME_ERROR, "wrong statement call")
        

    def run_function(self, func_Code): 
        # print(func_Code)
        statements_Node = func_Code.dict.get('statements', [])
        for statements in statements_Node: 
            # print(statements.elem_type)
            self.run_statement(statements)
            

    def run(self, program):
        parsed_program = parse_program(program)
        program_node = parsed_program.elem_type
        if (program_node == 'program'):
            # parsed_program.dict['functions'] is not None
            # print(program_node['functions'])
            functions = parsed_program.dict.get('functions', [])
            if functions is not None:
                for func in functions:
                    if (func.dict.get('name') == 'main'):
                        self.run_function(func)
                        return
                    super().error(ErrorType.NAME_ERROR, "No main()")


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




# program_source = """func main() {
#     var x;
#     x = 3 - (3 + (2 + inputi()));
#     print(x);
# }
# """

#     # print("The sum is: ", x);

# a = Interpreter()
# a.run(program_source)


# /*
# *IN*
# 15
# *IN*
# *OUT*
# Hello
# 15
# *OUT*
# */
