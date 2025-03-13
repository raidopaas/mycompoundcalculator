from django.shortcuts import render
from datetime import datetime, date
import calendar
from calc import globals

def calculate_daily_interest(amount, interest_rate):
	interest_year = amount * interest_rate
	interest_day = round(interest_year / 360, 2)
	return interest_day

def generate_day_data(
		annual_rate,
		tax_rate,
		start_day,
		num_of_days, 
		annual_deposit,
		monthly_deposit,
		weekly_deposit,
		additional,
		yearly_deposit_day,
		monthly_deposit_day,
		weekly_deposit_day,
		additional_deposit_day,
		year, 
		month,
		):

	days = []
	interest_payment = 0
	start_day_of_month = calendar.monthrange(year, month)[0]
	weekly_deposit_parameter = (7 - (start_day_of_month - weekly_deposit_day)) if (start_day_of_month > weekly_deposit_day) else (weekly_deposit_day - start_day_of_month)
	accrued_monthly_deposits = 0
	interest = 0
	interest_payment = 0
	received_interest_payment = 0

	for i in range(start_day, num_of_days + 1):

		#fixing the interest for the previous month
		if i == 2:
			globals.collected_interest = globals.accrued_interest
			globals.accrued_interest = 0
		#interest payment
		if i == 5:
			interest_payment = round(globals.collected_interest * (1 - tax_rate), 2)
			received_interest_payment = interest_payment
			globals.total_collected_interest += interest_payment
			globals.total_collected_interest = round(globals.total_collected_interest, 2)
			globals.total_collected_money += interest_payment
			globals.total_collected_money = round(globals.total_collected_money, 2)
		else:
			interest_payment = 0

		interest = calculate_daily_interest(globals.total_collected_money, annual_rate)
		globals.accrued_interest += interest
		globals.accrued_interest = round(globals.accrued_interest, 2)

		deposit = 0
		deposit += globals.initial_amount
		globals.initial_amount = 0
		deposit += monthly_deposit if i == monthly_deposit_day else 0
		deposit += weekly_deposit if (i - 1) % 7 == weekly_deposit_parameter else 0
		deposit += annual_deposit if i == yearly_deposit_day else 0
		deposit += additional if i == additional_deposit_day else 0
		deposit = round(deposit, 2)
		accrued_monthly_deposits += deposit
		accrued_monthly_deposits = round(accrued_monthly_deposits, 2)
		globals.total_collected_money += deposit
		globals.total_collected_money = round(globals.total_collected_money, 2)
		globals.total_deposits += deposit

		days.append({
			"day": i,
			"deposit": deposit,
			"balance": globals.total_collected_money,
			"interest": interest,
			"interest_payment": interest_payment,
			})
	return days, accrued_monthly_deposits, received_interest_payment, globals.total_collected_money, globals.collected_interest

def generate_month_data(
		annual_rate,
		tax_rate,
		current_year,
		start, 
		end,
		start_day,
		end_day,
		final_year,
		annual_deposit, 
		monthly_deposit, 
		weekly_deposit,
		additional,
		yearly_deposit_day,
		yearly_deposit_month,
		monthly_deposit_day, 
		weekly_deposit_day,
		additional_deposit_month,
		additional_deposit_day
		):

	months = []
	for j in range(start, end + 1):
		annual = annual_deposit if j == yearly_deposit_month else 0
		additional_deposit = additional if j == additional_deposit_month else 0
		num_of_days = end_day if final_year and j == end else calendar.monthrange(current_year, j)[1]
		day_data = generate_day_data(
				annual_rate,
				tax_rate,
				start_day,
				num_of_days,
				annual,
				monthly_deposit,
				weekly_deposit,
				additional_deposit,
				yearly_deposit_day,
				monthly_deposit_day, 
				weekly_deposit_day,
				additional_deposit_day,
				current_year, 
				j
				)

		start_day = 1
		
		globals.accrued_yearly_deposits += day_data[1]
		globals.accrued_yearly_deposits = round(globals.accrued_yearly_deposits, 2)
		globals.accrued_interest_payments += day_data[2]
		globals.accrued_interest_payments = round(globals.accrued_interest_payments, 2)

		months.append({
			"month": j,
			"deposits": day_data[1],
			"interest": day_data[2],
			"total_balance": day_data[3],
			"total_interest": day_data[4],
			"days": day_data[0],
		})

	return months

