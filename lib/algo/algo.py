#Gets a target percent, a dictionary holding assignment name keys and data in a list   
def algo_main(target): #(target, assignment_data, group_data):
    print('Hi there') ###confirm program start
    target_percent = float(target)
    weight_percent_remaining = float(100.00)

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

    #define the dict to hold ungraded assignments
    ungraded_assignments = {}

    ###start algorithm
    #for each assignment grou[]
    for group_id in group_data:
        assignment_list = group_data[str(group_id)] #has the group weight and assignments
        points = 0              #points user has from used_max_points
        used_max_points = 0     #max points the user can have currently
        max_points = 0          #total max points in the group

        #iterate through the assignments
        for i in range(1, len(assignment_list)):
            #assignment is graded
            if assignment_data[str(assignment_list[i])][0] == 1:
                print('GRADED')

            #assignment is not graded
            else:
                print('NOT GRADED')


    print('Bye there') ###confirm program end



algo_main(93)