SELECT COUNT(clientid) as cnt_clients FROM ( 
  SELECT clientid, COUNT(clientid) FROM t_bank
  WHERE loanDebtBalance > 0
  GROUP BY clientid 
HAVING COUNT(clientid) >= ?) as T;
