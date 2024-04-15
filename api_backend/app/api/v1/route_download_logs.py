from datetime import date

import fastapi
from app.api.utils.base.role import BRAND_ROLE_NAMES_DICT
from app.api.utils.base.route_logging import \
    get_csv_stream_with_logs_of_brand_from_brand_name
from app.api.utils.base.user_has_role import check_user_has_role_for_brand
from app.api.utils.base.user_profile import get_current_user_profile
from app.db.base import get_db
from app.db.models.user_profile import UserProfile, UserTypes
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK

router = fastapi.APIRouter()


@router.get(
    "/v1/download_logs/{brand_name}", dependencies=[fastapi.Depends(get_current_user_profile)]
)
async def download_brand_related_logs_route(
    brand_name: str,
    db: Session = fastapi.Depends(get_db),
    current_user_profile: UserProfile = fastapi.Depends(get_current_user_profile),
):
    if current_user_profile.user_type not in [UserTypes.BUSINESS_ADMIN, UserTypes.ON_ADMIN]:
        raise HTTPException(
            status_code=HTTP_200_OK, detail="you do not have the right to download logs..."
        )

    if current_user_profile.user_type == UserTypes.BUSINESS_ADMIN:
        current_user_is_brand_admin = await check_user_has_role_for_brand(
            db, str(current_user_profile.username), BRAND_ROLE_NAMES_DICT["business_admin"], brand_name
        )
        if not current_user_is_brand_admin:
            raise HTTPException(
                status_code=HTTP_200_OK, detail=f"you are not admin of the brand {brand_name}"
            )

    csv_strem = await get_csv_stream_with_logs_of_brand_from_brand_name(brand_name, db)
    date_today = date.today().strftime('%Y%m%d')
    return StreamingResponse(
        iter([csv_strem.getvalue()]),
        media_type="text/csv",
        headers={'Content-Disposition': f'attachment; filename={brand_name}_{date_today}_logs.csv'},
    )
