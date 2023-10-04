from typing import List

from ..registry import ability

# synthesize deps
import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@ability(
    name="list_files",
    description="List files in a directory",
    parameters=[
        {
            "name": "path",
            "description": "Path to the directory",
            "type": "string",
            "required": True,
        }
    ],
    output_type="list[str]",
)
async def list_files(agent, task_id: str, path: str) -> List[str]:
    """
    List files in a workspace directory
    """
    return agent.workspace.list(task_id=task_id, path=path)


@ability(
    name="write_file",
    description="Write data to a file",
    parameters=[
        {
            "name": "file_path",
            "description": "Path to the file",
            "type": "string",
            "required": True,
        },
        {
            "name": "data",
            "description": "Data to write to the file",
            "type": "bytes",
            "required": True,
        },
    ],
    output_type="None",
)
async def write_file(agent, task_id: str, file_path: str, data: bytes) -> None:
    """
    Write data to a file
    """
    if isinstance(data, str):
        data = data.encode()

    agent.workspace.write(task_id=task_id, path=file_path, data=data)
    await agent.db.create_artifact(
        task_id=task_id,
        file_name=file_path.split("/")[-1],
        relative_path=file_path,
        agent_created=True,
    )


@ability(
    name="read_file",
    description="Read data from a file",
    parameters=[
        {
            "name": "file_path",
            "description": "Path to the file",
            "type": "string",
            "required": True,
        },
    ],
    output_type="bytes",
)
async def read_file(agent, task_id: str, file_path: str) -> bytes:
    """
    Read data from a file
    """
    read_text = agent.workspace.read(task_id=task_id, path=file_path)
    agent.workspace.write(task_id=task_id, path="/output.txt", data=read_text)
    await agent.db.create_artifact(
        task_id=task_id,
        file_name='output.txt',
        relative_path='/output.txt',
        agent_created=True,
    )
    print("Testing",file_path)
    return read_text


# {
#   "name": "Create a brief report or summary highlighting how one or more companies from companies.txt are addressing or capitalizing on challenges or trends from challenges.txt. Write a file called output.txt.",
#   "input": "Create a brief report or summary highlighting how one or more companies from companies.txt are addressing or capitalizing on challenges or trends from challenges.txt. Write a file called output.txt.",
#   "additional_input": {},
#   "created_at": "2023-10-04T19:20:43.257265",
#   "modified_at": "2023-10-04T19:20:43.257268",
#   "task_id": "f7e7b984-c794-402c-9237-4f3194bde24a",
#   "step_id": "3cf31b8e-6b9a-4030-b4c7-d131ddcc4ac8",
#   "status": "created",
#   "output": null,
#   "additional_output": {},
#   "artifacts": [],
#   "is_last": true
# }

# synthesize_info

@ability(
    name="synthesize_info",
    description="Create a brief report or summary highlighting how one or more companies from companies.txt are addressing or capitalizing on challenges or trends from challenges.txt. Write a file called output.txt.",
    parameters=[
        {
            "name": "file_path1",
            "description": "1st Path to the file",
            "type": "string",
            "required": True,
        },
        {
            "name": "file_path2",
            "description": "2nd Path to the file",
            "type": "string",
            "required": True,
        },
    ],
    output_type="bytes",
)
async def synthesize_info(agent, task_id: str, file_path1: str, file_path2: str) -> bytes:
    """
    Read data from a file
    """
    # Read file 1
    read_text1 = agent.workspace.read(task_id=task_id, path=file_path1)
    # Read file 2
    read_text2 = agent.workspace.read(task_id=task_id, path=file_path2)
    # Rules
    rules = f'Create a brief report or summary highlighting how one or more companies from {read_text1} are addressing or capitalizing on challenges or trends from {read_text2}. The company mentioned in the output must actively address or capitalize on the challenges or trends listed. Format ability like '

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": f"{rules}"}])
    print("Testing completion", completion)

    agent.workspace.write(task_id=task_id, path="/output.txt", data=completion['choices'][0]['message']['content'].encode())
    await agent.db.create_artifact(
        task_id=task_id,
        file_name='output.txt',
        relative_path='/output.txt',
        agent_created=True,
    )
    return completion['choices'][0]['message']['content'].encode()