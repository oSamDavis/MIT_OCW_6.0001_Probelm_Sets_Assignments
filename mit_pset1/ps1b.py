# Author : Sam Davis Omekara Jr.

annual_salary = float(input("Enter your annual salary: "))  # annual salary of user
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))  # % of monthly salary to save
total_cost = float(input("Enter the cost of your dream house: "))  # total cost of home
semi_annual_raise = float(input("Enter semi-annual raise, as decimal: "))  # semi-annual raise

portion_down_payment = 0.25  # % of down payment for home
down_payment = portion_down_payment * total_cost  # computing the exact down payment needed
current_savings = 0.0  # current savings of user

number_of_months = 0  # var to hold number of months needed to save. also serves as counter
while current_savings < down_payment:  # while current savings is not up to the down payment
    if number_of_months % 6 == 0 and number_of_months != 0:  # if it's the 6th, 12th, 18th ...
        annual_salary += (semi_annual_raise*annual_salary)  # increasing salary w the raise

    monthly_salary = annual_salary / 12  # monthly salary
    current_savings += (current_savings*4/1200) + (portion_saved*monthly_salary)  # update current savings
    number_of_months += 1  # increase number of months

print("Number of months =", number_of_months)
