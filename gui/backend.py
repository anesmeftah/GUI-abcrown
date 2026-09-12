# backend.py
import os

class ExperimentManager:
    def __init__(self, target_directory: str = "C:/Users/anasm/OneDrive/Desktop/CRNS/adaptive-crown-verification/VNNLIBS"):
        self.target_directory = target_directory

    def get_vnnlib_files(self) -> list[str]:
        if not os.path.exists(self.target_directory):
            return []
        return [f for f in os.listdir(self.target_directory) if f.endswith(".vnnlib")]

    def vnnlib_manage(self, selected_file: str):
        """Handles single file selection."""
        full_path = os.path.join(self.target_directory, selected_file)
        print(f"[Backend] Selected VNNLIB file: {full_path}")