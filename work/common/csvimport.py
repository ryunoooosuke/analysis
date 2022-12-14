import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

class CsvImporter:
    
    # csvファイル読み込み実行
    def ExecImport(file_name, work_no):
        file_path = os.environ['INPUT_FILE_PATH']
        result = pd.read_csv(os.environ['INPUT_FILE_PATH'] + str(work_no) + "/" + file_name)
        return result

    