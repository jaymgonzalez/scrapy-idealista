from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import dotenv
import json
import os
import re

dotenv.load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4o-mini-2024-07-18"

# Define the prompt template

property_details_template_string = """

Extract the following ###property_details### using the information ###instructions### in the exact format provided.

###property_details###
{listing_description}

###instructions###
{format_instructions}

If you succeed you will receive a tip.

Take a deep breath, think about what you are about to do, and start working on it.

"""


class HouseAttributes(BaseModel):
    house_size: str
    condition: str
    house_type: str
    rooms: int
    floors: int
    bathrooms: int
    lot_size: int
    built_year: int
    air_conditioning: bool
    terrace: bool
    garage: bool
    heating: bool
    garden: bool
    storage_room: bool
    swimming_pool: bool
    elevator: bool


class GarageAttributes(BaseModel):
    size_in_m2: int
    covered: bool = Field(description="Is the garage covered?")
    security: bool = Field(description="Is there human security ?")
    type: str = Field(
        description="What type of vehicle fits: big car, motorcycle, small car, etc"
    )
    concesion: bool = Field(description="Is it a concession from the city?")
    expenses: int = Field(description="Monthly expenses, IBI, etc")


def extract_item_attributes(listing_description, pydantic_object):
    pydantic_parser = PydanticOutputParser(pydantic_object=pydantic_object)
    format_instructions = pydantic_parser.get_format_instructions()
    prompt_template = ChatPromptTemplate.from_template(property_details_template_string)
    messages = prompt_template.format_messages(
        listing_description=listing_description, format_instructions=format_instructions
    )
    chat = ChatOpenAI(temperature=0.3, model=model, api_key=api_key)
    response = chat(messages)
    try:
        cleaned_response = re.sub(r"```|json", "", response.content).strip()
        response = json.loads(cleaned_response)
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding the response: {response.content}")

    return response
