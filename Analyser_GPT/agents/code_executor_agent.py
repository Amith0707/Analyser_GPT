from autogen_agentchat.agents import CodeExecutorAgent

def getCodeExecutorAgent(code_Executor):

    code_Executor_agent=CodeExecutorAgent(
        name="Python_Code_Executor_Agent",
        code_executor=code_Executor
    )
    return code_Executor_agent
    