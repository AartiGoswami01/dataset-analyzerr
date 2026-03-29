import logging
import os

import click
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from dotenv import load_dotenv
from openai_agent import create_agent
from openai_agent_executor import OpenAIAgentExecutor
from starlette.applications import Starlette


load_dotenv()
logging.basicConfig()


@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=5000)
def main(host: str, port: int):
    # API key check
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError('OPENAI_API_KEY environment variable not set')

    # ✅ FIXED SKILL (NO PLACEHOLDERS)
    skill = AgentSkill(
        id='data_analysis',
        name='Dataset Analyzer',
        description='Analyze datasets and provide insights like mean, min, max, missing values',
        tags=["data", "analysis", "csv", "json"],
        examples=[
            "Analyze this dataset",
            "Find missing values",
            "Give summary statistics",
            "Check if dataset is clean"
        ],
    )

    # ✅ FIXED AGENT CARD
    agent_card = AgentCard(
        name='dataset-analyzer',
        description='AI agent that analyzes datasets and returns structured insights',
        url=f'http://{host}:{port}/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    # Create OpenAI agent
    agent_data = create_agent()

    agent_executor = OpenAIAgentExecutor(
        card=agent_card,
        tools=agent_data['tools'],
        api_key=os.getenv('OPENAI_API_KEY'),
        system_prompt=agent_data['system_prompt'],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=InMemoryTaskStore()
    )

    a2a_app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )

    app = Starlette(routes=a2a_app.routes())

    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    main()