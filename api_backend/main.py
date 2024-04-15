import json
import time
from typing import Callable, List, Union

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.utils.base.route_logging import (get_brand_id_from_response_body,
                                              write_log)
from app.api.utils.base.user_profile import get_current_user_profile
from app.api.v1 import (route_brand, route_category, route_download_logs,
                        route_item, route_item_class, route_item_configuration,
                        route_role, route_user_has_role, route_user_profile)
from app.db.base import engine, get_session

app = FastAPI(
    title="ON-Limited API",
    description="This API lets you interact with the ON-Limited ecosystem.",
    version="0.0.1",
    contact={
        "name": "ON-Limited",
        "email": "info@on-limited.com",
    },
    license_info={
        "name": "CC-BY-3.0",
    },
)

origins = [

    "http://localhost:3000",
    "http://localhost:8000",
    "https://app.on-limited.com",
    "https://api.on-limited.com",
    "https://wallet.on-limited.com",
    "http://0.0.0.0:8000",
    "http://0.0.0.0:3000",
    "http://157.245.64.39:8000",
    "http://157.245.64.39:3000",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RouteLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        *,
        skip_routes: Union[List[str], None] = None,
    ):
        self._skip_routes = skip_routes if skip_routes else []
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if self._should_route_be_skipped(request):
            try:
                request.state.db = get_session(engine)
                response = await call_next(request)
            finally:
                request.state.db.close()
            return response
        else:
            return await self._execute_request_with_logging(request, call_next)

    def _should_route_be_skipped(self, request: Request) -> bool:
        return any([True for path in self._skip_routes if request.url.path.startswith(path)])

    async def _execute_request_with_logging(
        self, request: Request, call_next: Callable
    ) -> Response:

        start_time = time.perf_counter()
        try:
            request.state.db = get_session(engine)

            route_url = request.url.path
            method = request.method
            host = request.client.host + ":" + str(request.client.port)

            response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))

            try:
                response_body_json = json.loads((b''.join(response_body)).decode())

            except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                response_body_json = None

            try:
                brand_id = await get_brand_id_from_response_body(response_body_json, request.state.db)
            except (TypeError, HTTPException):
                brand_id = None

            auth_token: Union[str, None] = request.headers.get('Authorization')
            if auth_token is not None and 'Bearer' in auth_token:
                try:
                    current_user_profile = await get_current_user_profile(
                        request.state.db,
                        auth_token.split('Bearer')[1].strip(),
                    )
                    current_user_profile_id = int(str(current_user_profile.user_profile_id))

                except HTTPException:
                    current_user_profile_id = None

            else:
                current_user_profile_id = None

            finish_time = time.perf_counter()
            process_time = finish_time - start_time

            await write_log(
                route_url,
                method,
                host,
                response_body_json,
                current_user_profile_id,
                brand_id,
                process_time,
                request.state.db,
            )

        finally:
            request.state.db.close()

        return response


app.add_middleware(RouteLoggerMiddleware)


@app.get("/")
async def root():
    return {"message": "test api"}

app.include_router(route_user_profile.router)
app.include_router(route_brand.router)
app.include_router(route_role.router)
app.include_router(route_item.router)
app.include_router(route_category.router)
app.include_router(route_item_class.router)
app.include_router(route_item_configuration.router)
app.include_router(route_user_has_role.router)
app.include_router(route_download_logs.router)
