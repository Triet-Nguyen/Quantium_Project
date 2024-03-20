
/* chỉnh lại kiểu dữ liệu Cột date */
SELECT CONVERT(DATE, DATEADD(day, date-2, '1900-01-01')) AS BUYDATE, 
		STORE_NBR,
		LYLTY_CARD_NBR,
		TXN_ID,
		PROD_NBR,
		PROD_NAME,
		PROD_QTY,
		TOT_SALES
INTO TABLEFIXDATE
FROM [Quantium].[dbo].[transactions]


select BUYDATE, COUNT(BUYDATE)
from TABLEFIXDAY
GROUP BY BUYDATE
ORDER BY BUYDATE;


/* lọc cột PROD_NAME loại bỏ sản phẩm không phải là chips */

CREATE TABLE NewTable (
    Cleaned_PROD_NAME NVARCHAR(MAX)
);

INSERT INTO NewTable (Cleaned_PROD_NAME)
SELECT REPLACE(REPLACE(table2.word, ' ', ''), '0', '') AS Cleaned_PROD_NAME
FROM (
    SELECT value as word
    FROM (
        SELECT PROD_NAME, COUNT(PROD_NAME) AS NameCount
        FROM TABLEFIXDATE
        GROUP BY PROD_NAME
    ) AS table1
    CROSS APPLY STRING_SPLIT(table1.PROD_NAME, ' ')
) as table2
WHERE PATINDEX('%[0-9 ]%', table2.word) = 0;

DELETE FROM NewTable
WHERE LTRIM(RTRIM(Cleaned_PROD_NAME)) = '';

DELETE FROM NewTable
WHERE Cleaned_PROD_NAME = 'Salsa';

DELETE FROM TABLEFIXDATE
WHERE PROD_NAME LIKE '%salsa%';

select Cleaned_PROD_NAME, count(Cleaned_PROD_NAME) as soluong
from NewTable
WHERE PATINDEX('%[^A-Za-z]%', Cleaned_PROD_NAME) = 0
group by Cleaned_PROD_NAME
order by soluong desc

/* LỌC DỮ LIỆU CỘT PROD_QTY */

select PROD_QTY, count(PROD_QTY) as Tong_so_lan
from TABLEFIXDATE
group by PROD_QTY
order by PROD_QTY


select *
from TABLEFIXDATE
where PROD_QTY = '200'

DELETE FROM TABLEFIXDATE
WHERE PROD_QTY = '200';

/* loại bỏ dữ liệu PROD_QTY = 200 vì khách hàng mua số lượng lớn và chỉ phát sinh 2 đơn trong 2 năm có thể là mua vì mục đích thương mại không đem lại lợi ích cho việc phân tích */

select *
from TABLEFIXDATE
order by DATE

select BUYDATE,SUM(PROD_QTY) AS TOTAL_QTY, CONVERT(DECIMAL(18,1), SUM(TOT_SALES)) AS TOTAL_RN
INTO REVENUE
from TABLEFIXDATE
GROUP BY BUYDATE
ORDER BY BUYDATE

select *
from REVENUE
ORDER BUYDATE

/* tách dữ liệu size ra thành một cột riêng */

Create function UDF_ExtractNumbers
(  
  @input varchar(255)  
)  
Returns varchar(255)  
As  
Begin  
  Declare @alphabetIndex int = Patindex('%[^0-9]%', @input)  
  Begin  
    While @alphabetIndex > 0  
    Begin  
      Set @input = Stuff(@input, @alphabetIndex, 1, '' )  
      Set @alphabetIndex = Patindex('%[^0-9]%', @input )  
    End  
  End  
  Return @input
End
go

SELECT CONVERT(INT, dbo.UDF_ExtractNumbers(PROD_NAME)) AS SIZE, COUNT(CONVERT(INT, dbo.UDF_ExtractNumbers(PROD_NAME))) AS SizeCount
INTO SIZEBUY
FROM dbo.TABLEFIXDATE
GROUP BY CONVERT(INT, dbo.UDF_ExtractNumbers(PROD_NAME))
ORDER BY CONVERT(INT, dbo.UDF_ExtractNumbers(PROD_NAME));

 
/* lấy tên thương hiêu bằng cách lọc lấy chữ đầu tiên của chuỗi */


SELECT 
    LEFT(PROD_NAME, CHARINDEX(' ', PROD_NAME + ' ') - 1) AS BRAND
into BRAND
FROM 
    dbo.TABLEFIXDATE

UPDATE dbo.BRAND1
SET BRAND = 
    CASE
        WHEN BRAND LIKE '%RED%' THEN REPLACE(BRAND, 'RED', 'RRD')
        WHEN BRAND LIKE '%SNBTS%' THEN REPLACE(BRAND, 'SNBTS', 'SUNBITES')
        WHEN BRAND LIKE '%INFZNS%' THEN REPLACE(BRAND, 'INFZNS', 'INFUZIONS')
        WHEN BRAND LIKE '%WW%' THEN REPLACE(BRAND, 'WW', 'WOOLWORTHS')
        WHEN BRAND LIKE '%SMITHS%' THEN REPLACE(BRAND, 'SMITHS', 'SMITH')
        WHEN BRAND LIKE '%NCC%' THEN REPLACE(BRAND, 'NCC', 'NATURAL')
        WHEN BRAND LIKE '%DORITOS%' THEN REPLACE(BRAND, 'DORITOS', 'DORITO')
        WHEN BRAND LIKE '%GRAIN%' THEN REPLACE(BRAND, 'GRAIN', 'GRNWVES')
        ELSE BRAND
    END;

select BRAND, Count(BRAND) as QTY
from dbo.BRAND
group by BRAND
order by QTY desc


/* merge hai bảng transaction và behavior lại */

select BUYDATE,STORE_NBR, TB.LYLTY_CARD_NBR,TXN_ID,PROD_NBR, PROD_NAME, PROD_QTY, TOT_SALES, LIFESTAGE, PREMIUM_CUSTOMER
into TOTALDATA
from dbo.TABLEFIXDATE as TB
inner join dbo.PBEHAVIOUR as PB
on TB.LYLTY_CARD_NBR = PB.LYLTY_CARD_NBR
order by BUYDATE

/* lọc null cột Lifestage, premium customer */

select *
from TOTALDATA
where LIFESTAGE is null;

select *
from TOTALDATA
where PREMIUM_CUSTOMER is null;


/* lọc lấy bảng pack-size */

SELECT 
  LIFESTAGE, 
  PREMIUM_CUSTOMER, 
  ROUND(SUM(TOT_SALES) / (SELECT SUM(TOT_SALES) FROM TOTALDATA) *100 , 1) AS PER
INTO PRO_SALE
FROM 
  TOTALDATA
GROUP BY 
  LIFESTAGE, 
  PREMIUM_CUSTOMER

order by lifestage








