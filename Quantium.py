import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.pyplot as plt

# vẽ biểu đồ doanh thu để tìm ra ngày bị thiếu

    # Kết nối đến cơ sở dữ liệu SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-CD1J161\TRIET;DATABASE=Quantium')

    # Truy vấn SQL để lấy dữ liệu từ cơ sở dữ liệu
query = "SELECT BUYDATE, TOTAL_RN FROM dbo.REVENUE order by BUYDATE "

query1 = "SELECT * FROM dbo.TABLEFIXDATE"

query2 = "SELECT * FROM dbo.SIZEBUY order by SIZE"

query3 = "SELECT LIFESTAGE, PREMIUM_CUSTOMER, TOT_SALES, LYLTY_CARD_NBR, PROD_QTY  FROM dbo.TOTALDATA "

    # Sử dụng pandas để đọc dữ liệu từ kết quả truy vấn vào DataFrame
df = pd.read_sql(query, conn)

df2 = pd.read_sql(query2, conn)

df3 = pd.read_sql(query3, conn)
  
    # Đóng kết nối sau khi hoàn thành
conn.close()
# Chuyển đổi cột 'BUYDATE' thành kiểu datetime64[ns]
df['BUYDATE'] = pd.to_datetime(df['BUYDATE'])

# In ra DataFrame để kiểm tra dữ liệu
print(df.head())

# Tạo DataFrame df_date với cột 'BUYDATE' là chuỗi ngày trong khoảng từ '2018-07-01' đến '2019-06-30'
df_date = pd.DataFrame({'BUYDATE': pd.date_range(start='2018-07-01', end='2019-06-30', freq='D')})

# Chuyển đổi cột 'BUYDATE' thành kiểu datetime64[ns]
df_date['BUYDATE'] = pd.to_datetime(df_date['BUYDATE'])

# vẽ biểu đồ ngày phát sinh đơn hàng 

merged_df = pd.merge(df_date, df, on='BUYDATE', how='left')  # Chọn 'left' để giữ toàn bộ chuỗi ngày

plt.plot(merged_df['BUYDATE'], merged_df['TOTAL_RN'], linestyle='-', color='b', label='Line 1')
plt.xlabel('BUYDATE')
plt.ylabel('TOTAL REVENUE')
plt.title('REVENUE')
plt.xticks(rotation='vertical')
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

# Thêm chú thích nếu có nhiều đường
# Hiển thị lưới
plt.show()
