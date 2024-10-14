import os
from fastapi import APIRouter, HTTPException
from app.models.data_model import InputData, InputTable
from app.services.process_service import ProcessService
from app.services.crew_service import CrewService
from app.repositories.mongo_repository import MongoRepository

router = APIRouter()

# Initialize necessary services
crew_service = CrewService()
process_service = ProcessService(crew_service=crew_service)
mongo_repo = MongoRepository()

@router.post("/process/")
async def process_data(data: InputData):
    """
    Processes the provided text using CrewAI and returns the result.

    :param data: Input data containing text and ID.
    :return: A JSON response with the processed data.
    """
    try:
        agent_path = os.path.join("jsons", "agent", "get_info_prospect.json")
        example_path = os.path.join("jsons", "example", "get_info_prospect.json")

        
        # Process the text with CrewAI
        processed_data = process_service.process_prospect_info(
            content=data.text,
            prospect_id=data.id,
            agent_path=agent_path,
            example_path=example_path
        )

        # Optionally save the result to MongoDB
        # mongo_repo.save_result(processed_data)

        return {"status": "success", "data": processed_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tables/")
async def process_tables(data: InputTable):
    """
    Processes the table data using CrewAI and returns the converted text.

    :param data: Input data containing table content and overlap.
    :return: A JSON response with the converted text.
    """
    try:
        overlap_str = "\n".join(data.overlap)
        
        agent_path = os.path.join("json", "agent", "convert_table_in_text.json")
        example_path = os.path.join("json", "example", "convert_table_in_text.json")

        # Process the table data with CrewAI
        processed_data = process_service.process_convert_table(
            agent_path=agent_path,
            example_path=example_path,
            overlap=overlap_str,
            page=data.page
        )

        return {"status": "success", "converted_text": processed_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_status():
    """
    Returns the status of the API.

    :return: A JSON response with the status message.
    """
    return {"status": "success"}