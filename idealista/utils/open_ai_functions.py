from pydantic import BaseModel, Field
import instructor
import dotenv
import openai
import os

dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4o-mini-2024-07-18"

client = instructor.from_openai(openai.OpenAI(), mode=instructor.Mode.TOOLS)

message = {
    "role": "user",
    "content": """Extract the ###property_details### from the following information and accurately fill the required fields.

                ###property_details###
                `{{listing_description}}`
                ###property_details###

                If you succeed you will receive a tip.

                Take a deep breath, think about what you are about to do, and start working on it.""",
}


class GarageAttributes(BaseModel):
    size_in_m2: int = Field(description="Size in square meters. If unknown, use 0")
    covered: bool = Field(description="Is the garage covered?")
    security: bool = Field(description="Is there human security?")
    type: str = Field(
        description="What type of vehicle fits: big car, motorcycle, small car, etc"
    )
    concesion: bool = Field(description="Is it a concession from the city?")
    expenses: int = Field(description="Monthly expenses, IBI, etc. If unknown, use 0")


def extract_item_attributes(listing_description, pydantic_object):
    response = client.chat.completions.create(
        model=model,
        messages=[message],
        response_model=pydantic_object,
        context={"listing_description": listing_description},
        max_retries=2,
    )

    return response.dict()


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
