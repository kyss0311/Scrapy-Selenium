/* 查詢股價 */
SELECT * FROM stock_price ORDER BY deal_price DESC NULLS LAST;
/* 查詢股利 */
SELECT * FROM stock_dividend ORDER BY cash_yield DESC NULLS LAST;