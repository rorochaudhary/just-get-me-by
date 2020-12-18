import math

#Gets a target percent, a dictionary holding assignment name keys and data in a list   
def algo(target): #(target, assignment_data, group_data):
    target_percent = float(target)
    weight_percent_remaining = float(100.00)
    ungraded_assignments = []

    ###Hard coded test values
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

    #for each assignment group
    for group_id in group_data:
        assignment_list = group_data[str(group_id)] #has the group weight and assignments
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

        #subtract used points if there were graded assignments in the group
        if used_max_points != 0:
            target_percent -= (points / used_max_points) * (used_max_points / max_points * assignment_list[0])
            weight_percent_remaining -= (used_max_points / max_points * assignment_list[0])

        #end condition of grade not possible
        if target_percent > weight_percent_remaining:
            break

    #calculate the scores needed on assignments to get the target grade
    average_percent = float(target_percent / weight_percent_remaining)
    for i in range(0, len(ungraded_assignments) - 1):
        assignment = ungraded_assignments[i]
        assignment_data[assignment][1] = math.ceil(assignment_data[assignment][2] * average_percent)

    #calculate the last score


    ###Check result
    print(assignment_data)

algo(93)