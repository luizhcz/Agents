# Project Name: **CrewAI Processing Service**

## Overview

This project provides a framework for setting up and executing text and table processing tasks using CrewAI. It allows the creation of agents, tasks, and crews based on configurable JSON inputs. The system uses the `crewai` and `langchain_openai` libraries to handle large language models (LLMs), facilitating complex natural language processing workflows.

## Features

- **Agent Creation**: Dynamically create agents using LLMs (like GPT-4) with configurable roles, goals, backstories, and more.
- **Task Management**: Define tasks that agents will execute, with clear descriptions and expected outcomes.
- **Crew Setup**: Create a crew of agents and assign tasks for them to complete in collaboration.
- **Flexible JSON-based Configuration**: Easily configure agents, tasks, and crews through JSON files.
- **Error Handling**: Comprehensive error handling to ensure smooth execution of tasks.

## Requirements

- Python 3.8+
- Required Python libraries:
  - `crewai`
  - `langchain_openai`
  - `json`
  - Any additional dependencies for file handling or application structure.

## Installation

1. Clone the repository:

   ```bash
   https://github.com/luizhcz/CrewAI-Processing-Service.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. **Crew Setup**

You can create agents, tasks, and crews using the `CrewSetup` class. Configure model parameters such as the LLM model name, temperature, and execution time.

Example of creating an agent:

```python
from app.workers.crew_setup import CrewSetup

crew_setup = CrewSetup(model_name="gpt-4o-mini", temperature=0.1)
agent = crew_setup.create_agent(
    role="Data Processor",
    goal="Extract and process financial data",
    backstory="Experienced analyst",
    verbose=True,
    memory=True
)
```

### 2. **Create and Process Crew**

You can create a crew from a JSON file using `CrewService` and process it using `CrewWorker`.

```python
from app.services.crew_service import CrewService
from app.workers.crew_worker import CrewWorker

# Load configuration from JSON
crew_service = CrewService()
crew = crew_service.create_from_json('path/to/your/config.json')

# Execute crew tasks
crew_worker = CrewWorker(crew)
result = crew_worker.process(inputs={"content": "Sample content"})
```

### 3. **Process Text or Table**

Process text or table data using the `ProcessService`.

```python
from app.services.process_service import ProcessService

process_service = ProcessService(crew_service)

# Process text
result = process_service.process_prospect_info(
    content="Example content",
    agent_path='path/to/agent/config.json',
    example_path='path/to/example.json',
    prospect_id="12345"
)

# Process table
converted_text = process_service.process_table_conversion(
    page="Table data",
    agent_path='path/to/agent/config.json',
    example_path='path/to/example.json',
    overlap="Overlapping text"
)
```

### JSON Configuration Example

Here's an example of a JSON configuration for agents, tasks, and crew:

```json
{
  "model_config": {
    "model_name": "gpt-4o-mini",
    "temperature": 0.1,
    "max_execution_time": 999999
  },
  "agent": {
    "role": "Data Analyst",
    "goal": "Analyze data trends",
    "backstory": "Expert in financial data analysis",
    "verbose": true,
    "memory": true,
    "max_iter": 20
  },
  "task": {
    "description": "Analyze the provided data",
    "expected_output": "Summary of data trends"
  },
  "crew": {
    "verbose": 2
  }
}
```

## Error Handling

The system includes error handling mechanisms to catch exceptions during processing, providing meaningful feedback and logging errors.

Example:

```python
try:
    result = crew_worker.process(inputs={"content": "Sample content"})
except Exception as e:
    print(f"Error processing task: {e}")
```

## Contribution

Feel free to contribute by opening issues, submitting pull requests, or improving the documentation.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

This readme provides an introduction to setting up and using the CrewAI Processing Service for text and table tasks. For more advanced configurations, refer to the code and JSON templates provided in the repository.
