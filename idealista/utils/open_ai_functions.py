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

    # try:
    #     cleaned_response = re.sub(r"```|json", "", response.content).strip()
    #     response = json.loads(cleaned_response)
    # except json.JSONDecodeError:
    #     raise ValueError(f"Error decoding the response: {response.content}")


# if __name__ == "__main__":
#     data = """
#     ¡No busques más! Tenemos la plaza de garaje que necesitas en Calle de Sebastián Gómez, precio 90 euros + 21% IVA, Total 108,90 €. No es fácil aparcar en la zona, es habitual ver coches en doble fila. ¡Esta es tu oportunidad! Si tienes un coche nuevo, o no es tan nuevo, pero no quieres que duerma en la calle y no quieres perder tiempo dando vueltas. Tendrás acceso las 24 horas, los 7 días de la semana. El garaje sólo tiene una planta de sótano, es fácil el acceso, una vez vez dentro la maniobra de aparcamiento es sencilla. El edificio tiene conserjería y ascensor para salir a la calle. Los gastos de comunidad son a cargo del propietario. Lo mejor de todo, ¡puedes ver la plaza y probar la maniobra de aparcamiento antes de alquilar! No te lo pienses más, llámanos 6 9 6 0 7 8 1 5 3. Te esperamos. Un saludo.

# Si tienes alguna duda recuerda que puedes hablar con HOUSELINK por chat.

# Publicidad

# Características básicas
# Plaza para coche pequeño
# Cubierta
# Con ascensor
# Extras
# Puerta automática de garaje
# Personal de seguridad
#     """

#     response = extract_item_attributes(data, GarageAttributes)
#     print(response)
#     print(response.size_in_m2)
#     print(response.covered)
#     print(response.security)
#     print(response.type)
#     print(response.concesion)
#     print(response.expenses)
#     print(response.dict())
#     print(response.json())
#     print(response.dict().keys())
#     print(response.dict().values)
