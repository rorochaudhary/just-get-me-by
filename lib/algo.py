import math
import copy

#returns an {'error'}: 'messagee'} on failure and the filled list on success
#Gets a target percent, a dictionary holding assignment name keys with data in a list,
# and a dictionary holding group id keys with the group weight and assignments in the group
def calculate_min_grades(target: float, assignment: list, group_data: list) -> dict:
    assignment_data = copy.deepcopy(assignment)
    score_loc = 0
    max_score_loc = 1
    target_percent = float(target)              #user's target grade
    weight_percent_remaining = float(100.00)    #percent that the user can still get
    ungraded_assignments = []                   #list of ungraded assignments
    assignment_weights = {}                     #holds ungraded assignment weights
    current_assignment = 0                      #index of assignment to change the weight for

    #empty assignment data
    if not assignment_data:
        return {'error': "No assignments found"}

    #empty group data
    if not group_data:
        return {'error': "No group data found"}

    #invalid target
    if target_percent < 0 or target_percent > 100:
        return {'error': "Target percent not in range 0-100"}

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

            #use assignment if it is worth points
            if assignment_info[max_score_loc] != None:
                max_points += assignment_info[max_score_loc]

                #assignment is graded
                if assignment_info[score_loc] != None:
                    points += assignment_info[score_loc]
                    used_max_points += assignment_info[max_score_loc]

                #ungraded assignments
                else:
                    ungraded_assignments.append(assignment_list[i])
                    assignment_weights[str(assignment_list[i])] = assignment_info[max_score_loc]

        #Calculate assignment weights / 100
        for i in range(current_assignment, len(ungraded_assignments)):
            #calculate if assignment is worth points
            if max_points != 0:
                assignment_weights[ungraded_assignments[i]] = (assignment_weights[ungraded_assignments[i]] / max_points) * group_weight
                current_assignment += 1

        #subtract used points if there were graded assignments in the group
        if used_max_points != 0 and max_points != 0:
            target_percent -= (points / used_max_points) * ((used_max_points / max_points) * group_weight)
            weight_percent_remaining -= ((used_max_points / max_points) * group_weight)

        #end condition of grade not possible
        if target_percent > weight_percent_remaining:
            return {'error': "Impossible grade"}

    #calculate the scores needed on assignments to get the target grade
    if target_percent > 0:
        average_percent = float(target_percent / weight_percent_remaining)
        for i in range(0, len(ungraded_assignments) - 1):
            assignment = ungraded_assignments[i]
            assignment_data[assignment][score_loc] = float(math.ceil(assignment_data[assignment][max_score_loc] * average_percent))

            #calculate weight gain if score has weight
            if assignment_data[assignment][max_score_loc] != 0:
                target_percent -= (assignment_data[assignment][score_loc] / assignment_data[assignment][max_score_loc]) * assignment_weights[assignment]
                weight_percent_remaining -= assignment_weights[assignment]

            #negative scores error handling
            if assignment_data[assignment][score_loc] < 0:
                assignment_data[assignment][score_loc] = 0

        #calculate last score
        if len(ungraded_assignments) > 0:
            final_assignment = ungraded_assignments[len(ungraded_assignments) - 1]
            #score has weight
            if assignment_weights[final_assignment] != 0:
                assignment_data[final_assignment][score_loc] = float(math.ceil((target_percent / assignment_weights[final_assignment]) * assignment_data[final_assignment][max_score_loc]))
                weight_percent_remaining -= assignment_weights[final_assignment]
            else:
                assignment_data[final_assignment][score_loc] = 0

            #negative scores error handling
            if assignment_data[final_assignment][score_loc] < 0:
                assignment_data[final_assignment][score_loc] = 0

        #error handle weights not adding up to 100
        if weight_percent_remaining != 0:
            return {'error': "Group weights don't add up to 100"}

    #change all needed scores to 0
    else:
        for i in ungraded_assignments:
            assignment_data[i][score_loc] = 0

    return assignment_data
