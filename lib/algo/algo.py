import math

#returns an empty list on failure and the filled list on success
#Gets a target percent, a dictionary holding assignment name keys with data in a list,
# and a dictionary holding group id keys with the group weight and assignments in the group
def algo(target, assignment_data, group_data) -> dict:
    target_percent = float(target)              #user's target grade
    weight_percent_remaining = float(100.00)    #percent that the user can still get
    ungraded_assignments = []                   #list of ungraded assignments
    assignment_weights = {}                     #holds ungraded assignment weights
    current_assignment = 0                      #index of assignment to change the weight for

    #for each assignment group
    for group_id in group_data:
        assignment_list = group_data[str(group_id)] #has the group weight and assignments
        group_weight = assignment_list[0]
        points = 0              #points user has from used_max_points
        used_max_points = 0     #max points the user can have currently
        max_points = 0          #total max points in the group

        #iterate through the assignments
        for i in range(1, len(assignment_list)):
            assignment_info = assignment_data[str(assignment_list[i])]
            max_points += assignment_info[2]

            #assignment is graded
            if assignment_info[0] == 1:
                points += assignment_info[1]
                used_max_points += assignment_info[2]

            #ungraded assignments
            else:
                ungraded_assignments.append(assignment_list[i])
                assignment_weights[str(assignment_list[i])] = assignment_info[2]

        #change assignment weights
        for i in range(current_assignment, len(ungraded_assignments)):
            assignment_weights[ungraded_assignments[i]] = assignment_weights[ungraded_assignments[i]] / max_points * group_weight
            current_assignment += 1

        #subtract used points if there were graded assignments in the group
        if used_max_points != 0:
            target_percent -= (points / used_max_points) * (used_max_points / max_points * group_weight)
            weight_percent_remaining -= (used_max_points / max_points * group_weight)

        #end condition of grade not possible
        if target_percent > weight_percent_remaining:
            impossible = {}
            return impossible

    #calculate the scores needed on assignments to get the target grade
    average_percent = float(target_percent / weight_percent_remaining)
    for i in range(0, len(ungraded_assignments) - 1):
        assignment = ungraded_assignments[i]
        assignment_data[assignment][1] = math.ceil(assignment_data[assignment][2] * average_percent)
        target_percent -= assignment_data[assignment][1] / assignment_data[assignment][2] * assignment_weights[assignment]

        #negative scores error handling
        if assignment_data[assignment][1] < 0:
            assignment_data[assignment][1] = 0

    #calculate last score
    final_assignment = ungraded_assignments[len(ungraded_assignments) - 1]
    assignment_data[final_assignment][1] = math.ceil(target_percent / assignment_weights[final_assignment] * assignment_data[final_assignment][2])
    #negative scores error handling
    if assignment_data[final_assignment][1] < 0:
        assignment_data[final_assignment][1] = 0

    return assignment_data

###Hard coded test case
assignment_data = {
    'A1': [1, 17, 20],
    'A2': [1, 18, 20],
    'A3': [0, -1, 20],
    'A4': [0, -1, 25],
    'midterm': [1, 43, 50],
    'final': [0, -1, 100]
}
group_data = {
    '1': [50, "A1", "A2", "A3", "A4"],
    '2': [15, "midterm"],
    '3': [35, "final"]
}

#Written test case
results = algo(93, assignment_data, group_data)
print('\n~RESULTS~')
print('GOAL: 93')
for key, value in results.items():
    print(key, value)
print()

#random test case
results = algo(75, assignment_data, group_data)
print('\n~RESULTS~')
print('GOAL: 75')
for key, value in results.items():
    print(key, value)
print()

#random test case
results = algo(34, assignment_data, group_data)
print('\n~RESULTS~')
print('GOAL: 34')
for key, value in results.items():
    print(key, value)
print()

#random test case
results = algo(20, assignment_data, group_data)
print('\n~RESULTS~')
print('GOAL: 20')
for key, value in results.items():
    print(key, value)
print()