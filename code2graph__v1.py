"""工    作   日   志
1、新增了词袋和数据流生成
2、数据流存在问题    [2,2,8]无[8,2,10],而是[2,2,10]
"""
import ast
import astpretty
import os
from itertools import islice
import copy


def While_Node(Node, list, body_string, no_list):
    list.append(body_string + "While")
    no_list.append(Node.lineno)
    list.append(body_string + "While.cond" + str(type(Node.test))[11:-2])
    no_list.append(Node.lineno)
    body_string = body_string + "While.body."
    for n in islice(ast.walk(Node), 1, None):
        # astpretty.pprint(n)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if type(n) == ast.For:
            For_Node(n, list, body_string, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string + "Assign." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string + "Expr." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Return):
            list.append(body_string + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if len(Node.orelse):
            if n == Node.orelse[len(Node.orelse) - 1]:
                break
        else:
            if n == Node.body[len(Node.body) - 1]:
                break


def For_Node(Node, list, body_string, no_list):
    list.append(body_string + "For")
    no_list.append(Node.lineno)
    list.append(body_string + "For.cond" + str(type(Node.iter))[11:-2])
    no_list.append(Node.lineno)
    body_string = body_string + "For.body."
    for n in islice(ast.walk(Node), 1, None):
        # astpretty.pprint(n)
        if type(n) == ast.For:
            For_Node(n, list, body_string, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string, no_list)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string + "Assign." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string + "Expr." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Return):
            list.append(body_string + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if len(Node.orelse):
            if n == Node.orelse[len(Node.orelse) - 1]:
                break
        else:
            if n == Node.body[len(Node.body) - 1]:
                break
        """astpretty.pprint(n)
        print(type(n))"""


def Attribute_Node(Node):
    """if isinstance(Node.value, ast.Name):
        string = Node.value.id
    elif isinstance(Node.value, ast.Attribute):
        string = Attribute_Node(Node.value)
    elif isinstance(Node.value, ast.Call):
        string = Call_node(Node.value)
    else:
        string = str(type(Node.value))[13:-2]"""
    string = Node.attr
    return string


def Call_node(Node):
    string = 'Call.'
    if isinstance(Node.func, ast.Name):
        string += Node.func.id
    elif isinstance(Node.func, ast.Attribute):
        string += Attribute_Node(Node.func)
    else:
        string = 'UNN'
    return string
    # print(string)


def If_Node(Node, list, body_string, no_list):
    list.append(body_string + "If")
    no_list.append(Node.lineno)
    list.append(body_string + "If.cond" + str(type(Node.test))[11:-2])
    no_list.append(Node.lineno)
    body_string = body_string + "If.body."
    for n in islice(ast.walk(Node), 1, None):
        # astpretty.pprint(n)
        if type(n) == ast.For:
            For_Node(n, list, body_string, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string, no_list)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string + "Assign" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                # astpretty.pprint(n.value)
                call_string = Call_node(n.value)
                list.append(body_string + "Expr" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Return):
            list.append(body_string + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if len(Node.orelse):
            if n == Node.orelse[len(Node.orelse) - 1]:
                break
        else:
            if n == Node.body[len(Node.body) - 1]:
                break


def Try_Node(Node, list, body_string, no_list):
    list.append(body_string + 'Try')
    no_list.append(Node.lineno)
    # list.append(body_string + "Try.cond" + str(type(Node.test))[12:-2])
    body_string1 = body_string + "Try.body."
    for n in islice(ast.walk(Node), 1, None):
        # astpretty.pprint(n)
        if type(n) == ast.For:
            For_Node(n, list, body_string1, no_list)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string1, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string1 + "Assign" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string1 + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                # astpretty.pprint(n.value)
                call_string = Call_node(n.value)
                list.append(body_string1 + "Expr" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string1 + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Return):
            list.append(body_string1 + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if n == Node.body[len(Node.body) - 1]:
            break  # Def单层遍历的截止信号
    body_string2 = body_string + "Try.handlers."
    for node in Node.handlers:
        body_string2 = body_string2[:-1] + str(Node.handlers.index(node) + 1) + '.'
        for n in islice(ast.walk(node), 1, None):
            if type(n) == ast.For:
                For_Node(n, list, body_string2, no_list)
            if isinstance(n, ast.While):
                While_Node(n, list, body_string, no_list)
            if isinstance(n, ast.With):
                With_Node(n, list, body_string, no_list)
            if type(n) == ast.If:
                If_Node(n, list, body_string2, no_list)
            if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
                if isinstance(n.value, ast.Call):
                    call_string = Call_node(n.value)
                    list.append(body_string2 + "Assign" + "." + call_string)
                    no_list.append(n.lineno)
                else:
                    list.append(body_string2 + "Assign" + str(type(n.value))[11:-2])
                    no_list.append(n.lineno)
            if isinstance(n, ast.Expr):
                if isinstance(n.value, ast.Call):
                    # astpretty.pprint(n.value)
                    call_string = Call_node(n.value)
                    list.append(body_string2 + "Expr" + "." + call_string)
                    no_list.append(n.lineno)
                else:
                    list.append(body_string2 + "Expr" + str(type(n.value))[11:-2])
                    no_list.append(n.lineno)
            if isinstance(n, ast.Return):
                list.append(body_string2 + "Return" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
            if isinstance(n, ast.Raise):
                if isinstance(n.exc, ast.Call):
                    string = Call_node(n.exc)
                    list.append(body_string + "Raise.Call." + string)
                    no_list.append(n.lineno)
                else:
                    list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                    no_list.append(n.lineno)
            if n == node.body[len(node.body) - 1]:
                break  # Def单层遍历的截止信号
    body_string3 = body_string + "Try.else."
    for n in islice(ast.walk(Node), 1 + len(Node.body) + len(Node.handlers), None):
        # astpretty.pprint(n)
        if type(n) == ast.For:
            For_Node(n, list, body_string3, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string3, no_list)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string3 + "Assign" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string3 + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                # astpretty.pprint(n.value)
                call_string = Call_node(n.value)
                list.append(body_string3 + "Expr" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string3 + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Return):
            list.append(body_string3 + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if len(Node.orelse):
            if n == Node.orelse[len(Node.orelse) - 1]:
                break  # Def单层遍历的截止信号
    body_string4 = body_string + "Try.final."
    for n in islice(ast.walk(Node), 1 + len(Node.body) + len(Node.handlers) + len(Node.orelse), None):
        # astpretty.pprint(n)
        if type(n) == ast.For:
            For_Node(n, list, body_string4, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string4, no_list)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string4 + "Assign" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string4 + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                # astpretty.pprint(n.value)
                call_string = Call_node(n.value)
                list.append(body_string4 + "Expr" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string4 + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Return):
            list.append(body_string4 + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if len(Node.finalbody):
            if n == Node.finalbody[len(Node.finalbody) - 1]:
                break  # Def单层遍历的截止信号


def With_Node(Node, list, body_string, no_list):
    list.append(body_string + "With")
    no_list.append(Node.lineno)
    body_string = body_string + "With.body."
    for n in islice(ast.walk(Node), 1, None):
        # astpretty.pprint(n)
        if type(n) == ast.For:
            For_Node(n, list, body_string, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string, no_list)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string + "Assign" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                # astpretty.pprint(n.value)
                call_string = Call_node(n.value)
                list.append(body_string + "Expr" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Return):
            list.append(body_string + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if n == Node.body[len(Node.body) - 1]:
            break  # Def单层遍历的截止信号


def Def_Node(Node, list, def_no, no_list):
    list.append("Def" + str(def_no))
    no_list.append(Node.lineno)
    body_string = 'Def' + str(def_no) + '.'
    for n in islice(ast.walk(Node), 1, None):
        # astpretty.pprint(n)
        if isinstance(n, ast.FunctionDef):
            def_no += 1
            Def_Node(n, list, def_no, no_list)
        if type(n) == ast.For:
            For_Node(n, list, body_string, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string, no_list)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                string = Call_node(n.value)
                list.append(body_string + "Assign" + "." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string + "Expr" + '.' + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Return):
            # astpretty.pprint(n)
            list.append(body_string + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if n == Node.body[len(Node.body) - 1]:
            break  # Def单层遍历的截止信号


def Class_Node(Node, list, Class_no, no_list):
    def_no = 0
    list.append("Class" + str(Class_no))
    no_list.append(Node.lineno)
    body_string = "Main."  # !!!!!有点问题
    for n in islice(ast.walk(Node), 1, None):
        # astpretty.pprint(n)
        if type(n) == ast.For:
            For_Node(n, list, body_string, no_list)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string + "Assign" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                # astpretty.pprint(n.value)
                call_string = Call_node(n.value)
                list.append(body_string + "Expr" + "." + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Return):
            list.append(body_string + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.FunctionDef):
            def_no += 1
            Def_Node(n, list, def_no, no_list)
            # astpretty.pprint(n)
        if len(Node.decorator_list):
            if n == Node.decorator_list[len(Node.decorator_list) - 1]:
                break
        else:
            if n == Node.body[len(Node.body) - 1]:
                break


def Main_Node(Node, list, no_list):
    list.append("Main")
    no_list.append(Node.lineno)
    body_string = ''
    for n in islice(ast.walk(Node), 1, None):
        # astpretty.pprint(n)
        if type(n) == ast.For:
            For_Node(n, list, body_string, no_list)
        if type(n) == ast.If:
            If_Node(n, list, body_string, no_list)
        if isinstance(n, ast.While):
            While_Node(n, list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, list, body_string, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                string = Call_node(n.value)
                list.append(body_string + "Assign" + "." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                call_string = Call_node(n.value)
                list.append(body_string + "Expr" + '.' + call_string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Return):
            # astpretty.pprint(n)
            list.append(body_string + "Return" + str(type(n.value))[11:-2])
            no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if len(Node.orelse):
            if n == Node.orelse[len(Node.orelse) - 1]:
                break
        else:
            if n == Node.body[len(Node.body) - 1]:
                break


def get_nodeList(Node, node_list, no_list):
    # Node:根节点    node_List: 顺序节点列表       length:顺序存储控制单元长度的列表
    def_no = 0
    Class_no = 0
    for n in ast.walk(Node):
        # astpretty.pprint(n)
        # print(type(node))
        body_string = ''
        if isinstance(n, ast.ClassDef):
            Class_no += 1
            Class_Node(n, node_list, Class_no, no_list)
        if isinstance(n, ast.Assign) or isinstance(n, ast.AugAssign) or isinstance(n, ast.AnnAssign):
            if isinstance(n.value, ast.Call):
                string = Call_node(n.value)
                node_list.append("Assign" + "." + string)
                no_list.append(n.lineno)
            else:
                node_list.append("Assign" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Expr):
            if isinstance(n.value, ast.Call):
                string = Call_node(n.value)
                node_list.append("Expr" + "." + string)
                no_list.append(n.lineno)
            else:
                node_list.append("Expr" + str(type(n.value))[11:-2])
                no_list.append(n.lineno)
        if isinstance(n, ast.Raise):
            if isinstance(n.exc, ast.Call):
                string = Call_node(n.exc)
                node_list.append(body_string + "Raise.Call." + string)
                no_list.append(n.lineno)
            else:
                node_list.append(body_string + "Raise" + str(type(n.exc))[11:-2])
                no_list.append(n.lineno)
        if type(n) == ast.For:
            For_Node(n, node_list, body_string, no_list)
        if isinstance(n, ast.While):
            While_Node(n, node_list, body_string, no_list)
        if isinstance(n, ast.Try):
            Try_Node(n, node_list, body_string, no_list)
        if isinstance(n, ast.With):
            With_Node(n, node_list, body_string, no_list)
        if type(n) == ast.If:
            if isinstance(n.test, ast.Compare):
                if isinstance(n.test.comparators[0], ast.Constant):
                    if n.test.comparators[0].value == '__main__':
                        Main_Node(n, node_list, no_list)
            else:
                If_Node(n, node_list, body_string, no_list)
        if isinstance(n, ast.FunctionDef):
            def_no += 1
            Def_Node(n, node_list, def_no, no_list)
            # astpretty.pprint(n)
            # get_nodelist(n)
        if len(Node.body):
            if n == Node.body[len(Node.body) - 1]:
                break


def get_edge(node_dict, edge_list):
    """"
    根据控制流，给图加上边
    """
    x = 0
    large = []
    for n in node_dict:
        if n < len(node_dict):
            edge_list.append([n, 1, n + 1])
    for n in node_dict:
        if node_dict[n][:4] == 'Class' or node_dict[n] == 'Main':
            large.append(n)
        if 'Def' in node_dict[n] and '.' not in node_dict[n]:
            x = n
            for i in range(n, len(node_dict) + 1):
                if node_dict[x] not in node_dict[i]:
                    y = i
                    if [y - 1, 1, y] in edge_list:
                        edge_list.remove([y - 1, 1, y])
                    edge_list.append([x, 1, y])
                    break
        if node_dict[n][-3:] == 'For':
            x = n
            for i in range(n + 1, len(node_dict) + 1):
                if node_dict[i][0:len(node_dict[x]) + 1] != node_dict[x] + '.':
                    y = i  # 控制单元出口
                    # print(node_dict[x])
                    # print(node_dict[y])
                    if node_dict[y][0:len(node_dict[x]) - 3] == node_dict[x][0:len(node_dict[x]) - 3]:
                        if [y - 1, 1, y] in edge_list:
                            edge_list.remove([y - 1, 1, y])
                        edge_list.append([x, 1, y])
                    break
        if node_dict[n][-5:] == 'While':
            x = n
            for i in range(n + 1, len(node_dict) + 1):
                if node_dict[i][0:len(node_dict[x]) + 1] != node_dict[x] + '.':
                    y = i
                    # print(node_dict[x])
                    # print(node_dict[y])
                    if node_dict[y][0:len(node_dict[x]) - 5] == node_dict[x][0:len(node_dict[x]) - 5]:
                        if [y - 1, 1, y] in edge_list:
                            edge_list.remove([y - 1, 1, y])
                        edge_list.append([x, 1, y])
                    break
        if node_dict[n][-2:] == 'If':
            x = n
            for i in range(n + 1, len(node_dict) + 1):
                if node_dict[i][0:len(node_dict[x]) + 1] != node_dict[x] + '.':
                    y = i
                    # print(node_dict[y])
                    if node_dict[y][0:len(node_dict[x]) - 2] == node_dict[x][0:len(node_dict[x]) - 2]:
                        if [y - 1, 1, y] in edge_list:
                            edge_list.remove([y - 1, 1, y])
                        edge_list.append([x, 1, y])
                    break
        if node_dict[n] == 'With':
            x = n
            for i in range(n + 1, len(node_dict) + 1):
                if node_dict[i][0:len(node_dict[x]) + 1] != node_dict[x] + '.':
                    y = i
                    # print(node_dict[y])
                    if node_dict[y][0:len(node_dict[x]) - 2] == node_dict[x][0:len(node_dict[x]) - 2]:
                        if [y - 1, 1, y] in edge_list:
                            edge_list.remove([y - 1, 1, y])
                        edge_list.append([x, 1, y])
                    break
        if node_dict[n] == 'Try':
            x = n
            for i in range(n + 1, len(node_dict) + 1):
                if node_dict[i][0:len(node_dict[x]) + 1] != node_dict[x] + '.':
                    y = i
                    # print(node_dict[y])
                    if node_dict[y][0:len(node_dict[x]) - 2] == node_dict[x][0:len(node_dict[x]) - 2]:
                        if [y - 1, 1, y] in edge_list:
                            edge_list.remove([y - 1, 1, y])
                        edge_list.append([x, 1, y])
                    break
    if len(large) > 1:
        for n in range(1, len(large)):
            if [large[n] - 1, 1, large[n]] in edge_list:
                edge_list.remove([large[n] - 1, 1, large[n]])
            edge_list.append([large[n - 1], 1, large[n]])


def get_token(root_node):
    temp = []
    for n in ast.walk(root_node):
        for child in ast.iter_child_nodes(n):
            child.parent = n
    for n in ast.walk(root_node):
        if isinstance(n, ast.FunctionDef) or isinstance(n, ast.ClassDef):
            temp.append(n.name)
        for child in ast.iter_child_nodes(n):
            if isinstance(child, ast.Name):
                if isinstance(child.parent, ast.Call):
                    continue
                else:
                    temp.append(child.id)
    list1 = []
    for n in temp:
        if n not in list1:
            list1.append(n)
    return list1


def make_Node_txt(path, content):
    if os.path.exists(path):
        if os.path.isdir(path):
            f = open('graph/Graph_Node.txt', 'a+')
            f.write(content)
            f.write('\n')
            f.seek(0)
            # read = f.readline()
            f.close()
            # print(read)
        else:
            print('please input the dir name')
    else:
        print('the path is not exists')


def make_Edge_txt(path, content):
    if os.path.exists(path):
        if os.path.isdir(path):
            f = open('graph/Graph_Edge.txt', 'a+')
            f.write(content)
            f.write('\n')
            f.seek(0)
            # read = f.readline()
            f.close()
            # print(read)
        else:
            print('please input the dir name')
    else:
        print('the path is not exists')


def predict_txt(path, content):
    if os.path.exists(path):
        if os.path.isdir(path):
            f = open('graph/predict.txt', 'a+')
            f.write(content)
            f.write('\n')
            f.seek(0)
            # read = f.readline()
            f.close()
            # print(read)
        else:
            print('please input the dir name')
    else:
        print('the path is not exists')


def token_txt(path, content):
    if os.path.exists(path):
        if os.path.isdir(path):
            f = open('graph/token.txt', 'a+')
            f.write(content)
            f.write('\n')
            f.seek(0)
            # read = f.readline()
            f.close()
            # print(read)
        else:
            print('please input the dir name')
    else:
        print('the path is not exists')


def dataFlow(root_node, list1):
    # astpretty.pprint(root_node)
    length = 0
    var = []
    for n in ast.walk(root_node):
        for child in ast.iter_child_nodes(n):
            child.parent = n
        if isinstance(n, ast.Name):
            if n.lineno > length:
                length = n.lineno
    # print("该代码的节点列表长度为：", length)
    for no in range(length):
        for n in ast.walk(root_node):
            if isinstance(n, ast.Name) and n.lineno == no + 1 and n.id in id_list:
                temp_list = [n.id, str(n.ctx)[5:10].strip(), n.lineno]
                var.append(temp_list)
            if isinstance(n, ast.FunctionDef):  # 加上自定义函数传入的变量（非Name，无法从上面方法找出）
                for a in n.args.args:
                    if a.lineno == no + 1 and a.arg in list1:
                        temp_list = [a.arg, "Store", a.lineno]
                        var.append(temp_list)
    start_list = []
    end_list = []
    dataflow = []
    for point in var:
        if point[1] == 'Store':
            start_list.append([point[0], point[2]])
        else:
            end_list.append([point[0], point[2]])
    # print(start_list, len(start_list))
    # print(end_list, len(end_list))
    for list1 in end_list:
        for list2 in start_list:
            if list2[0] == list1[0] and list2[1] < list1[1]:
                list3 = [list2[1], list1[1]]
                if list3 not in dataflow:
                    dataflow.append(list3)
    return dataflow


def add_dataflow(list1, list2, list3):
    """
    :param list1: dataflow_list
    :param list2: no_list
    :param list3: graph_edge
    :return:
    """
    for n in list1:
        a, b = n[0], n[1]
        start = list2.index(a)
        if list2[start + 1] == a:
            start = start + 1
        end = list2.index(b)
        if end < len(list2) - 1:
            if list2[end + 1] == b:
                end = end + 1
        start += 1
        end += 1
        flag = 0
        for edge in list3:
            if edge[0] == start and edge[2] == end:
                edge[1] = 3
                flag = 1
                break
        if flag == 0:
            list3.append([start, 2, end])
    return list3


def get_trainData(dict1, list1, no):
    """
    :param dict1: 图的节点字典
    :param list1: 图的边列表
    :param no: 待被挖洞的节点编号
    :return: 新的节点字典、新的边列表、predict——word
    """
    word = dict1[no]
    dict1[no] = 'hole'
    for edge in list1:
        if edge[0] == no or edge[2] == no:
            edge[1] = 4
    return dict1, list1, word


code_path = './error'
path2 = './error_graph'
files = os.listdir(code_path)
# print(files)
file_no = 1
for file in files:
    print(file_no)
    file_no += 1
    position = code_path + '/' + file
    # print(position)
    print(file)
    with open(position, 'r', encoding='utf-8') as f:
        content = f.read()
    # print(content)
    root_node = ast.parse(content)
    astpretty.pprint(root_node)
    id_list = get_token(root_node)
    dataflow_list = dataFlow(root_node, id_list)
    print(dataflow_list)
    Node_list = []
    no_list = []
    get_nodeList(root_node, Node_list, no_list)
    # print(file)
    print(len(no_list), no_list)
    print(len(Node_list), Node_list)
    no = list(range(len(Node_list)))
    no.remove(0)
    no.append(len(Node_list))
    graph_node = dict(zip(no, Node_list))
    # print(graph_node)
    graph_edge = []
    get_edge(graph_node, graph_edge)
    # print(graph_edge)
    graph_edge = add_dataflow(dataflow_list, no_list, graph_edge)
    # print(graph_node)
    print(dataflow_list)
    print(no_list)
    print(graph_edge)
    # 剔除重复的for、if的body嵌套
    for n in range(len(graph_node)):
        if 'Def' in graph_node[n + 1] and '.' in graph_node[n + 1]:
            graph_node[n + 1] = graph_node[n + 1][5:]
            graph_node[n + 1] = graph_node[n + 1].lstrip(".")
        if graph_node[n + 1][0:9] == 'With.body':
            graph_node[n + 1] = graph_node[n + 1][10:]
        """if 'Try' in graph_node[n + 1] and '.' in graph_node[n + 1]:
            graph_node[n + 1] = graph_node[n + 1][10:]"""
        while graph_node[n + 1].count("If") + graph_node[n + 1].count("For") + graph_node[n + 1].count("While") + \
                graph_node[n + 1].count("With") > 1 and ".body." in graph_node[n + 1] and "Main" not in graph_node[
            n + 1] and "Try" not in graph_node[n + 1]:
            if graph_node[n + 1][0:7] == "If.body":
                # print(graph_node[n + 1])
                graph_node[n + 1] = graph_node[n + 1][8:]
            if graph_node[n + 1][0:8] == "For.body":
                # print(graph_node[n + 1])
                graph_node[n + 1] = graph_node[n + 1][9:]
            if graph_node[n + 1][0:10] == "While.body":
                # print(graph_node[n + 1])
                graph_node[n + 1] = graph_node[n + 1][11:]
            if graph_node[n + 1][0:9] == "With.body":
                # print(graph_node[n + 1])
                graph_node[n + 1] = graph_node[n + 1][10:]
    with open('./graph/node.txt', 'a+') as f:
        f.write(str(graph_node))
        print(graph_node)
        f.write('\n')
    for i in graph_node:
        dict2 = copy.deepcopy(graph_node)
        list2 = copy.deepcopy(graph_edge)
        node1, edge1, predict = get_trainData(dict2, list2, i)
        make_Node_txt(path2, str(node1))
        make_Edge_txt(path2, str(edge1))
        predict_txt(path2, str(predict))
        token_txt(path2, str(id_list))

    """
    try:
        with open(position, 'r', encoding='utf-8') as f:
            content = f.read()
        # print(content)
        root_node = ast.parse(content)
        # astpretty.pprint(root_node)
        id_list = get_token(root_node)
        dataflow_list = dataFlow(root_node, id_list)
        print(dataflow_list)
        Node_list = []
        get_nodeList(root_node, Node_list)
        print(Node_list)
    except:
        os.remove(position)
        """
