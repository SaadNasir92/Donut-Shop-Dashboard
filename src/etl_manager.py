class ETLManager:
    def __init__(self, processing_files: list[str]) -> None:
        self.files: list[str] = processing_files
        self.transformed_data: dict = {}

    def log_process(self, info):
        with open(self.logs_file, "a") as file:
            file.write(f"{info}\n")
