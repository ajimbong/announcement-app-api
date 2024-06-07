from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import api.crud.permission as crud
from api.crud.channel import get_channel
from api.crud.staff import get_staff
import api.schemas.permission as schema
from api.utils.dependencies import get_db

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
    dependencies=[],
)


@router.get("/", response_model=list[schema.Permission], status_code=status.HTTP_200_OK)
def get_permissions(channel_id: Optional[int] = None, staff_id: Optional[int]=None, db: Session = Depends(get_db)):
    """
    ## Behaves like a Generic Get function for many and single items
    - Can get all permissions filtered by channel id and student id.
    - Can get permissions filtered by channel id only.
    - Can get permissions filtered by student id only.

    > N/B: You can't get all the permissions
    """

    if channel_id is not None and staff_id is not None:
        return crud.get_permissions_for_staff(db, staff_id=staff_id)
    elif channel_id is not None:
        return crud.get_permissions_for_channel(db, channel_id=channel_id)
    elif staff_id is not None:
        return crud.get_permissions_for_staff(db, staff_id=staff_id)

    return []


@router.post("/", response_model=schema.Permission, status_code=status.HTTP_201_CREATED)
def create_permission(permission: schema.PermissionCreate, db: Session = Depends(get_db)):
    """
    - Verify if Channel ID is correct
    - Verify if Staff ID is correct
    - Check if Table entry already exists
    - Create Permission
    """

    channel_id = permission.channel_id
    db_channel = get_channel(db, channel_id)
    if db_channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

    staff_id = permission.staff_id
    db_staff = get_staff(db, staff_id)
    if db_staff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    db_permission = crud.get_permission_for_channel_and_staff(db, channel_id, staff_id)
    print(db_permission)
    if db_permission is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Channel Permission already exists")

    return crud.add_permission(db, permission)


@router.put("/", response_model=schema.Permission, status_code=status.HTTP_200_OK)
def update_permission(permission: schema.PermissionUpdate, db: Session = Depends(get_db)):
    """
    > We don't have any dynamic path because the staff_id and channel_id
      will be gotten from the body object

    - Verifies if entry exists to update
    - Perform update action
    """

    channel_id = permission.channel_id
    staff_id = permission.staff_id

    db_permission = crud.get_permission_for_channel_and_staff(db, channel_id, staff_id)
    if db_permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel Permission not found")

    return crud.update_permission(db, permission)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission: schema.PermissionDelete, db: Session = Depends(get_db)):
    """
        > We don't have any dynamic path because the staff_id and channel_id
          will be gotten from the body object

        - Verifies if entry exists to delete
        - Perform delete action
        """

    channel_id = permission.channel_id
    staff_id = permission.staff_id

    db_permission = crud.get_permission_for_channel_and_staff(db, channel_id, staff_id)
    if db_permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel Permission not found")

    crud.delete_permission(db, channel_id, staff_id)
    return JSONResponse(content={"detail": "Channel Permission Deleted"})
