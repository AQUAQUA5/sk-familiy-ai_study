SELECT COUNT(*) FROM productlines;
SELECT COUNT(*) FROM products;

SELECT
    a.productCode, a.productName, b.productLine, b.textDescription
FROM
    products a 
INNER JOIN  -- 또는 그냥 JOIN 이라고만 써도 INNER JOIN으로 동작합니다.
    productlines b ON a.productLine = b.productLine;
    
    
SELECT a.employeeNumber, a.lastName, a.firstName, b.phone
FROM employees a
INNER JOIN offices b ON a.officeCode = b.officeCode;

SELECT
priceEach, quantityOrdered, priceEach * quantityOrdered AS total
FROM orderdetails;


 #
SELECT orderDate, d.orderNumber, d.priceEach * d.quantityOrdered AS total
FROM orderdetails AS d 
INNER JOIN orders AS o ON d.orderNumber = o.orderNumber;

#GROUP BY 사용
SELECT o.orderDate
FROM orderdetails AS d 
INNER JOIN orders AS o ON d.orderNumber = o.orderNumber
ORDER BY o.orderDate;

#rollup
SELECT o.orderDate, o.orderNumber
FROM orderdetails AS d 
INNER JOIN orders AS o ON d.orderNumber = o.orderNumber
GROUP BY ROLLUP (o.orderDate, o.orderNumber)
ORDER BY o.orderDate;

#GROUP BY + 집계함수
SELECT o.orderDate, sum(d.priceEach * d.quantityOrdered) AS total
FROM orderdetails AS d 
INNER JOIN orders AS o ON d.orderNumber = o.orderNumber
GROUP BY o.orderDate;

#정렬 
#오름차순 : order by (칼럼)  , order by (칼럼) ASC
#내림차순 : order by (칼럼) DESC 							
SELECT o.orderDate, sum(d.priceEach * d.quantityOrdered) AS total
FROM orderdetails AS d 
INNER JOIN orders AS o ON d.orderNumber = o.orderNumber
GROUP BY o.orderDate
ORDER BY o.orderDate;

#HAVING 적용
SELECT o.orderDate, sum(d.priceEach * d.quantityOrdered) AS total
FROM orderdetails AS d 
INNER JOIN orders AS o ON d.orderNumber = o.orderNumber
GROUP BY o.orderDate
HAVING o.orderDate >='2003-01-31'
ORDER BY o.orderDate;

#구문오류 순서 where에선 select의 별칭을 사용할 수 없음.
#SQL 실행 순서 문제:
#FROM+JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
#근데 또 group by는 select의 별칭 사용 가능
SELECT SUBSTRING(orderDate, 1,4) years , orderdate
FROM orders
WHERE years = '2004';

#연도에 조건 넣기, 서브쿼리
SELECT *
FROM (
	SELECT SUBSTRING(orderDate, 1,4) years , orderdate
	FROM orders ) AS a
WHERE years = '2004';

#연도별 합산
SELECT SUBSTRING(a.orderDate, 1,4) years, SUM(b.quantityOrdered * b.priceEach) total
FROM orders a
LEFT JOIN orderdetails b
ON a.ordernumber = b.ordernumber
GROUP BY years;

#중복값 제거
SELECT orderDate, COUNT(DISTINCT(customerNumber)), COUNT(ordernumber)
FROM orders
GROUP BY orderdate;

#s
SELECT customerNumber, substring(orderdate,1,4), sum(priceEach * quantityOrdered) AS total
FROM orders a
LEFT JOIN orderdetails b
ON a.ordernumber = b.ordernumber
GROUP BY customerNumber, orderdate
ORDER BY customerNumber;

#- 인당 매출액(연도별) 
#년도, 고객수, 매출액 
SELECT SUBSTRING(a.orderDate, 1,4) years, COUNT(DISTINCT(customernumber)) 고객수,
 SUM( b.quantityOrdered * b.priceEach) total ,
 SUM( b.quantityOrdered * b.priceEach) / COUNT(DISTINCT(customernumber)) 인당평균구매금액
FROM orders a 
LEFT JOIN orderdetails b 
ON a.ordernumber = b.orderNumber
GROUP BY years;

#
SELECT *
FROM orders a
LEFT JOIN orderdetails b
ON a.ordernumber = b.ordernumber
LEFT JOIN customers c
ON a.customerNumber = c.customerNumber;

#나라, 도시, 구매입금
SELECT c.country, c.city, SUM(priceEach * quantityOrdered) AS TOTAL
FROM orders a
LEFT JOIN orderdetails b
ON a.ordernumber = b.ordernumber
LEFT JOIN customers c
ON a.customerNumber = c.customerNumber
GROUP BY c.country, c.city
ORDER BY c.country;

SELECT c.country, c.city 
FROM orders a
LEFT JOIN orderdetails b
ON a.ordernumber = b.ordernumber
LEFT JOIN customers c
ON a.customerNumber = c.customerNumber
GROUP BY c.country, c.city
ORDER BY c.country;

#usa, canada만 반환
SELECT *
FROM customers
where customers.country = 'USA' OR 'Canada';

SELECT *
FROM customers
where country IN ('USA', 'CANADA');

SELECT country, CASE WHEN COUNTRY IN ('USA', 'CANADA') then '북미' ELSE '기타' END 지역
FROM customers;



