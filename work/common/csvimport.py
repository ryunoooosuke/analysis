import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


file_path = os.environ['INPUT_FILE_PATH']
class CsvImporter:
    # csvファイル読み込み実行
    @staticmethod
    def ExecImport(file_name, work_no):
        result = pd.read_csv(file_path + str(work_no) + "/" + file_name)
        return result

    