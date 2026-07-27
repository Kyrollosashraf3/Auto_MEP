# app/core/EDA/analyzer.py

import os
import numpy as np
import pandas as pd

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.file import File
from app.models.project import Project
from app.models.analysis_result import AnalysisResult
from app.config.logger import get_logger

logger = get_logger(__name__)

# ==========================================================
class DataAnalyzer:

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # Read File
    # ==========================================================

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
            return pd.read_excel(file_path)

        elif file_path.endswith(".csv"):
            return pd.read_csv(file_path)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type"
        )

    # ==========================================================
    # Engineering Calculations
    # ==========================================================

    def calc(self, df: pd.DataFrame):

        total_rooms = len(df)

        total_area = df["Area m²"].sum()
        avg_area = df["Area m²"].mean()

        total_occupancy = df["Occupancy"].sum()
        avg_occupancy = df["Occupancy"].mean()

        total_lighting = df["Lighting W"].sum()
        avg_lighting = df["Lighting W"].mean()

        total_equipment = df["Equipment W"].sum()
        avg_equipment = df["Equipment W"].mean()

        total_fresh_air = df["Fresh Air CFM"].sum()
        avg_fresh_air = df["Fresh Air CFM"].mean()

        largest_room = df.loc[
            df["Area m²"].idxmax(),
            "Room Name"
        ]

        largest_room_area = df["Area m²"].max()

        highest_occupancy_room = df.loc[
            df["Occupancy"].idxmax(),
            "Room Name"
        ]

        highest_occupancy = df["Occupancy"].max()

        highest_fresh_air_room = df.loc[
            df["Fresh Air CFM"].idxmax(),
            "Room Name"
        ]

        highest_fresh_air = df["Fresh Air CFM"].max()

        lighting_density = (
            total_lighting / total_area
            if total_area else 0
        )

        equipment_density = (
            total_equipment / total_area
            if total_area else 0
        )

        fresh_air_per_person = (
            total_fresh_air / total_occupancy
            if total_occupancy else 0
        )

        estimated_total_load_w = (
            total_lighting
            + total_equipment
            + (total_area * 120)
        )

        estimated_tr = estimated_total_load_w / 3517

        calc =  {
            "total_rooms": total_rooms,

            "room_names": df["Room Name"].tolist(),

            "total_area_m2": round(total_area, 2),

            "average_room_area_m2": round(avg_area, 2),

            "largest_room": largest_room,

            "largest_room_area_m2": round(
                largest_room_area,
                2
            ),

            "total_occupancy": total_occupancy,

            "average_occupancy": round(
                avg_occupancy,
                2
            ),

            "highest_occupancy_room": highest_occupancy_room,

            "highest_occupancy": highest_occupancy,

            "total_lighting_w": round(
                total_lighting,
                2
            ),

            "average_lighting_w": round(
                avg_lighting,
                2
            ),

            "lighting_density_w_m2": round(
                lighting_density,
                2
            ),

            "total_equipment_w": round(
                total_equipment,
                2
            ),

            "average_equipment_w": round(
                avg_equipment,
                2
            ),

            "equipment_density_w_m2": round(
                equipment_density,
                2
            ),

            "total_fresh_air_cfm": round(
                total_fresh_air,
                2
            ),

            "average_fresh_air_cfm": round(
                avg_fresh_air,
                2
            ),

            "fresh_air_per_person": round(
                fresh_air_per_person,
                2
            ),

            "highest_fresh_air_room": highest_fresh_air_room,

            "highest_fresh_air_cfm": round(
                highest_fresh_air,
                2
            ),

            "estimated_total_load_w": round(
                estimated_total_load_w,
                2
            ),

            "estimated_tr": round(
                estimated_tr,
                2
            )
        }

        calc = DataAnalyzer.convert_numpy(calc)

        return calc

    # ==========================================================
    # Convert NumPy Objects
    # ==========================================================

    @staticmethod
    def convert_numpy(obj):

        if isinstance(obj, dict):
            return {
                key: DataAnalyzer.convert_numpy(value)
                for key, value in obj.items()
            }

        if isinstance(obj, list):
            return [
                DataAnalyzer.convert_numpy(item)
                for item in obj
            ]

        if isinstance(obj, tuple):
            return tuple(
                DataAnalyzer.convert_numpy(item)
                for item in obj
            )

        if isinstance(obj, np.integer):
            return int(obj)

        if isinstance(obj, np.floating):
            return float(obj)

        if isinstance(obj, np.bool_):
            return bool(obj)

        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return obj
        
    def get_file_data(self, file_id: int) -> dict: 
        file_record = ( self.db.query(File, Project.name) .
                        join(Project, File.project_id == Project.id) 
                        .filter(File.id == file_id) 
                        .first() 
                      ) 

        
        if not file_record: 
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="File not found" ) 
        
        file = file_record[0] 
        project_name = file_record[1] 
        return ( file.file_name, project_name, )
    # ==========================================================
    # Public Method
    # ==========================================================

    def basic_info(self, file_id: int):
        
        cache = self.get_cached_result(file_id, "analysis")

        if cache:
            logger.info(f"Analysis cache hit for file {file_id}")
            analysis_result = {
                "calc": cache.result_json,
                "file_name": cache.file_name,
                "project_name": cache.project_name
            }
            return analysis_result
        
        logger.info(f"Running analysis for file {file_id}")
        df = self.get_df(file_id)
        file_name, project_name = self.get_file_data(file_id)
        calc = self.calc(df)

        analysis_result = {
            "calc": calc,
            "file_name": file_name,
            "project_name": project_name
        }

        self.save_result(file_id, "analysis", calc, file_name, project_name)

        return analysis_result







    def get_cached_result(self, file_id: int, type_: str):
        return (
            self.db.query(AnalysisResult)
            .filter(
                AnalysisResult.file_id == file_id,
                AnalysisResult.type == type_
            )
            .first()
        )


    def save_result(self, file_id: int, type_: str, calc: dict, file_name: str, project_name: str):
        existing = self.get_cached_result(file_id, type_)

        if existing:
            existing.result_json = calc
            existing.file_name = file_name
            existing.project_name = project_name
        else:
            existing = AnalysisResult(
                file_id=file_id,
                type=type_,
                result_json=calc,
                file_name=file_name,
                project_name=project_name
            )
            self.db.add(existing)

        self.db.commit()
        self.db.refresh(existing)
        return existing













"""
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
"""
