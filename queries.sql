
.print 
SELECT DISTINCT(waste_type) COUNT(s1.service_no), SUM(s1.internal_cost),SUM(s1.price),COUNT(s1.waste_type) FROM accounts a, account_managers m, service_agreements s1 WHERE a.customer_name = 'Rhianna Wilkinson', WHERE ;