def get_table_data(
		start_amount, 
		annual_rate,
		tax_rate,
		start, 
		end, 
		annual_addition, 
		monthly_addition, 
		weekly_addition,
		additional,
		yearly_deposit_day,
		yearly_deposit_month,
		monthly_deposit_day, 
		weekly_deposit_day,
		additional_date
		):

	date1 = start
	date2 = end
	years = date2.year - date1.year
	start_month = start.month
	end_month = end.month
	start_day = start.day
	end_day = end.day
	final_year = False

	additional_deposit_year = additional_date.year - date1.year
	additional_deposit_month = additional_date.month
	additional_deposit_day = additional_date.day

	globals.initial_amount = start_amount

	return_data = []

	for i in range(years + 1):
		additional_deposit = additional if i == additional_deposit_year else 0
		if i == 0 and years == 0:
			start_month_range = start_month
			end_month_range = end_month
			final_year = True
		elif i == 0 and years > 0:
			start_month_range = start_month
			end_month_range = 12
		elif i == years:
			start_month_range = 1
			end_month_range = end_month
			start_day = 1
			final_year = True
		else:
			start_month_range = 1
			end_month_range = 12
			start_day = 1

		globals.accrued_yearly_deposits = 0
		globals.accrued_interest_payments = 0

		months = generate_month_data(
	 				annual_rate,
	 				tax_rate,
	 				date1.year + i,
	 				start_month_range, 
	 				end_month_range,
	 				start_day,
	 				end_day,
	 				final_year,
	 				annual_addition, 
	 				monthly_addition, 
	 				weekly_addition,
	 				additional_deposit,
	 				yearly_deposit_day,
	 				yearly_deposit_month,
	 				monthly_deposit_day, 
	 				weekly_deposit_day,
	 				additional_deposit_month,
	 				additional_deposit_day
	 				)

		return_data.append({
				"year": date1.year + i,
				"deposits": globals.accrued_yearly_deposits,
				"received_interests": globals.accrued_interest_payments,
				"balance": globals.total_collected_money,
	 			"months": months,
			})

	return return_data
			
