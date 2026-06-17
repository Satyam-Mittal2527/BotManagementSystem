from .nodes.condition_node import ConditionNode
from .nodes.loop_node import LoopNode
from .nodes.script_node import ScriptNode
from .nodes.end_node import EndNode

NODE_MAP = {
    "start": ScriptNode,

    "process": ScriptNode,

    "decision": ConditionNode,

    "script": ScriptNode,

    "condition": ConditionNode,

    "loop": LoopNode,

    "end": EndNode

}