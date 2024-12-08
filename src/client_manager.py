from src import SERVICE
import io
import pandas as pd
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime as dt


class ClientManager:
    def __init__(self) -> None:
        self.logs_file = "datasets/client_shared/logs/google_drive_logs.txt"
        self.raw_archive_folder = "datasets/client_shared/archive_raw/"
        self.to_be_processed_folder = "datasets/client_shared/to_be_processed/"
        self.processed_folder = "datasets/client_shared/archive_processed/"

        self.log_process("Initializing client")

        self.contents = None
        self.files_to_process = []
        self.folders_information = []
        self.num_files_to_process = 0
        self.time_stamp = str(dt.now()).replace(":", "-")

        self.get_drive_contents()

    def get_drive_contents(self) -> None:
        self.log_process("Checking for available files...")
        response = (
            SERVICE.files()
            .list(
                pageSize=500,
                fields="files(id, name)",
            )
            .execute()
        )
        items = response.get("files", [])

        self.contents = items

        for content in self.contents:
            if "." in content["name"]:
                self.files_to_process.append(content)
            else:
                self.folders_information.append(content)

        self.num_files_to_process = len(self.files_to_process)

        self.log_process(f"Obtained {(self.num_files_to_process)} file(s) to process.")

        if self.num_files_to_process > 0:
            self.log_process("Archiving incoming file(s) from client.")

            for idx, content in enumerate(self.files_to_process):
                file_name = content["name"]
                file_id = content["id"]
                df = self.download_file(file_name, file_id)
                new_file_name = self.archive_incoming_data(df, file_name, file_id)
                self.files_to_process[idx]["name"] = new_file_name

            self.log_process(
                f"{self.num_files_to_process} files archived on {self.time_stamp}. Ready for processing."
            )

        else:
            self.log_process(f"No files to process at {self.time_stamp}")
            print("No files to process.")

    def download_file(self, file_name: str, file_id: str) -> pd.DataFrame:
        response = SERVICE.files().get_media(fileId=file_id)
        file_ = io.BytesIO()
        downloader = MediaIoBaseDownload(file_, response)

        done = False

        self.log_process(f"Downloading {file_name}.")

        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")

        # When downloading in chunks, the marker is at end of file because that is where the last chunk ended.
        # Seek 0 returns the marker to beginning of the file.
        file_.seek(0)
        df = pd.read_csv(file_)

        self.log_process(f"Downloaded {file_name}.")

        return df

    def log_process(self, info):
        with open(self.logs_file, "a") as file:
            file.write(f"{info}\n")

    def archive_incoming_data(
        self, dataframe: pd.DataFrame, file_name: str, file_id: str
    ) -> str:
        archive_path = f"{self.raw_archive_folder}{file_name.split('.')[0]}-{file_id}-{self.time_stamp}.csv"

        to_be_processed_path = f"{self.to_be_processed_folder}{file_name.split('.')[0]}-{file_id}-{self.time_stamp}.csv"

        dataframe.columns = dataframe.columns.str.lower().str.replace(" ", "_")
        dataframe.to_csv(archive_path, index=False)
        dataframe.to_csv(to_be_processed_path, index=False)

        self.log_process(
            f"Archived {file_name} with File ID: ({file_id}) at {self.time_stamp}."
        )

        return to_be_processed_path
