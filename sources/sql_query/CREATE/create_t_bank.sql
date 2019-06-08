CREATE TABLE t_bank
(
  accountnumber INTEGER NOT NULL,
  creditamount NUMERIC,
  loandebtbalance NUMERIC,
  pastdueloan NUMERIC,
  pastduepercent NUMERIC,
  dpdloan INTEGER,
  dpdpercent INTEGER,
  defaultdateloan TEXT,
  defaultdatepercent TEXT,
  clientid INTEGER,
  office character varying,
  CONSTRAINT key_test PRIMARY KEY (accountnumber)
);