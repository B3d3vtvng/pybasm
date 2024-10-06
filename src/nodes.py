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
        
        return f"main[\n{tab_offset}    Children[{tab_offset}    {child_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.children)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"


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
    def __init__(self, children: list[ASTNode]) -> None:
        super().__init__()
        self.children = children

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
    def __init__(self, name: str, idx: int):
        super().__init__()
        self.name = name
        self.idx = idx

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        return f"ArrayVarNode[\n{tab_offset}    Name: {self.name}\n{tab_offset}    Idx: {self.idx}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class VarDecNode(ASTNode):
    def __init__(self, name: str, value: ASTNode, type: str) -> None:
        super().__init__()
        self.name = name
        self.value = value
        self.type = type

    def __repr__(self) -> str:
        self.value.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        return f"VarDecNode[\n{tab_offset}    Name: {self.name}\n{tab_offset}    Value[\n{tab_offset}        {self.value}\n{tab_offset}    ]\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class BinOpNode(ASTNode):
    def __init__(self, left: NumberNode | StringNode | ArrayNode | VarNode, op: str, right: NumberNode | StringNode | ArrayNode | VarNode, type: str) -> None:
        super().__init__()
        self.left = left
        self.op = op
        self.right = right
        self.type = type

    def __repr__(self) -> str:
        self.left.repr_offset = self.repr_offset + 2
        self.right.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        return f"BinOpNode[\n{tab_offset}    Left[ \n{tab_offset}        {self.left}\n{tab_offset}    ]\n{tab_offset}    Operator: '{self.op}'  \n{tab_offset}    Right:[\n{tab_offset}        {self.right}\n{tab_offset}    ]    \n{tab_offset}    Id: {self.id}\n{tab_offset}]"
    
class UnOpNode(ASTNode):
    def __init__(self, op: str, right: ASTNode, type: str) -> None:
        super().__init__()
        self.op = op
        self.right = right
        self.type = type

    def __repr__(self) -> str:
        self.right.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        return f"UnOpNode[\n{tab_offset}    Right[\n{tab_offset}        {self.right}\n{tab_offset}    ] \n{tab_offset}    Operator: '{self.op}'\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class FuncDefNode(ASTNode):
    def __init__(self, name: str, arg_names: list[str], children: list[ASTNode]) -> None:
        super().__init__()
        self.name = name
        self.arg_names = arg_names
        self.children = children

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        child_str = f""
        for child in self.children:
            child.repr_offset = self.repr_offset + 2
            child_str += f"\n{"    " * child.repr_offset}{child}"
        
        return f"FuncDefNode[\n{tab_offset}    Children[{tab_offset}        {child_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.children)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class FuncCallNode(ASTNode):
    def __init__(self, name: str, args: list[ASTNode]) -> None:
        super().__init__()
        self.name = name
        self.args = args

    def __repr__(self) -> str:
        tab_offset = "    " * self.repr_offset
        arg_str = f""
        for arg in self.args:
            arg.repr_offset = self.repr_offset + 2
            arg_str += f"\n{"    " * arg.repr_offset}{arg}"
        
        return f"FuncCallNode[\n{tab_offset}    Name: {self.name}\n{tab_offset}    Args[{tab_offset}        {arg_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.args)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class ForLoopNode(ASTNode):
    def __init__(self, iter_var_name: str, iter: ArrayNode | VarNode | FuncCallNode, children: list[ASTNode]) -> None:
        super().__init__()
        self.iter_var_name = iter_var_name
        self.iter = iter
        self.children = children

    def __repr__(self) -> str:
        self.iter.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        child_str = f""
        for child in self.children:
            child.repr_offset = self.repr_offset + 2
            child_str += f"\n{"    " * child.repr_offset}{child}"
        
        return f"ForLoopNode[\n{tab_offset}    Iter Var Name: {self.iter_var_name}\n{tab_offset}    Iter[\n{tab_offset}        {self.iter}\n{tab_offset}    Children[{tab_offset}        {child_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.children)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class ExpressionNode(ASTNode):
    def __init__(self, left: BinOpNode | VarNode | ArrayVarNode | FuncCallNode | ExpressionNode, op: str, right: BinOpNode | VarNode | ArrayVarNode | FuncCallNode | ExpressionNode) -> None:
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        self.left.repr_offset = self.repr_offset + 2
        self.right.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        return f"ExpressionNode[\n{tab_offset}    Left[ \n{tab_offset}        {self.left}\n{tab_offset}    ]\n{tab_offset}    Operator: '{self.op}'  \n{tab_offset}    Right:[\n{tab_offset}        {self.right}\n{tab_offset}    ]    \n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class WhileLoopNode(ASTNode):
    def __init__(self, condition: ExpressionNode | FuncCallNode | VarNode | ArrayVarNode | BoolNode, children: list[ASTNode]) -> None:
        super().__init__()
        self.condition = condition
        self.children = children

    def __repr__(self) -> str:
        self.condition.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        child_str = f""
        for child in self.children:
            child.repr_offset = self.repr_offset + 2
            child_str += f"\n{"    " * child.repr_offset}{child}"
        
        return f"WhileLoopNode[\n{tab_offset}    Condition[\n{tab_offset}        {self.condition}\n{tab_offset}    Children[{tab_offset}        {child_str}\n{tab_offset}    ]\n{tab_offset}    Len: {len(self.children)}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class IfNode(ASTNode):
    def __init__(self, condition: ExpressionNode, children: list[ASTNode]) -> None:
        super().__init__()
        self.condition = condition
        self.children = children

    def __repr__(self) -> str:
        repr_res = WhileLoopNode.__repr__(self)
        repr_res = "IfNod" + repr_res[12:]
        return repr_res

class ElifNode(ASTNode):
    def __init__(self, condition: ExpressionNode | FuncCallNode | VarNode | ArrayVarNode | BoolNode, prev_conditions: list[IfNode | ElifNode], children: list[ASTNode]) -> None:
        super().__init__()
        self.condition = condition
        self.prev_conditions = prev_conditions
        self.children = children

class ElseNode(ASTNode):
    def __init__(self, condition: ExpressionNode | FuncCallNode | VarNode | ArrayVarNode | BoolNode, prev_conditions: list[IfNode | ElifNode], children: list[ASTNode]) -> None:
        super().__init__()
        self.condition = condition
        self.prev_conditions = prev_conditions
        self.children = children

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

    def traverse_node(self, trvs_type: str) -> None:
        parent_node = self.cur_node
        if not parent_node.__getattribute__(trvs_type):
            return -1
        
        self.cur_node = parent_node.__getattribute__(trvs_type)
        if isinstance(self.cur_node, list):
            self.cur_node = self.cur_node[0]
        self.cur_node.parent = parent_node

    def next_child_node(self) -> None:
        parent_node = self.cur_node.parent
        self.cur_node = [node for node in parent_node.children if node.id == self.cur_node.id +1][0]
        self.cur_node.parent = parent_node

    def detraverse_node(self) -> None:
        self.cur_node = self.cur_node.parent

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
    test_ast.append_node(IfNode(None, None))
    test_ast.traverse_node("children")
    test_ast.append_node(ExpressionNode(None, '==', None), "condition")
    test_ast.traverse_node("condition")
    test_ast.append_node(VarNode("x"), "left")
    test_ast.append_node(NumberNode(10), "right")
    test_ast.detraverse_node()
    test_ast.append_node(FuncCallNode("print", []))
    test_ast.traverse_node("children")
    test_ast.append_node(StringNode("Hello World"), "args")
    test_ast.detraverse_node()
    test_ast.detraverse_node()
    

    print(test_ast)

            
            

    

    
