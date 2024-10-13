from __future__ import annotations

class ASTNode():
    def __init__(self):
        self.parent = None
        self.id = None
        self.repr_offset = 0

class ASTBaseNode(ASTNode):
    def __init__(self) -> None:
        super().__init__()
        self.children = []

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        child_str = f""
        for child in self.children:
            child.repr_offset = self.repr_offset + 2
            child_str += f"\n{"    " * child.repr_offset}{child}"
            child_str = child_str
        
        return f"Module[\n{tab_offset}    Children[{tab_offset}    {child_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.children)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"
    
class ExpressionNode(ASTNode):
    def __init__(self, op: str) -> None:
        super().__init__()
        self.left = None
        self.op = op
        self.right = None

    def __repr__(self) -> str:
        self.left.repr_offset = self.repr_offset + 2
        self.right.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        return f"ExpressionNode[\n{tab_offset}    Left[ \n{tab_offset}        {self.left}\n{tab_offset}    ]\n{tab_offset}    Operator: '{self.op}'  \n{tab_offset}    Right:[\n{tab_offset}        {self.right}\n{tab_offset}    ]    \n{tab_offset}    Id: {self.id}\n{tab_offset}]"
    
class NumberNode(ASTNode):
    def __init__(self, value: int | float) -> None:
        super().__init__()
        self.value = value
        
    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        return f"NumberNode[\n{tab_offset}    Value: {self.value}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class StringNode(ASTNode):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        return f"StringNode[\n{tab_offset}    Value: {self.value}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class BoolNode(ASTNode):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        return f"BoolNode[\n{tab_offset}    Value: {self.value}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class ArrayNode(ASTNode):
    def __init__(self) -> None:
        super().__init__()
        self.children = []

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        child_str = f""
        for child in self.children:
            child.repr_offset = self.repr_offset + 2
            child_str += f"\n{"    " * child.repr_offset}{child}"
        
        return f"ArrayNode[\n{tab_offset}    Children[{tab_offset}        {child_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.children)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class VarNode(ASTNode):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        return f"VarNode[\n{tab_offset}    Name: {self.name}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class ArrayVarNode(ASTNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.content = None

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        return f"ArrayVarNode[\n{tab_offset}    Name: {self.name}\n{tab_offset}    Content: {self.content}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"
    
class SliceExpressionNode(ASTNode):
    def __init__(self) -> None:
        super().__init__()
        self.left = None
        self.right = None

class AssignNode(ASTNode):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.value = None
        self.type = None

    def set_type(self, type: str) -> None:
        self.type = type
        return None

    def __repr__(self) -> str:
        self.value.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        return f"VarDecNode[\n{tab_offset}    Name: {self.name}\n{tab_offset}    Value[\n{tab_offset}        {self.value}\n{tab_offset}    ]\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class BinOpNode(ASTNode):
    def __init__(self, op: str) -> None:
        super().__init__()
        self.left = None
        self.op = op
        self.right = None
        self.type = None

    def set_type(self, type: str) -> None:
        self.type = type
        return None

    def __repr__(self) -> str:
        self.left.repr_offset = self.repr_offset + 2
        self.right.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        return f"BinOpNode[\n{tab_offset}    Left[ \n{tab_offset}        {self.left}\n{tab_offset}    ]\n{tab_offset}    Operator: '{self.op}'  \n{tab_offset}    Right:[\n{tab_offset}        {self.right}\n{tab_offset}    ]    \n{tab_offset}    Id: {self.id}\n{tab_offset}]"
    
class UnOpNode(ASTNode):
    def __init__(self, op: str) -> None:
        super().__init__()
        self.op = op
        self.right = None
        self.type = None

    def set_type(self, type: str) -> None:
        self.type = type
        return None

    def __repr__(self) -> str:
        self.right.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        return f"UnOpNode[\n{tab_offset}    Right[\n{tab_offset}        {self.right}\n{tab_offset}    ] \n{tab_offset}    Operator: '{self.op}'\n{tab_offset}    Id: {self.id}\n{tab_offset}]"
    
class Condition(ASTNode):
    def __init__(self, op: str) -> None:
        super().__init__()
        self.left = None
        self.op = op
        self.right = None

class LogicalExpressionNode(ASTNode):
    def __init__(self, op: str) -> None:
        self.left = None
        self.op = op
        self.right = None

class FuncDefNode(ASTNode):
    def __init__(self, name: str, arg_names: list[str]) -> None:
        super().__init__()
        self.name = name
        self.arg_names = arg_names
        self.children = None

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        child_str = f""
        for child in self.children:
            child.repr_offset = self.repr_offset + 2
            child_str += f"\n{"    " * child.repr_offset}{child}"
        
        return f"FuncDefNode[\n{tab_offset}    Children[{tab_offset}        {child_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.children)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class FuncCallNode(ASTNode):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.args = None

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        arg_str = f""
        for arg in self.args:
            arg.repr_offset = self.repr_offset + 2
            arg_str += f"\n{"    " * arg.repr_offset}{arg}"
        
        return f"FuncCallNode[\n{tab_offset}    Name: {self.name}\n{tab_offset}    Args[{tab_offset}        {arg_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.args)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class ForLoopNode(ASTNode):
    def __init__(self, iter_var_name: str) -> None:
        super().__init__()
        self.iter_var_name = iter_var_name
        self.iter = None
        self.children = None

    def __repr__(self) -> str:
        self.iter.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        child_str = f""
        for child in self.children:
            child.repr_offset = self.repr_offset + 2
            child_str += f"\n{"    " * child.repr_offset}{child}"
        
        return f"ForLoopNode[\n{tab_offset}    Iter Var Name: {self.iter_var_name}\n{tab_offset}    Iter[\n{tab_offset}        {self.iter}\n{tab_offset}    Children[{tab_offset}        {child_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.children)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class WhileLoopNode(ASTNode):
    def __init__(self) -> None:
        super().__init__()
        self.condition = None
        self.children = None

    def __repr__(self) -> str:
        self.condition.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        child_str = f""
        for child in self.children:
            child.repr_offset = self.repr_offset + 2
            child_str += f"\n{"    " * child.repr_offset}{child}"
        
        return f"WhileLoopNode[\n{tab_offset}    Condition[\n{tab_offset}        {self.condition}\n{tab_offset}    Children[{tab_offset}        {child_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.children)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class IfNode(ASTNode):
    def __init__(self) -> None:
        super().__init__()
        self.condition = None
        self.children = None

    def __repr__(self) -> str:
        repr_res = WhileLoopNode.__repr__(self)
        repr_res = "IfNod" + repr_res[12:]
        return repr_res

class ElifNode(ASTNode):
    def __init__(self, prev_conditions: list[ASTNode]) -> None:
        super().__init__()
        self.condition = None
        self.prev_conditions = prev_conditions
        self.children = None

class ElseNode(ASTNode):
    def __init__(self, prev_conditions: list[IfNode | ElifNode]) -> None:
        super().__init__()
        self.condition = None
        self.prev_conditions = prev_conditions
        self.children = None

class AST():
    def __init__(self) -> None:
        self.base_node = ASTBaseNode()
        self.base_node.id = 0
        self.cur_node = self.base_node
        self.next_free_id = 1

    def get_cur_node(self) -> ASTNode:
        return self.cur_node
    
    def set_cur_node_by_idx(self, idx: int) -> None:
        self.cur_node = self.base_node.children[idx]
        return None

    def traverse_node(self, trvs_type: str = "children") -> None | int:
        parent_node = self.cur_node
        if not parent_node.__getattribute__(trvs_type):
            return -1
        
        self.cur_node = parent_node.__getattribute__(trvs_type)
        if isinstance(self.cur_node, list):
            self.cur_node = self.cur_node[0]
        self.cur_node.parent = parent_node
        return None

    def next_child_node(self) -> None:
        parent_node = self.cur_node.parent
        cur_node_idx = parent_node.children.index(self.cur_node)
        if cur_node_idx == len(parent_node.children)-1:
            return None
        self.cur_node = parent_node.children[cur_node_idx+1]
        self.cur_node.parent = parent_node
        return None

    def prev_child_node(self) -> None:
        parent_node = self.cur_node.parent
        cur_node_idx = parent_node.children.index(self.cur_node)
        if cur_node_idx == 0:
            return None
        self.cur_node = self.parent_node.children[cur_node_idx-1]
        if not self.cur_node.parent:
            self.cur_node.parent = parent_node
        return None

    def detraverse_node(self) -> None:
        self.cur_node = self.cur_node.parent
        return None

    def get_node_by_id(self, id: int) -> ASTNode:
        old_cur_node = self.cur_node
        for i in range(len(self.base_node.children)):
            self.set_cur_node_by_idx(i)
            if self.cur_node.id == id:
                return self.get_node_by_id_cleanup(old_cur_node)
            cur_node_atts = self.cur_node.__dict__
            if "children" in cur_node_atts:
                res = self.get_node_by_id_children_handler(id)
                if res:
                    return self.get_node_by_id_cleanup(old_cur_node, res)
            elif "left" in cur_node_atts:
                left_res = self.get_node_by_id_binop_handler(id, "left")
                if left_res:
                    return self.get_node_by_id_cleanup(old_cur_node, left_res)
                right_res = self.get_node_by_id_binop_handler(id, "right")
                if right_res:   
                    return self.get_node_by_id_cleanup(old_cur_node, right_res)
        self.cur_node = old_cur_node
        return None
                
    def get_node_by_id_cleanup(self, old_cur_node: ASTNode, return_node: ASTNode=None) -> ASTNode:
        if not return_node:
            return_node = self.cur_node
        self.cur_node = old_cur_node
        return return_node
    
    def get_node_by_id_traverse_search(self, id: int) -> ASTNode | None:
        if self.cur_node.id == id:
                return self.cur_node
        cur_node_atts = self.cur_node.__dict__
        if "children" in cur_node_atts:
            res = self.get_node_by_id_children_handler(id)
            if res:
                return res
        elif "left" in cur_node_atts:
            left_res = self.get_node_by_id_binop_handler(id, "left")
            if left_res:
                return left_res
            right_res = self.get_node_by_id_binop_handler(id, "right")
            if right_res:   
                return right_res
        
    def get_node_by_id_children_handler(self, id: int) -> ASTNode | None:
        parent_node = self.cur_node
        self.traverse_cur_node("children")
        for i in range(len(parent_node.children)):
            res = self.get_node_by_id_traverse_search(id)
            if res:
                return res
            self.next_child_node()
        self.cur_node = parent_node
        return None
    
    def get_node_by_id_binop_handler(self, id: int, side: str) -> ASTNode | None:
        parent_node = self.cur_node
        self.traverse_cur_node(side)
        res = self.get_node_by_id_traverse_search(id)
        if res:
            return res
        self.cur_node = parent_node
        return None

    def append_node(self, node: ASTNode, type: str = "children") -> None:
        node.parent = self.cur_node
        node.id = self.next_free_id
        self.next_free_id += 1

        if type == "children":
            if not self.cur_node.children:
                self.cur_node.children = []
            self.cur_node.__setattr__(type, self.cur_node.children + [node])
            return None
        
        if type == "args":
            if not self.cur_node.args:
                self.cur_node.args = []
            self.cur_node.__setattr__("args", self.cur_node.args + [node])
            return None

        self.cur_node.__setattr__(type, node)
        return None
    
    def insert_child_node_by_idx(self, idx: int, node: ASTNode) -> None:
        node.parent = self.cur_node
        node.id = self.next_free_id
        self.next_free_id += 1
        self.cur_node.children.insert(idx, node)
        self.sort_ids()
        return None
    
    def sort_ids(self):
        pass

    def __repr__(self):
        return self.base_node.__repr__()

if __name__ == "__main__":
    test_ast = AST()
    test_ast.append_node(BinOpNode(None, "+", None, "int"))
    test_ast.traverse_node()
    test_ast.append_node(BinOpNode(None, "*", None, "int"), "left")
    test_ast.append_node(NumberNode(10), "right")
    test_ast.traverse_node("left")
    test_ast.append_node(NumberNode(5), "left")
    test_ast.append_node(NumberNode(5), "right")
    test_ast.detraverse_node()
    test_ast.detraverse_node()
    
    print(test_ast)