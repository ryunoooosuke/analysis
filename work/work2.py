from common import csvimport as ci
import pandas as pd
import matplotlib.pyplot as plt


def main():
    CreateDumpFile()

    # 商品毎、顧客毎、地域毎の年月単位の購入回数、金額
    import_data = GetData("dump_data.csv")
    pivot_by_price = import_data.pivot_table(index="purchase_month", columns="item_name", values="item_price", aggfunc="sum", fill_value=0)
    pivot_by_customer = import_data.pivot_table(index="purchase_month", columns="顧客名", aggfunc="size", fill_value=0)
    pivot_by_region = import_data.pivot_table(index="purchase_month", columns="地域", aggfunc="size", fill_value=0)

    print(pivot_by_price)
    print(pivot_by_customer)
    print(pivot_by_region)

    # 購入がないユーザー
    earnings_data = GetEarningsData()
    customer_data = GetCustomerData()
    away_data = pd.merge(earnings_data, customer_data, left_on="customer_name", right_on="顧客名", how="right")
    print(away_data[away_data["purchase_date"].isnull()][["顧客名", "メールアドレス", "登録日"]])

# dumpファイル作成
def CreateDumpFile():
    earnings_data = GetEarningsData()
    customer_data = GetCustomerData()

    join_data = pd.merge(
        earnings_data,
        customer_data,
        left_on="customer_name",
        right_on="顧客名",
        how="left")
    join_data = join_data.drop("customer_name", axis=1)
    dump_data = join_data[[
        "purchase_date",
        "purchase_month",
        "item_name",
        "item_price",
        "顧客名",
        "かな",
        "地域",
        "メールアドレス",
        "登録日"]]

    dump_data.to_csv("dump_data.csv", index=False)

# 売上データ取得変換
def GetEarningsData():
    earnings_data = GetData("uriage.csv")

    # 小文字→大文字変換
    earnings_data["item_name"] = earnings_data["item_name"].str.upper()
    # スペース除去
    earnings_data["item_name"] = earnings_data["item_name"].str.replace("　", "")
    earnings_data["item_name"] = earnings_data["item_name"].str.replace(" ", "")

    earnings_data["purchase_date"] = pd.to_datetime(earnings_data["purchase_date"])
    earnings_data["purchase_month"] = earnings_data["purchase_date"].dt.strftime("%Y%m")

    # 欠損データ保管（金額「item_price」）
    flg_is_null = earnings_data["item_price"].isnull()
    for null_item_name in list(earnings_data.loc[flg_is_null, "item_name"].unique()):
        price = earnings_data.loc[(~flg_is_null) & (earnings_data["item_name"] == null_item_name), "item_price"].max()
        earnings_data.loc[(flg_is_null) & (earnings_data["item_name"] == null_item_name), "item_price"] = price

    # 確認用
    '''   
    for item_name in list(earnings_data["item_name"].sort_values().unique()):
        print(item_name
        + ":"
        + str(earnings_data.loc[earnings_data["item_name"] == item_name]["item_price"].max())
        + ", "
        + str(earnings_data.loc[earnings_data["item_name"] == item_name]["item_price"].min()))
    ''' 
    return earnings_data

# 顧客データ変換
def GetCustomerData():
    customer_data = GetData("kokyaku_daicho.xlsx")
    # スペース除去
    customer_data["顧客名"] = customer_data["顧客名"].str.replace("　", "")
    customer_data["顧客名"] = customer_data["顧客名"].str.replace(" ", "")

    # 日付の変換
    flg_is_serial = customer_data["登録日"].astype("str").str.isdigit()
    from_serial = pd.to_timedelta(
        customer_data.loc[flg_is_serial, "登録日"].astype("float") - 2,
        unit="D") + pd.to_datetime("1900/1/1")
    # 書式の統一
    from_string = pd.to_datetime(customer_data.loc[~flg_is_serial, "登録日"])
    customer_data["登録日"] = pd.concat([from_serial, from_string])
    customer_data["登録年月"] = customer_data["登録日"].dt.strftime("%Y%m")
    return customer_data

def CheckEarningsData():
    earnings_data = GetData("uriage.csv")
    earnings_data["purchase_date"] = pd.to_datetime(earnings_data["purchase_date"])
    earnings_data["purchase_month"] = earnings_data["purchase_date"].dt.strftime("%Y%m")
    pivot_data = pd.pivot_table(earnings_data, index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
    pivot_data2 = pd.pivot_table(earnings_data, index="purchase_month", columns="item_name", values="item_price", aggfunc="sum", fill_value=0)
    print(len(pd.unique(earnings_data["item_name"])))

# データ取得
def GetData(file_name):
    result = ci.CsvImporter.ExecImport(file_name, 2)
    return result

# グラフ描写
def ShowGraph(pivot_data):
    for item_name in pivot_data.columns:
        plt.plot(list(pivot_data.index), pivot_data[item_name], label = item_name)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()


