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



# Lọc dữ liệu cho những ngày trong tháng 12/2018
dec_2018_data = merged_df[(merged_df['BUYDATE'].dt.year == 2018) & (merged_df['BUYDATE'].dt.month == 12)]

# In ra dữ liệu
print(dec_2018_data)

# dựa vào dữ liệu này thây được ngày bị thiếu là ngày 25/12/2018 và này là ngày giáng sinh nên các cửa hàng sẽ đóng cửa và có thể kết luận rằng không bị thiếu số liệu nào cả



# vẽ biểu đồ pack-size

plt.bar(df2['SIZE'], df2['SizeCount'], color='skyblue', width = 10, edgecolor = 'black')
plt.xlabel('Size')
plt.ylabel('SizeCount')
plt.title('Bar Chart - Size Buy')
plt.xticks(rotation='vertical')  # Xoay nhãn trục x để dễ đọc
plt.show()


# vẽ biểu đồ propotion of sales
# Tính tổng số doanh số bán hàng
total_sales = df3['TOT_SALES'].sum()

# Tính tỷ lệ phần trăm của doanh số bán hàng của mỗi nhóm so với tổng doanh số bán hàng
df3['Sales_Percentage'] = df3['TOT_SALES'] / total_sales * 100

# Tạo pivot table cho dữ liệu
pivot_df_sale = df3.pivot_table(index='LIFESTAGE', columns='PREMIUM_CUSTOMER', values='Sales_Percentage', aggfunc='sum')

# Vẽ biểu đồ cột chồng
ax = pivot_df_sale.plot(kind='bar', stacked=True)

# Đặt tiêu đề và nhãn
plt.xlabel('Lifestage')
plt.ylabel('Percentage of Total Sales')
plt.title('Stacked Column Chart by Lifestage and Premium Customer')

# Hiển thị phần trăm trên từng cột
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    ax.annotate(f'{height:.1f}%', (x + width / 2, y + height / 2), ha='center', va='center')

# Hiển thị biểu đồ
plt.show()


# vẽ biểu đồ propotion of customers

# Tính số lượng khách hàng duy nhất cho mỗi cặp giá trị của cột LIFESTAGE và PREMIUM_CUSTOMER
unique_customers_per_group = df3.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['LYLTY_CARD_NBR'].nunique().reset_index()

# Tính tổng số lượng khách hàng duy nhất
total_unique_customers = unique_customers_per_group['LYLTY_CARD_NBR'].sum()

# Tạo một cột mới để tính phần trăm lượng khách của mỗi nhóm
unique_customers_per_group['Customer_Percentage'] = (unique_customers_per_group['LYLTY_CARD_NBR'] / total_unique_customers) * 100

# Tạo pivot table cho dữ liệu
pivot_df_cus = unique_customers_per_group.pivot_table(index='LIFESTAGE', columns='PREMIUM_CUSTOMER', values='Customer_Percentage', aggfunc='sum')

# Vẽ biểu đồ cột chồng
ax = pivot_df_cus.plot(kind='bar', stacked=True)

# Đặt tiêu đề và nhãn
plt.xlabel('Lifestage')
plt.ylabel('Percentage of Total Customers')
plt.title('Stacked Column Chart by Lifestage and Premium Customer')

# Hiển thị phần trăm trên từng cột
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    ax.annotate(f'{height:.1f}%', (x + width / 2, y + height / 2), ha='center', va='center')

# Hiển thị biểu đồ
plt.show()


# vẽ biểu đồ Buy per Customer

# Tính tổng số lượng sản phẩm đã mua cho mỗi nhóm
total_products_bought = df3.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['PROD_QTY'].sum().reset_index()

# Tính số lượng khách hàng duy nhất cho mỗi nhóm
unique_customers_per_group = df3.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['LYLTY_CARD_NBR'].nunique().reset_index()

# Tính tỉ lệ mua hàng trung bình cho mỗi nhóm
unique_customers_per_group['Buy_per_customers'] = total_products_bought['PROD_QTY'] / unique_customers_per_group['LYLTY_CARD_NBR']

# Tạo pivot table cho dữ liệu
pivot_df_BPC = unique_customers_per_group.pivot_table(index='LIFESTAGE', columns='PREMIUM_CUSTOMER', values='Buy_per_customers', aggfunc='sum')

# Vẽ biểu đồ cột chồng
ax = pivot_df_BPC.plot(kind='bar', stacked=False)

# Đặt tiêu đề và nhãn
plt.xlabel('Lifestage')
plt.ylabel('Average Products Bought per Customer')
plt.title('Bar Chart by Lifestage and Premium Customer')

# Hiển thị chỉ số trên từng cột

for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    ax.annotate(f'{height:.1f}', (x + width / 2, y + height / 2), ha='center', va='center')

# Hiển thị biểu đồ
plt.show()

# vẽ biểu đồ Price per unit

 #Tính tổng số lượng sản phẩm đã mua cho mỗi nhóm
total_products_bought = df3.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['PROD_QTY'].sum().reset_index()

# Tính tổng doanh số cho mỗi nhóm
total_sales_per_group = df3.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['TOT_SALES'].sum().reset_index()

# Tính giá trung bình cho mỗi sản phẩm
total_products_bought['Price_per_unit'] = total_sales_per_group['TOT_SALES'] / total_products_bought['PROD_QTY']

# Tạo pivot table cho dữ liệu
pivot_df_BPC = total_products_bought.pivot_table(index='LIFESTAGE', columns='PREMIUM_CUSTOMER', values='Price_per_unit', aggfunc='sum')

# Vẽ biểu đồ
ax = pivot_df_BPC.plot(kind='bar', stacked=False)

# Đặt tiêu đề và nhãn
plt.xlabel('Lifestage')
plt.ylabel('Average Products Bought per Customer')
plt.title('Bar Chart by Lifestage and Premium Customer')

# Hiển thị chỉ số trên từng cột
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy() 
    ax.annotate(f'{height:.1f}', (x + width / 2, y + height / 2), ha='center', va='center')

# Hiển thị biểu đồ
plt.show()