def home(request):
	table_data = [{}]
	totals_data = {}

	initial_amount = 0
	interest_rate_percentage = 0
	tax_rate_percentage = 0
	tax_rate = 0
	start_date = date(2025, 1, 16)
	end_date = date(2025, 1, 17)

	yearly_deposit = 0
	monthly_deposit = 0
	weekly_deposit = 0
	additional_deposit = 0
	monthly_deposit_day = 1
	weekly_deposit_day = "Monday"
	weekly_deposit_day_as_nr = 1
	yearly_deposit_day = 1
	yearly_deposit_month = "January"
	yearly_deposit_month_as_nr = 1

	globals.total_deposits = 0
	globals.total_collected_money = 0
	globals.accrued_interest = 0
	globals.total_collected_interest = 0
	globals.collected_interest = 0

	error_message = ""

	if request.method == 'POST':
		try:
			initial_amount = float(request.POST.get('initial_amount', 0) or 0)
			interest_rate_percentage = float(request.POST.get('interest_rate', 0) or 0)
			tax_rate_percentage = float(request.POST.get('tax_rate', 0) or 0)
			start_date_str = str(request.POST.get('start_date', "2025-01-16") or "2025-01-16")
			start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
			end_date_str = str(request.POST.get('end_date', "2025-01-16") or "2025-01-16")
			end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

			#get() with Default Values: Used 0 as a default to handle missing or empty fields.
			#or 0 Fallback: Ensures an empty string is treated as 0.
			weekly_deposit = float(request.POST.get('weekly_deposit', 0) or 0)
			monthly_deposit = float(request.POST.get('monthly_deposit', 0) or 0)
			monthly_deposit_day = int(request.POST.get('monthly_deposit_day', 1) or 1)
			weekly_deposit_day = str(request.POST.get('weekly_deposit_day', "Monday") or "Monday")
			weekly_deposit_day_as_nr = list(calendar.day_name).index(weekly_deposit_day)
			yearly_deposit_day = int(request.POST.get('yearly_deposit_day', 1) or 1)
			yearly_deposit_month = str(request.POST.get('yearly_deposit_month', "January") or "January")
			yearly_deposit_month_as_nr = list(calendar.month_name).index(yearly_deposit_month)
			yearly_deposit = float(request.POST.get('yearly_deposit', 0) or 0)
			additional_deposit = float(request.POST.get('additional_deposit', 0) or 0)
			additional_deposit_date_str = str(request.POST.get('additional_deposit_date'))
			additional_deposit_date = datetime.strptime(additional_deposit_date_str, "%Y-%m-%d").date() if additional_deposit_date_str != "" else ""

			if any(x < 0 for x in [initial_amount, interest_rate_percentage, tax_rate_percentage, weekly_deposit, monthly_deposit, yearly_deposit, additional_deposit]):
			#if initial_amount < 0 or interest_rate_percentage < 0 or weekly_deposit < 0 or monthly_deposit < 0 or yearly_deposit < 0:
				error_message = "Please Provide Correct Input"
			elif start_date >= end_date:
				error_message = "Starting date has to be earlier than end date"
			elif additional_deposit > 0 and additional_deposit_date_str == "":
				error_message = "Please provide a date for additional deposit"
			elif additional_deposit > 0 and (additional_deposit_date < start_date or additional_deposit_date > end_date):
				error_message = "Additional deposit date cannot be outside the investment period"
			else:
				if additional_deposit == 0:
				#a random date for additional deposit date in case additional deposit is left blank
					additional_deposit_date = date(2025, 1, 17)
				
				interest_rate = interest_rate_percentage / 100
				tax_rate = tax_rate_percentage / 100

				table_data = get_table_data(
					initial_amount, 
					interest_rate,
					tax_rate,
					start_date, 
					end_date, 
					yearly_deposit, 
					monthly_deposit, 
					weekly_deposit,
					additional_deposit,
					yearly_deposit_day,
					yearly_deposit_month_as_nr,
					monthly_deposit_day,
					weekly_deposit_day_as_nr,
					additional_deposit_date
					)

		except ValueError:
			error_message = "Please Provide Correct Input"
			return render(request, 'home.html', {
				'error_message': error_message,
			})

	weekdays = {
	
	}

	return render(request, 'home.html', {
		'days': list(range(1, 29)),
		'weekdays':  {
			'Monday': 'Monday',
			'Tuesday': 'Tuesday',
			'Wednesday': 'Wednesday',
			'Thursday': 'Thursday',
			'Friday': 'Friday',
			'Saturday': 'Saturday',
			'Sunday': 'Sunday',
		},
		'months': {
			'January': 'January',
			'February': 'February',
			'March': 'March',
			'April': 'April',
			'May': 'May',
			'June': 'June',
			'July': 'July',
			'August': 'August',
			'September': 'September',
			'October': 'October',
			'November': 'November',
			'December': 'December'
		},
		'monthly_deposit_day': monthly_deposit_day,
		'weekly_deposit_day_as_nr': weekly_deposit_day_as_nr,
		'initial_amount': initial_amount,
		'interest_rate_percentage': interest_rate_percentage,
		'tax_rate_percentage': tax_rate_percentage,
		'start_date': start_date,
		'end_date': end_date,
		'weekly_deposit': weekly_deposit,
		'monthly_deposit': monthly_deposit,
		'yearly_deposit': yearly_deposit,
		'additional_deposit': additional_deposit,
		'table_data': table_data,
		'total_collected': globals.total_collected_money,
		'total_deposits': globals.total_deposits,
		'interest_earned': round(globals.total_collected_money - globals.total_deposits, 2),
		'totals_data': totals_data,
		'final_interest_payment': round(globals.accrued_interest * (1 - tax_rate), 2),
		'error_message': error_message,
	})
