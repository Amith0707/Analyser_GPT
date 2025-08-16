from autogen_agentchat.agents import CodeExecutorAgent
import asyncio
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor #--->Runs a code in docker
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage

async def main():
    docker=DockerCommandLineCodeExecutor(
        work_dir='/tmp',
        timeout=120
    )
    code_executor_agent=CodeExecutorAgent(
        name='CodeExecutorAgent',
        code_executor=docker,
    )
    task=TextMessage(
        content='''Here is the code
    ```Python
print('Hello World') 
    ```
        ''',
        source='user'
    )
    await docker.start()

    result=await code_executor_agent.on_messages(
        messages=[task],
        cancellation_token=CancellationToken()
    )
    await docker.stop()
    print("The result is: ",result)

if (__name__=="__main__"):
    asyncio.run(main())