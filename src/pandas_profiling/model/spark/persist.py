import warnings
from typing import Any, Dict

from pyspark.sql import DataFrame


class PersistHandler:
    def __init__(self) -> None:
        self.persisted_spark_objects: Dict[str, Any] = {}

    def persist(self, name: str, spark_object: DataFrame):
        # persist object
        try:
            spark_object.persist()
        except Exception as e:
            warnings.warn(f"Unable to persist {spark_object} due to exception {e}")

        # and track it
        self.persisted_spark_objects[name] = spark_object

    def unpersist(self, name: str):
        if name in self.persisted_spark_objects:

            spark_object = self.persisted_spark_objects[name]

            # unpersist object
            try:
                spark_object.unpersist()
            except Exception as e:
                warnings.warn(
                    f"Unable to unpersist {spark_object} due to exception {e}"
                )

            # then stop tracking it
            self.persisted_spark_objects.pop(name)
        else:
            warnings.warn(f"{name} is not a persisted spark object")

    def unpersist_all(self):
        all_obj_keys = list(self.persisted_spark_objects.keys())
        for key in all_obj_keys:
            self.unpersist(key)


GlobalPersistHandler = PersistHandler()
