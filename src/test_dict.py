from CatchRates import catch_rate as rate

while 1:
    try:
        query = raw_input("Enter a Pokemon >> ").strip().lower()
        print "Catch rate of %s is %d" % (query, rate[query])
    except:
        print "Please enter a valid pokemon name."
