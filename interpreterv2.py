# Add to spec:
# - printing out a nil value is undefined

from env_v1 import EnvironmentManager
from type_valuev1 import Type, Value, create_value, get_printable
from intbase import InterpreterBase, ErrorType
from brewparse import parse_program


# Main interpreter class
class Interpreter(InterpreterBase):
    # constants
    BIN_OPS = {"+", "-", "*", "/"}
    COMP_OPS = {"==", "!=", "<", "<=", ">", ">="}
    COND_OPS = {"&&", "||"}

    # methods
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.trace_output = trace_output
        self.__setup_ops()
        # self.inScope = False

    # run a program that's provided in a string
    # usese the provided Parser found in brewparse.py to parse the program
    # into an abstract syntax tree (ast)
    def run(self, program):
        ast = parse_program(program)
        self.__set_up_function_table(ast)
        main_func = self.__get_func_by_name("main", 0)
        self.env = EnvironmentManager()
        self.__run_statements(main_func.get("statements"))

    def __set_up_function_table(self, ast):
        self.func_name_to_ast = {}
        for func_def in ast.get("functions"):
            self.func_name_to_ast[(func_def.get("name"), len(func_def.get("args")))] = func_def

    def __get_func_by_name(self, name, arg_len):
        key = (name, arg_len)
        if key in self.func_name_to_ast:
            return self.func_name_to_ast[key]
        # if name not in self.func_name_to_ast:
        super().error(ErrorType.NAME_ERROR, f"Function {name} not found")

    
    def __execute_func(self, call_ast):
        # print("check") #temp
        passIn_arg = call_ast.get("args") #only contain the value, not the variable name
        passIn_argV = []
        for v in passIn_arg: 
            passIn_argV.append(self.__eval_expr(v))
        # ard has function name, the argument pass in 
        # print(arg)
        func = self.__get_func_by_name(call_ast.get("name"), len(passIn_arg)) # find the function node
        func_statements = func.get("statements") # the statement need to run
        func_arg = func.get("args")
        self.env.new_scope_func()
        for arg1, arg2 in zip(func_arg, passIn_argV):
            var_name = arg1.get("name")
            var_value = arg2
            self.env.create(var_name, var_value)
        # print(func_arg) # contiain the arg name
        # print(passIn_arg) # the pass in argument value 

        # put arguments into the function scope
        #run statement
        returnValue = self.__run_statements(func_statements)
        self.env.notInScope_func()
        if returnValue is not None: 
            return returnValue
        else:
            return Value(Type.NIL, None)
        
        # containReturn = False
        # for statement in func_statements: 
        #     if statement.elem_type == "return" and statement.get("expression").elem_type != "nil":
        #         containReturn = True
        #         return returnValue
        # if containReturn == False: 
        #     return Value(Type.NIL, None)
        
        
        # idea: 
        # push the arg var and value into local stack for the function
        # and then isScope is true to run the whole funciton 
        # good night 
        # the argument pass into func should be in the local scope which is the function scope
        # life is too freaking good 

    def __run_statements(self, statements):
        # all statements of a function are held in arg3 of the function AST node
        for statement in statements:
            if self.trace_output:
                print(statement)
            if statement.elem_type == InterpreterBase.FCALL_NODE:
                returnValue = self.__call_func(statement)
                if returnValue is not None: 
                    if (type(returnValue) is Value) and returnValue.value() is not None:
                        return returnValue
            elif statement.elem_type == "=":
                self.__assign(statement)
            elif statement.elem_type == InterpreterBase.VAR_DEF_NODE:
                self.__var_def(statement)
            elif statement.elem_type == InterpreterBase.IF_NODE: # need scope
                returnValue = self.__call_if(statement)
                if returnValue is not None: 
                    return returnValue
            elif statement.elem_type == InterpreterBase.RETURN_NODE: # return what's in the scope first 
                return self.__call_return(statement)
            elif statement.elem_type == InterpreterBase.FOR_NODE: # need scope 
                returnValue = self.__call_for(statement)
                if returnValue is not None: 
                    return returnValue

    def __call_func(self, call_node):
        func_name = call_node.get("name")
        arg_len = len(call_node.get("args"))
        if func_name == "print":
            return self.__call_print(call_node)
        if func_name == "inputi":
            return self.__call_input(call_node)
        if func_name == "inputs":
            return self.__call_input(call_node)
        if self.__get_func_by_name(call_node.get("name"), arg_len):
            return self.__execute_func(call_node)

        # add code here later to call other functions
        super().error(ErrorType.NAME_ERROR, f"Function {func_name} not found")

    def __call_print(self, call_ast):
        output = ""
        for arg in call_ast.get("args"):
            result = self.__eval_expr(arg)  # result is a Value object
            output = output + get_printable(result)
        super().output(output)
        return Value(Type.NIL, None)

    def __call_input(self, call_ast):
        args = call_ast.get("args")
        if args is not None and len(args) == 1:
            result = self.__eval_expr(args[0])
            super().output(get_printable(result))
        elif args is not None and len(args) > 1:
            super().error(
                ErrorType.NAME_ERROR, "No inputi() function that takes > 1 parameter"
            )
        inp = super().get_input()
        if call_ast.get("name") == "inputi":
            return Value(Type.INT, int(inp))
        elif call_ast.get('name') == "inputs": 
            return Value(Type.STRING, inp)
        # we can support inputs here later
    
    def __call_if(self, call_ast):  
        cond_result = self.__eval_expr(call_ast.get("condition")) # evaluate condition, return Value
        if cond_result.type() is not Type.BOOL:
            super().error(
                ErrorType.TYPE_ERROR, "need Boolean to evalute the condition"
            )
        if cond_result.value():
            self.env.new_scope()
            returnValue = self.__run_statements(call_ast.get("statements"))
            self.env.notInScope()
            return returnValue
            # print("hi")
        else:
            else_statements = call_ast.get("else_statements")
            if else_statements is not None:
                self.env.new_scope()
                returnValue = self.__run_statements(else_statements)
                self.env.notInScope()
                return returnValue
            # print("by")
        
        
    def __call_return(self, call_ast):
        cond = call_ast.get("expression")
        if cond is not None and cond.elem_type != "nil":
            return self.__eval_expr(cond)
        else: 
            return Value(Type.NIL, None)
    
    def __call_for(self, call_ast):
        # self.inScope = True
        init_cond = call_ast.get("init")
        check_cond = call_ast.get("condition")
        update_var = call_ast.get("update")
        true_statements = call_ast.get("statements")
        
        self.__assign(init_cond)
            # var_name = init_cond.get("name")
            # var_initV = self.__eval_expr(init_cond.get("expression"))
            # variable = (var_name, var_initV)
        cond = self.__eval_expr(check_cond) # return a Value (bool, True/False)
        if cond.type() is not Type.BOOL:
            super().error(
                ErrorType.TYPE_ERROR, "need Boolean to evalute the condition"
            )
            # print(type(init_cond))
        while(cond.value()): # while condition is true
            self.env.new_scope()
            returnValue = self.__run_statements(true_statements)
            self.env.notInScope()
            if returnValue is not None: 
                return returnValue
            self.__assign(update_var)
            cond = self.__eval_expr(check_cond)

    def __assign(self, assign_ast):
        var_name = assign_ast.get("name")
        value_obj = self.__eval_expr(assign_ast.get("expression"))
        if not self.env.set(var_name, value_obj):
            super().error(
                ErrorType.NAME_ERROR, f"Undefined variable {var_name} in assignment"
            )

    def __var_def(self, var_ast):
        var_name = var_ast.get("name")
        if not self.env.create(var_name, Value(Type.INT, 0)):
            super().error(
                ErrorType.NAME_ERROR, f"Duplicate definition for variable {var_name}"
            )

    def __eval_expr(self, expr_ast):
        if expr_ast.elem_type == InterpreterBase.INT_NODE:
            return Value(Type.INT, int(expr_ast.get("val")))
        if expr_ast.elem_type == InterpreterBase.STRING_NODE:
            return Value(Type.STRING, expr_ast.get("val"))
        if expr_ast.elem_type == InterpreterBase.BOOL_NODE:
            return Value(Type.BOOL, expr_ast.get("val"))
        if expr_ast.elem_type == InterpreterBase.NIL_NODE:
            return Value(Type.NIL, None)
        
        if expr_ast.elem_type == InterpreterBase.VAR_NODE:
            var_name = expr_ast.get("name")
            val = self.env.get(var_name)
            if val is None:
                super().error(
                    ErrorType.NAME_ERROR, f"Variable {var_name} not found")
            return val
        
        if expr_ast.elem_type == InterpreterBase.FCALL_NODE:
            return self.__call_func(expr_ast)
        
        if expr_ast.elem_type in Interpreter.BIN_OPS: # +-*/ for int, + for string
            return self.__eval_op(expr_ast)
        
        if expr_ast.elem_type in Interpreter.COMP_OPS: # == != >= > < <=
            return self.__eval_op(expr_ast)
        
        if expr_ast.elem_type in Interpreter.COND_OPS: # &&, ||
            return self.__eval_op(expr_ast)       
        
        if expr_ast.elem_type == InterpreterBase.NEG_NODE: # negative value
            pos_val = expr_ast.get("op1") #return list of value
            if pos_val.elem_type == InterpreterBase.VAR_NODE or pos_val.elem_type == InterpreterBase.NEG_NODE:
                val_Value = self.__eval_expr(pos_val)
                if val_Value.type() != Type.INT:
                    super().error(
                        ErrorType.TYPE_ERROR, f"neg_node only works for integer",
                    )
            elif pos_val.elem_type != InterpreterBase.INT_NODE:
                super().error(
                    ErrorType.TYPE_ERROR, f"neg_node only works for integer",
                )
            # print(type(pos_val))
            elif pos_val.elem_type == InterpreterBase.INT_NODE:
                val_Value = self.__eval_expr(pos_val) # reutrn Value 
            val = val_Value.value() # return the abs value of neg 
            negval = 0 - val # becomse neg
            return Value(Type.INT, negval) #return Value
        
        if expr_ast.elem_type == InterpreterBase.NOT_NODE: # opposite value
            bol_val = expr_ast.get("op1")
            if (bol_val.elem_type == InterpreterBase.BOOL_NODE or 
                bol_val.elem_type == InterpreterBase.VAR_NODE or 
                bol_val.elem_type == InterpreterBase.NOT_NODE):
                    bol_Value = self.__eval_expr(bol_val)
                    # print(type(bol_Value), "hi")
                    if bol_Value.value() == True:
                        return Value(Type.BOOL, False)
                    elif bol_Value.value() == False:
                        return Value(Type.BOOL, True)
            else:
                super().error(
                    ErrorType.TYPE_ERROR, f"not_node only works for boolean",
                )
            

    def __eval_op(self, arith_ast):
        left_value_obj = self.__eval_expr(arith_ast.get("op1"))
        right_value_obj = self.__eval_expr(arith_ast.get("op2"))
        if left_value_obj.type() != right_value_obj.type():
            if (arith_ast.elem_type == "==" or arith_ast.elem_type == "!="):
                f = self.op_to_lambda["diff"][arith_ast.elem_type]
                return f(left_value_obj, right_value_obj)
            else:
                super().error(
                    ErrorType.TYPE_ERROR, f"Incompatible types for {arith_ast.elem_type} operation",
                )      
        if arith_ast.elem_type not in self.op_to_lambda[left_value_obj.type()]:
            super().error(
                ErrorType.TYPE_ERROR,
                f"Incompatible operator {arith_ast.elem_type} for type {left_value_obj.type()}",
            )
        f = self.op_to_lambda[left_value_obj.type()][arith_ast.elem_type]
        return f(left_value_obj, right_value_obj)

    def __setup_ops(self):
        self.op_to_lambda = {}
        # set up operations on integers
        self.op_to_lambda[Type.INT] = {
            "+": lambda x, y: Value(x.type(), x.value() + y.value()),
            "-": lambda x, y: Value(x.type(), x.value() - y.value()),
            "*": lambda x, y: Value(x.type(), x.value() * y.value()),
            "/": lambda x, y: Value(x.type(), int(x.value() // y.value())),
            
            "==": lambda x, y: Value(Type.BOOL, x.value() == y.value()),
            "!=": lambda x, y: Value(Type.BOOL, x.value() != y.value()),
            ">":  lambda x, y: Value(Type.BOOL, x.value() > y.value()),
            ">=": lambda x, y: Value(Type.BOOL, x.value() >= y.value()),
            "<":  lambda x, y: Value(Type.BOOL, x.value() < y.value()),
            "<=": lambda x, y: Value(Type.BOOL, x.value() <= y.value()),
        }
        
        #string 
        self.op_to_lambda[Type.STRING] = {
            "+":  lambda x, y: Value(x.type(), x.value() + y.value()),
            "==": lambda x, y: Value(Type.BOOL, x.value() == y.value()),
            "!=": lambda x, y: Value(Type.BOOL, x.value() != y.value()),
        }
        
        #bool 
        self.op_to_lambda[Type.BOOL] = {
            "==": lambda x, y: Value(Type.BOOL, x.value() == y.value()),
            "!=": lambda x, y: Value(Type.BOOL, x.value() != y.value()),
            "||": lambda x, y: Value(Type.BOOL, x.value() or y.value()),
            "&&": lambda x, y: Value(Type.BOOL, x.value() and y.value()),
        }
        
        self.op_to_lambda[Type.NIL] = {
            "==": lambda x, y: Value(Type.BOOL, x.value() == y.value()),
            "!=": lambda x, y: Value(Type.BOOL, x.value() != y.value()),
        }

        # mix for the different type == and !=
        # asked chatgpt for hint about the "diff"
        self.op_to_lambda["diff"] = { 
            "==": lambda x, y: Value(Type.BOOL, x.type() == y.type()),
            "!=": lambda x, y: Value(Type.BOOL, x.type() != y.type()),
        }
        
        # add other operators here later for int, string, bool, etc



# test = """
# func main() {
#     var a;
#     a = true;
#     var b;
#     b = !a;
#     print(!(!b));
# }
# """


# a = Interpreter(); 
# a.run(test)


