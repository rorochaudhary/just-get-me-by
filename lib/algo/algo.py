import math

#returns an empty list on failure and the filled list on success
#Gets a target percent, a dictionary holding assignment name keys with data in a list,
# and a dictionary holding group id keys with the group weight and assignments in the group
def algo(target, assignment_data, group_data) -> dict:
    score_loc = 0
    max_score_loc = 1
    target_percent = float(target)              #user's target grade
    weight_percent_remaining = float(100.00)    #percent that the user can still get
    ungraded_assignments = []                   #list of ungraded assignments
    assignment_weights = {}                     #holds ungraded assignment weights
    current_assignment = 0                      #index of assignment to change the weight for

    #for each assignment group
    for group_id in group_data:
        assignment_list = group_data[group_id] #has the group weight and assignments
        group_weight = assignment_list[0]           #weight of the group
        points = 0                                  #points user has from used_max_points
        used_max_points = 0                         #max points the user can have currently
        max_points = 0                              #total max points in the group

        #iterate through the assignments
        for i in range(1, len(assignment_list)):
            assignment_info = assignment_data[str(assignment_list[i])]
            max_points += assignment_info[max_score_loc]

            #assignment is graded
            if assignment_info[score_loc] != None:
                points += assignment_info[score_loc]
                used_max_points += assignment_info[max_score_loc]

            #ungraded assignments
            else:
                ungraded_assignments.append(assignment_list[i])
                assignment_weights[str(assignment_list[i])] = assignment_info[max_score_loc]

        #change assignment weights
        for i in range(current_assignment, len(ungraded_assignments)):
            assignment_weights[ungraded_assignments[i]] = (assignment_weights[ungraded_assignments[i]] / max_points) * group_weight
            current_assignment += 1

        #subtract used points if there were graded assignments in the group
        if used_max_points != 0:
            target_percent -= (points / used_max_points) * ((used_max_points / max_points) * group_weight)
            weight_percent_remaining -= ((used_max_points / max_points) * group_weight)

        #end condition of grade not possible
        if target_percent > weight_percent_remaining:
            impossible = {}
            return impossible

    #calculate the scores needed on assignments to get the target grade
    if target_percent > 0:
        average_percent = float(target_percent / weight_percent_remaining)
        for i in range(0, len(ungraded_assignments) - 1):
            assignment = ungraded_assignments[i]
            assignment_data[assignment][score_loc] = math.ceil(assignment_data[assignment][max_score_loc] * average_percent)
            target_percent -= (assignment_data[assignment][score_loc] / assignment_data[assignment][max_score_loc]) * assignment_weights[assignment]

            #negative scores error handling
            if assignment_data[assignment][score_loc] < 0:
                assignment_data[assignment][score_loc] = 0

        #calculate last score
        final_assignment = ungraded_assignments[len(ungraded_assignments) - 1]
        assignment_data[final_assignment][score_loc] = (math.ceil(target_percent / assignment_weights[final_assignment]) * assignment_data[final_assignment][max_score_loc])
        #negative scores error handling
        if assignment_data[final_assignment][score_loc] < 0:
            assignment_data[final_assignment][score_loc] = 0
    #change all needed scores to 0
    else:
        for i in ungraded_assignments:
            assignment_data[i][score_loc] = 0

    return assignment_data