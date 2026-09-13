# backend.py
import os

class ExperimentManager:
    def __init__(self, vnn_directory: str = "C:/Users/anasm/OneDrive/Desktop/CRNS/adaptive-crown-verification/VNNLIBS" , onnx_dir : str = "C:/Users/anasm/OneDrive/Desktop/CRNS/adaptive-crown-verification/ONNX" , csv_dir : str = "C:/Users/anasm/OneDrive/Desktop/CRNS/adaptive-crown-verification/CSV"):
        self.vnn_directory = vnn_directory
        self.onnx_directory = onnx_dir
        self.csv_directory = csv_dir

    def get_vnnlib_files(self) -> list[str]:
        if not os.path.exists(self.vnn_directory):
            return []
        return [f for f in os.listdir(self.vnn_directory) if f.endswith(".vnnlib")]

    def vnnlib_manage(self, selected_file: str):
        """Handles single file selection."""
        full_path = os.path.join(self.vnn_directory, selected_file)
        print(f"[Backend] Selected VNNLIB file: {full_path}")

    def get_onnx_files(self) -> list[str]:
        if not os.path.exists(self.onnx_directory):
            return []
        return [f for f in os.listdir(self.onnx_directory) if f.endswith(".onnx")]

    def onnx_manage(self, selected_file: str):
        """Handles single file selection."""
        full_path = os.path.join(self.onnx_directory, selected_file)
        print(f"[Backend] Selected ONNX file: {full_path}")

    def get_csv_files(self) -> list[str]:
        if not os.path.exists(self.csv_directory):
            return []
        return [f for f in os.listdir(self.csv_directory) if f.endswith(".csv")]

    def csv_manage(self, selected_file: str):
        """Handles single CSV file selection."""
        full_path = os.path.join(self.csv_directory, selected_file)
        print(f"[Backend] Selected CSV file: {full_path}")


    