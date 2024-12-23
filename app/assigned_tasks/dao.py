from datetime import datetime

from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.assigned_tasks.models import AssignedTask
from app.database import get_db
from app.tasks.dao import TaskDAO


class AssignedTaskDAO(BaseDAO):
    model = AssignedTask

    @classmethod
    async def add_with_task(cls, user_id: int, status_id: int, deadline: datetime, title: str,
                            description: str):
        """
        Создает задачу, затем создаёт запись в assigned_tasks с привязкой к созданной задаче.
        """
        new_task = await TaskDAO.add(title=title, description=description)

        assigned_task = await cls.add(
            user_id=user_id,
            task_id=new_task.id,
            status_id=status_id,
            deadline=deadline
        )
        return assigned_task

    @staticmethod
    async def find_all_with_related():
        async for db_session in get_db():
            result = await db_session.execute(
                select(AssignedTask).options(selectinload(AssignedTask.task), selectinload(AssignedTask.status))
            )
            return result.scalars().all()

