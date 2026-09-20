import logging
from typing import TypeVar

from django.db.models import Model
from ninja import Schema

ModelType = TypeVar("ModelType", bound=Model)

logger = logging.getLogger(__name__)


class UpdateService:
    @staticmethod
    async def aupdate_instance(
        instance: ModelType,
        payload: Schema,
        partial: bool = False,
        skip_if_same: bool = True,
    ) -> ModelType:
        updated_fields = []
        data = payload.model_dump(exclude_unset=partial)

        for attr, value in data.items():
            if skip_if_same and getattr(instance, attr) == value:
                continue

            setattr(instance, attr, value)
            updated_fields.append(attr)

        if updated_fields:
            logger.info(
                f"Updating {instance.__class__.__name__} {instance.pk}: {updated_fields}"
            )
            await instance.asave(update_fields=updated_fields)

        return instance

    @staticmethod
    def update_instance(
        instance: ModelType,
        payload: Schema,
        partial: bool = False,
        skip_if_same: bool = True,
    ) -> ModelType:
        updated_fields = []
        data = payload.model_dump(exclude_unset=partial)

        for attr, value in data.items():
            if skip_if_same and getattr(instance, attr) == value:
                continue

            setattr(instance, attr, value)
            updated_fields.append(attr)

        if updated_fields:
            logger.info(
                f"Updating {instance.__class__.__name__} {instance.pk}: {updated_fields}"
            )
            instance.save(update_fields=updated_fields)

        return instance
