from workflow_engine.nodes.variable_node import VariableNode
from workflow_engine.nodes.condition_node import ConditionNode
from workflow_engine.nodes.bot_node import BotNode
from workflow_engine.nodes.delay_node import DelayNode
from workflow_engine.nodes.api_node import APINode

NODE_MAP = {
    "variable": VariableNode,
    "condition": ConditionNode,
    "bot": BotNode,
    "delay": DelayNode,
    "api" : APINode
}