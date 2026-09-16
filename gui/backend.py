# backend.py
import os
import subprocess
import sys
from pathlib import Path

class ExperimentManager:
    def __init__(self, vnn_directory: str = "C:/Users/anasm/OneDrive/Desktop/CRNS/adaptive-crown-verification/VNNLIBS" , onnx_dir : str = "C:/Users/anasm/OneDrive/Desktop/CRNS/adaptive-crown-verification/ONNX" , csv_dir : str = "C:/Users/anasm/OneDrive/Desktop/CRNS/adaptive-crown-verification/CSV", benchmark_dir: str = "C:/Users/anasm/OneDrive/Desktop/CRNS/adaptive-crown-verification/Benchmarks"):
        self.vnn_directory = vnn_directory
        self.onnx_directory = onnx_dir
        self.csv_directory = csv_dir
        self.benchmark_directory = benchmark_dir
        self.selected_benchmark = None

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

    def get_benchmarks(self) -> list[str]:
        if not os.path.exists(self.benchmark_directory):
            return []
        return [
            name
            for name in os.listdir(self.benchmark_directory)
            if os.path.isdir(os.path.join(self.benchmark_directory, name))
        ]

    def benchmark_manage(self, selected_benchmark: str):
        """Handles benchmark folder selection."""
        self.selected_benchmark = selected_benchmark
        full_path = os.path.join(self.benchmark_directory, selected_benchmark)
        print(f"[Backend] Selected benchmark: {full_path}")

    def start_attack(self, selected_benchmark: str, config_path: str = ""):
        """Start the local alpha-beta-CROWN verifier for a benchmark."""
        benchmark_path = os.path.join(self.benchmark_directory, selected_benchmark)
        if not os.path.isdir(benchmark_path):
            print(f"[Backend] Benchmark folder not found: {benchmark_path}")
            return

        project_root = Path(__file__).resolve().parents[2]
        verifier_script = project_root / "adaptive-crown-verification" / "run_verifier.py"
        if not verifier_script.is_file():
            print(f"[Backend] Verifier script not found: {verifier_script}")
            return

        print(f"[Backend] Starting attack for benchmark: {selected_benchmark}")
        command = [sys.executable, str(verifier_script), "--benchmark", benchmark_path]
        if config_path:
            command.extend(["--config", config_path])

        subprocess.Popen(
            command,
            cwd=verifier_script.parent,
        )


    