from common import csvimport as ci
import pandas as pd
import matplotlib.pyplot as plt


def main():
    input_data = CreateData()
    pivot_data = pd.pivot_table(input_data, index="payment_month", columns="item_name", values="price", aggfunc="sum")
    print(pivot_data)
    print(input_data.describe())
    ShowGraph(pivot_data)

# データ作成
def CreateData():
    transaction1 = GetData("transaction_1.csv")
    transaction2 = GetData("transaction_2.csv")
    join_transaction = pd.concat([transaction1, transaction2], ignore_index="True")

    detail1 = GetData("transaction_detail_1.csv")
    detail2 = GetData("transaction_detail_2.csv")
    join_detail = pd.concat([detail1, detail2], ignore_index="True")

    customer_master = GetData("customer_master.csv")
    item_master = GetData("item_master.csv")

    # マージ
    join_data = pd.merge(join_detail, join_transaction[["transaction_id", "payment_date", "customer_id"]], on="transaction_id", how="left")
    join_data = pd.merge(join_data, customer_master, on="customer_id", how="left")
    join_data = pd.merge(join_data, item_master, on="item_id", how="left")
    join_data["price"] = join_data["item_price"] * join_data["quantity"]

    ## 日付変換処理
    join_data["payment_date"] = pd.to_datetime(join_data["payment_date"])
    join_data["payment_month"] = join_data["payment_date"].dt.strftime("%Y%m")

    return join_data

# データ取得
def GetData(file_name):
    result = ci.CsvImporter.ExecImport(file_name, 1)
    return result

# グラフ描写
def ShowGraph(pivot_data):
    for item_name in pivot_data.columns:
        plt.plot(list(pivot_data.index), pivot_data[item_name], label = item_name)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()


