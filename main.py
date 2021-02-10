from typing import List

from fastapi import FastAPI, Depends
import csv
from tortoise.contrib.fastapi import register_tortoise
import logging

from models import Users, User_Pydantic
from tortoise.contrib import fastapi

fastapi.logging = logging.getLogger('uvicorn')

app = FastAPI(title="Fastapi & tortoise")


def get_values_from_csv(csv_filepath=r'UsersData.csv'):
    data = {}
    with open(csv_filepath, encoding='utf-8') as csv_fh:
        csv_reader = csv.DictReader(csv_fh)
        for rows in csv_reader:
            keys = rows['ID']
            data[keys] = rows
    return data


@app.get('/')
async def json_api(user_dict=Depends(get_values_from_csv)):
    # json_values = json.dumps(user_dict)
    return user_dict


@app.post('/post/', response_model=User_Pydantic)
async def create_user(user_dict=Depends(get_values_from_csv)):
    for i in user_dict:
        dict_name = user_dict[i]["Name"]
        dict_email = user_dict[i]["MailID"]
        user_obj = await Users.create(name=dict_name, email=dict_email, exclude_unset=True)
        await User_Pydantic.from_tortoise_orm(user_obj)
    return user_obj


@app.get('/get/', response_model=List[User_Pydantic])
async def get_user():
    return await User_Pydantic.from_queryset(Users.all())


register_tortoise(
    app,
    db_url="postgres://postgres:password@localhost:5432/postgres",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# postgres://postgres:password@localhost:5432/postgres
