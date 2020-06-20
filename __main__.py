import os
import sys
import csv
from collections import namedtuple, Counter

Plan = namedtuple('Plan', 'amount validity per_day_data additional_data fup')

jio_plans_source = sys.argv[1]
if not os.path.exists(jio_plans_source):
    print 'File not found --\n\t%s' % jio_plans_source
    sys.exit(1)

def msg(message, depth=0):
    print '\t' * depth, message

def print_plans(plans):
    print '{0:^8} {1:^10} {2:^12} {3:^15} {4:^7}'.format('Amount', 'Validity', \
         'Per Day Data', 'Additional Data', 'FUP')
    for plan in plans:
        print '{0:^8} {1:^10} {2:^12} {3:^15} {4:^7}'.format(plan.amount, plan.validity, \
            plan.per_day_data, plan.additional_data, plan.fup)

def calculate_efficient_plan(plans):
    result = {'data_ratio': None, 'validity_ratio': None, 'fup_ratio': None}
    max_data_ratio, max_validity_ratio, max_fup_ratio = 0, 0, 0
    for plan in plans:
        total_data = plan.per_day_data * plan.validity + plan.additional_data
        amount = plan.amount
        
        data_ratio = total_data/amount
        validity_ratio = plan.validity/amount
        fup_ratio = plan.fup/amount

        if data_ratio > max_data_ratio:
            max_data_ratio = data_ratio
            result['data_ratio'] = plan
        if validity_ratio > max_validity_ratio:
            max_validity_ratio = validity_ratio
            result['validity_ratio'] = plan
        if fup_ratio > max_fup_ratio:
            max_fup_ratio = fup_ratio
            result['fup_ratio'] = plan

    counter = Counter(result)
    return counter.most_common(1)

jio_plans = list()
with open(jio_plans_source, 'rb') as file:
    reader = csv.reader(file)
    for i, line in enumerate(reader):
        if i == 0: continue
        amount = float(line[0]); validity = int(line[1]); per_day_data = float(line[2])
        additional_data = float(line[3])
        fup = int(line[4])
        plan = Plan(amount, validity, per_day_data, additional_data, fup)
        jio_plans.append(plan)
jio_plans.sort(key=lambda x: x.amount)

msg('Total Plans : %d\nPlans are as folows :' % len(jio_plans))
print_plans(jio_plans)
most_efficient_plan = calculate_efficient_plan(jio_plans)
msg('The most efficient plan is ---\n\t%s' % most_efficient_plan)

