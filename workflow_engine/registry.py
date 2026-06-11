from workflow_engine.nodes.variable_node import VariableNode
from workflow_engine.nodes.condition_node import ConditionNode
from workflow_engine.nodes.bot_node import BotNode


NODE_MAP = {
    "variable": VariableNode,
    "condition": ConditionNode,
    "bot": BotNode
}