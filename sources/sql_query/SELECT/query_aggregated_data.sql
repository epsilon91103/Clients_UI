        SELECT 'Без просрочки' as period_delay, SUM(loanDebtBalance) as loanDebtBalance, SUM(creditAmount) as creditAmount, SUM(pastDueLoan) as pastDueLoan FROM t_bank
	  WHERE MAX(dpdLoan, dpdPercent) = 0
UNION
	SELECT '1-30' as period_delay, SUM(loanDebtBalance) as loanDebtBalance, SUM(creditAmount) as creditAmount, SUM(pastDueLoan) as pastDueLoan FROM t_bank
	  WHERE MAX(dpdLoan, dpdPercent) between 1 and 30
UNION
	SELECT '31-90' as period_delay, SUM(loanDebtBalance) as loanDebtBalance, SUM(creditAmount) as creditAmount, SUM(pastDueLoan) as pastDueLoan FROM t_bank
	  WHERE MAX(dpdLoan, dpdPercent) between 31 and 90
UNION
	SELECT '91-180' as period_delay, SUM(loanDebtBalance) as loanDebtBalance, SUM(creditAmount) as creditAmount, SUM(pastDueLoan) as pastDueLoan FROM t_bank
	  WHERE MAX(dpdLoan, dpdPercent) between 91 and 180
UNION
	SELECT '181-360' as period_delay, SUM(loanDebtBalance) as loanDebtBalance, SUM(creditAmount) as creditAmount, SUM(pastDueLoan) as pastDueLoan FROM t_bank
	  WHERE MAX(dpdLoan, dpdPercent) between 181 and 360
UNION
	SELECT '360+' as period_delay, SUM(loanDebtBalance) as loanDebtBalance, SUM(creditAmount) as creditAmount, SUM(pastDueLoan) as pastDueLoan FROM t_bank
	  WHERE MAX(dpdLoan, dpdPercent) > 360;