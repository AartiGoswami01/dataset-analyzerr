from agent_toolset import DatasetAnalyzerToolset

def create_agent():
    toolset = DatasetAnalyzerToolset()

    return {
        "tools": toolset.get_tools(),
        "system_prompt": "You are a dataset analyzer. Always return results in JSON format."
    }