#북미, 기타 판매 금액 비교
SELECT CASE WHEN c.country IN ('USA', 'CANADA') then '북미' ELSE '기타' END as continent , sum(b.priceEach*b.quantityordered)
FROM orders a
LEFT JOIN orderdetails b
ON a.ordernumber = b.ordernumber
LEFT JOIN customers c
ON a.customerNumber = c.customerNumber
GROUP BY continent;

SELECT * FROM sk17.naver_day_stock ORDER BY st_date DESC LIMIT 5;

SELECT st_code, st_date, st_high, st_low, st_close, st_trade 거래금액  FROM sk17.naver_day_stock WHERE st_date = '2025-05-29';

SELECT CONCAT('A', isu_srt_cd)
FROM sk17.st_master LIMIT 5;

CREATE VIEW master_code AS 
SELECT CONCAT('A',isu_srt_cd) st_code, isu_abbrv, list_dd, mkt_tp_nm, ist_shrs FROM sk17.st_master;

CREATE table master_code2 AS 
SELECT CONCAT('A',isu_srt_cd) st_code, isu_abbrv, list_dd, mkt_tp_nm, ist_shrs FROM sk17.st_master;

SELECT *
FROM master_code;

#5월29일에 거래금액이 제일 많은 주식 출력
SELECT isu_abbrv, 거래금액, 
DENSE_RANK() OVER(ORDER BY 거래금액 DESC) 랭킹
FROM (SELECT A.st_code, A.st_date, A.st_open, A.st_high, A.st_low, A.st_close,
 A.st_close * A.st_trade 거래금액, B.isu_abbrv
FROM sk17.naver_day_stock A
INNER JOIN master_code2 B
ON A.st_code = B.st_code
WHERE A.st_date = '2025-05-29')d;


ALTER TABLE master_code2 CONVERT TO CHARACTER SET UTF8;


SELECT A.st_code, A.st_date, A.st_open, A.st_high, A.st_low, A.st_close,
 A.st_close * A.st_trade 거래금액, B.isu_abbrv
FROM sk17.naver_day_stock A
INNER JOIN master_code2 B
ON A.st_code = B.st_code
WHERE A.st_date = '2025-05-29'
ORDER BY 거래금액 DESC LIMIT 5;


SELECT customernumber, max_date, '2005-06-01', DATEDIFF('2005-06-01', max_date) diff
FROM
(SELECT customernumber, MAX(orderdate) max_date
FROM orders
GROUP BY 1) AS d;

(SELECT customernumber, MAX(orderdate) max_date
FROM orders
GROUP BY 1);



SELECT A.st_code, A.st_date, A.st_open, A.st_high, A.st_low, A.st_close,
 A.st_close * A.st_trade 거래금액, B.isu_abbrv
FROM sk17.naver_day_stock A
INNER JOIN master_code2 B
ON A.st_code = B.st_code
WHERE A.st_date = '2025-05-29';



SELECT A.st_code, A.st_date, A.st_open, A.st_high, A.st_low, A.st_close,
 A.st_close * A.st_trade 거래금액, B.isu_abbrv
FROM sk17.naver_day_stock A
INNER JOIN master_code2 B
ON A.st_code = B.st_code
WHERE A.st_date = '2025-05-29'
ORDER BY 거래금액 DESC LIMIT 5;



SELECT isu_abbrv, 거래금액, 
DENSE_RANK() OVER(ORDER BY 거래금액 DESC) 랭킹
FROM (SELECT A.st_code, A.st_date, A.st_open, A.st_high, A.st_low, A.st_close,
 A.st_close * A.st_trade 거래금액, B.isu_abbrv
FROM sk17.naver_day_stock A
INNER JOIN master_code2 B
ON A.st_code = B.st_code
WHERE A.st_date = '2025-05-29') d




나라별 판매금액 랭킹 


SELECT country, total, 
RANK() OVER( ORDER BY total DESC) ranking 
FROM 
(SELECT  C.country, round(sum(B.priceEach * B.quantityOrdered)) AS total
FROM orders A 
LEFT JOIN orderdetails B 
ON A.orderNumber = B.orderNumber
LEFT JOIN customers C 
ON A.customerNumber = C.customerNumber
GROUP BY 1) D



SELECT customernumber, max_date, '2005-06-01', DATEDIFF('2005-06-01',max_date) diff 
FROM 
(SELECT customernumber, MAX(orderdate) max_date
FROM orders 
GROUP BY 1) AS D



SELECT *, case when diff >= 90 then '위험' ELSE '정상' END customer_type
FROM 
(
SELECT customernumber, max_date, '2005-06-01', DATEDIFF('2005-06-01',max_date) diff 
FROM 
(SELECT customernumber, MAX(orderdate) max_date
FROM orders 
GROUP BY 1) AS D ) AS E 



SELECT customer_type, COUNT(DISTINCT(customernumber)) 집계
FROM 
(SELECT *, case when diff >= 90 then '위험' ELSE '정상' END customer_type
FROM 
(
SELECT customernumber, max_date, '2005-06-01', DATEDIFF('2005-06-01',max_date) diff 
FROM 
(SELECT customernumber, MAX(orderdate) max_date
FROM orders 
GROUP BY 1) AS D ) AS E ) AS F
GROUP BY customer_type;




