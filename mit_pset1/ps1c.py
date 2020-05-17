# Author : Sam Davis Omekara Jr.

annual_salary = float(input("Enter your starting salary: "))  # annual salary of user

total_cost = 1000000  # total cost of home
semi_annual_raise = 0.07  # semi-annual raise

down_payment = 0.25 * total_cost  # computing the exact down payment needed

current_savings = 0.0  # current savings of user

epsilon = 100  # variables for bisection search
low = 0
high = 10000
portion_saved = (low + high) / 2.0  # % of monthly salary to save

number_of_months = 0  # var to hold number of months needed to save. also serves as counter
bisection_searches = 0  # var to hold number of bisection searches

while abs(current_savings - down_payment) >= epsilon and bisection_searches <= 13:  # log 10000 is a bit greater than 13
    current_savings = 0.0  # reset current savings
    reset_annual_salary = annual_salary  # resetting the annual salary for use in the "for loop"

    for number_of_months in range(36):  # using the for loop to calculate the current savings for 3 years i.e 36 months
        if number_of_months % 6 == 0 and number_of_months != 0:  # if it's the 6th, 12th, 18th ...
            reset_annual_salary += (semi_annual_raise * reset_annual_salary)  # increasing annual salary w the raise
        monthly_salary = reset_annual_salary / 12.0  # monthly salary
        current_savings += (current_savings * 4 / 1200) +\
                           (portion_saved * monthly_salary) / 10000.0  # update current savings

    if current_savings < down_payment:  # binary / bisection search begins
        low = portion_saved
    else:
        high = portion_saved
    portion_saved = (low + high) / 2.0
    bisection_searches += 1

if bisection_searches > 13:  # if it took more than 13 bisection searches i.e log10000 , then ...
    print("Cannot afford house in 3 years")
else:
    print("Portion Saved = ", portion_saved/10000)
