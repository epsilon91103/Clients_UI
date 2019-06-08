SELECT COUNT(DISTINCT T.clientid) as cnt_clients FROM ( 
  SELECT DISTINCT clientid, office, COUNT(clientid), SUM(pastDuePercent) as pct, SUM(pastDueLoan) as od FROM t_bank 
    WHERE loanDebtBalance > 0
    GROUP BY clientid, office 
    HAVING COUNT(clientid) >= ?
    ) as T 
WHERE T.od > 0 or T.pct > 0;
