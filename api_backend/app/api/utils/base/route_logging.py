import io
from typing import Any, List, Union

import pandas as pd  # type: ignore
from app.api.utils.base.brand import get_brand_from_name
from app.db.models.brand import Brand
from app.db.models.route_logging import RouteLogging
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def write_log(
    route_url: str,
    request_method: str,
    host: str,
    response: Union[str, None],
    current_user_profile_id: Union[int, None],
    brand_id: Union[int, None],
    process_time: float,
    db: Session,
):
    log = RouteLogging(
        route_url=route_url,
        request_method=request_method,
        host=host,
        response=response,
        current_user_profile_id=current_user_profile_id,
        brand_id=brand_id,
        process_time=process_time,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


async def get_csv_stream_with_logs_of_brand_from_brand_name(brand_name: str, db: Session):
    brand = await get_brand_from_name(db, brand_name)
    if brand is None:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"brand {brand_name} does note exist")

    stream = io.StringIO()
    query = db.query(RouteLogging).filter(RouteLogging.brand_id == brand.brand_id)
    brand_logs = pd.read_sql(query.statement, query.session.bind)
    brand_logs.to_csv(stream, index=False)

    return stream


async def get_brand_id_from_response_body(response_body_json: Any, db: Session):
    if response_body_json is not None:
        if not(isinstance(response_body_json, (str, list))):
            brand_id = await get_brand_id_from_single_response_body(response_body_json, db)
            return brand_id

        elif not(isinstance(response_body_json, str)):
            response_body_json_list: List[dict] = list(response_body_json)
            for response_body in response_body_json_list:
                if not(isinstance(response_body, str)):
                    brand_id = await get_brand_id_from_single_response_body(response_body, db)
                    if brand_id is not None:
                        return brand_id
    return None


async def get_brand_id_from_single_response_body(response_body_json, db: Session):
    if response_body_json.get('brand_id') is not None:
        return response_body_json.get('brand_id')
    elif response_body_json.get('brand_name') is not None:
        brand_name = response_body_json.get('brand_name')
        brand = await get_brand_from_name(db, brand_name) if isinstance(brand_name, str) else None
        if isinstance(brand, Brand):
            return int(str(brand.brand_id))
    return None
