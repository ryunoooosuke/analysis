import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


file_path = os.environ['INPUT_FILE_PATH']
class CsvImporter:
    # csvファイル読み込み実行
    @staticmethod
    def ExecImport(file_name, work_no):
        extension = str(file_name).split('.')[1]
        result = ""
        match extension:
            case "csv":
                result = pd.read_csv(file_path + str(work_no) + "/" + file_name)
            
            case "xlsx":
                result = pd.read_excel(file_path + str(work_no) + "/" + file_name)

        return result

    