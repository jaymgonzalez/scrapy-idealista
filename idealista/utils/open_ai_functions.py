from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai.chat_models.base import ChatOpenAI
from pydantic import BaseModel, Field
import dotenv
import os

dotenv.load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-3.5-turbo"

# Define the prompt template

house_details_template_string = """

Using the following ###house details### extract the information following the exact format that you are asked in the ###instructions###:

###house details###
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
    air_conditioning: int = Field(..., ge=0, le=1)
    terrace: int = Field(..., ge=0, le=1)
    garage: int = Field(..., ge=0, le=1)
    heating: int = Field(..., ge=0, le=1)
    garden: int = Field(..., ge=0, le=1)
    storage_room: int = Field(..., ge=0, le=1)
    swimming_pool: int = Field(..., ge=0, le=1)
    elevator: int = Field(..., ge=0, le=1)


def extract_house_attributes(listing_description):
    pydantic_parser = PydanticOutputParser(pydantic_object=HouseAttributes)
    format_instructions = pydantic_parser.get_format_instructions()
    prompt_template = ChatPromptTemplate.from_template(house_details_template_string)
    messages = prompt_template.format_messages(
        listing_description=listing_description, format_instructions=format_instructions
    )
    chat = ChatOpenAI(temperature=0.3, model=model, api_key=api_key)
    response = chat(messages)

    return response.content
