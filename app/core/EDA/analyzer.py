# app\core\EDA\analyzer.py
import pandas as pd
import numpy as np
from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.file import File
import os


class DataAnalyzer:
    def __init__(self, db: Session):
        self.db = db

    def get_df(self, file_id: int):
        file_record = (
            self.db.query(File)
            .filter(File.id == file_id)
            .first()
        )

        if not file_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )

        file_path = file_record.file_path

        if not file_path or not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )

        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is not an Excel or CSV file"
            )

        return df

    def calc(self, df: pd.DataFrame):
        total_area = df["Area m²"].sum()
        total_occupancy = df["Occupancy"].sum()
        total_lighting = df["Lighting W"].sum()
        total_equipment = df["Equipment W"].sum()
        total_fresh_air = df["Fresh Air CFM"].sum()

        largest_room = (
            df.loc[df["Area m²"].idxmax(), "Room Name"]
            if not df.empty else None
        )

        largest_room_area = (
            df["Area m²"].max()
            if not df.empty else 0
        )

        avg_area = round(df["Area m²"].mean(), 2)

        # Approximation فقط للتجربة
        estimated_total_load_w = (
            total_lighting +
            total_equipment +
            (total_area * 120)
        )

        estimated_tr = round(estimated_total_load_w / 3517, 2)

        room_names = df["Room Name"].to_list()

        return {
            "total_rooms": int(len(df)),
            "total_area_m2": float(round(total_area, 2)),
            "average_room_area_m2": float(avg_area),
            "total_occupancy": int(total_occupancy),
            "total_lighting_w": float(round(total_lighting, 2)),
            "total_equipment_w": float(round(total_equipment, 2)),
            "total_fresh_air_cfm": float(round(total_fresh_air, 2)),
            "largest_room": str(largest_room) if largest_room is not None else None,
            "largest_room_area_m2": float(round(largest_room_area, 2)),
            "estimated_total_load_w": float(round(estimated_total_load_w, 2)),
            "estimated_tr": float(estimated_tr),
            "room_names": room_names
        }

    def basic_info(self, file_id: int):
        df = self.get_df(file_id=file_id)
        result = self.calc(df=df)
        return result