from __future__ import annotations

class ASTNode():
    def __init__(self):
        self.id = None
        self.repr_offset = 0

class ASTBaseNode(ASTNode):
    def __init__(self) -> None:
        super().__init__()
        self.children = []

    def __repr__(self):
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
        self.parent = None
        
    def __repr__(self):
        tab_offset = "    " * self.repr_offset
        return f"NumberNode[\n{tab_offset}    Value: {self.value}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class StringNode(ASTNode):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value
        self.parent = None

    def __repr__(self):
        tab_offset = "    " * self.repr_offset
        return f"StringNode[\n{tab_offset}    Value: {self.value}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"


class BoolNode(ASTNode):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value
        self.parent = None

    def __repr__(self):
        tab_offset = "    " * self.repr_offset
        return f"BoolNode[\n{tab_offset}    Value: {self.value}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class ArrayNode(ASTNode):
    def __init__(self, children: list[ASTNode]) -> None:
        super().__init__()
        self.children = children
        self.parent = None

    def __repr__(self):
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
        self.parent = None

    def __repr__(self):
        tab_offset = "    " * self.repr_offset
        return f"VarNode[\n{tab_offset}    Name: {self.name}\n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class ArrayVarNode(ASTNode):
    def __init__(self, name: str, idx: int):
        super().__init__()
        self.name = name
        self.idx = idx
        self.parent = None

class VarDecNode(ASTNode):
    def __init__(self, name: str, value: any, type: str) -> None:
        super().__init__()
        self.name = name
        self.value = value
        self.type = type
        self.parent = None

class BinOpNode(ASTNode):
    def __init__(self, left: NumberNode | StringNode | ArrayNode | VarNode, op: str, right: NumberNode | StringNode | ArrayNode | VarNode, type: str) -> None:
        super().__init__()
        self.left = left
        self.op = op
        self.right = right
        self.type = type
        self.parent = None

    def __repr__(self):
        self.left.repr_offset = self.repr_offset + 2
        self.right.repr_offset = self.repr_offset + 2
        tab_offset = "    " * self.repr_offset
        return f"BinOpNode[\n{tab_offset}    Left: \n{tab_offset}        {self.left}  \n{tab_offset}    Operator: '{self.op}'  \n{tab_offset}    Right: \n{tab_offset}        {self.right}    \n{tab_offset}    Id: {self.id}\n{tab_offset}]"

class FuncDefNode(ASTNode):
    def __init__(self, name: str, arg_names: list[str], children: list[ASTNode]) -> None:
        super().__init__()
        self.name = name
        self.arg_names = arg_names
        self.children = children
        self.parent = None

class FuncCallNode(ASTNode):
    def __init__(self, name: str, args: list[ASTNode]) -> None:
        super().__init__()
        self.name = name
        self.args = args


class ForLoopNode(ASTNode):
    def __init__(self, iter_var_name: str, iter: ArrayNode | VarNode | FuncCallNode) -> None:
        super().__init__()
        self.iter_var_name = iter_var_name
        self.iter = iter
        self.parent = None

class ExpressionNode(ASTNode):
    def __init__(self, left: BinOpNode | VarNode | ArrayVarNode | FuncCallNode | ExpressionNode, op: str, right: BinOpNode | VarNode | ArrayVarNode | FuncCallNode | ExpressionNode) -> None:
        super().__init__()
        self.left = left
        self.op = op
        self.right = right
        self.parent = None

class WhileLoopNode(ASTNode):
    def __init__(self, condition: ExpressionNode | FuncCallNode | VarNode | ArrayVarNode | BoolNode, children: list[ASTNode]) -> None:
        super().__init__()
        self.condition = condition
        self.children = children
        self.parent = None

class IfNode(ASTNode):
    def __init__(self, condition: ExpressionNode | FuncCallNode | VarNode | ArrayVarNode | BoolNode, children: list[ASTNode]) -> None:
        super().__init__()
        self.condition = condition
        self.children = children
        self.parent = None

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
    def __init__(self, base_node: ASTBaseNode) -> None:
        self.base_node = base_node
        self.base_node.id = 0
        self.cur_node = self.base_node
        self.next_free_id = 1

    def get_cur_node(self) -> ASTNode:
        return self.cur_node
    
    def set_cur_node_by_idx(self, idx: int) -> None:
        self.cur_node = self.base_node.children[idx]

    def traverse_cur_node(self, trvs_type: str) -> None:
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

    def append_node(self, node: ASTNode, side: str | None=None) -> None:
        node.parent = self.cur_node
        node.id = self.next_free_id
        self.next_free_id += 1

        if not side:
            self.cur_node.children.append(node)
        else:
            self.cur_node.__setattr__(side, node)
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
    test_ast = AST(ASTBaseNode())
    test_ast.append_node(ArrayNode([]))
    test_ast.traverse_cur_node("children")
    test_ast.append_node(ArrayNode([]))
    test_ast.traverse_cur_node("children")
    test_ast.append_node(NumberNode(5))
    test_ast.append_node(StringNode("Hehehehaw"))
    test_ast.append_node(BoolNode(True))
    test_ast.detraverse_node()
    test_ast.append_node(StringNode("Paul stinkt"))
    test_ast.detraverse_node()

    print(test_ast)

            
            

    

    
