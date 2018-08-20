		'''
		#Definition of the student id. Temporarily it is a surrogate key.
		student_id_in = '1'
		register_student = True
		read_prob = True
		read_student = True
		#TO DO: This will be an input from the URL.
		#Definition of the topic and problem name. These two attributes define the problem.
		problem_name='Problem 13'
		topic_id='EQ-LINE'

		#This array will temporaly save the student answer for a given step.
		student_ans=[]
		#TO DO: All the input from the student will be saved into a .txt file. 

		if request.is_ajax() and request.method == 'POST':

			print ('\n \n hola process \n \n')

			#TO DO: Define this as a method.
			if register_student == True:
				try:
					#check if the user exists.
					Student.objects.get(id=student_id_in)
				except:
					return HttpResponse('The user does not exist.')

			#TO DO: Define this as a method.
			#Probably I can check this with a method directly inside the model? the form?
			if read_prob == True:
				try:
					problem_in = Problem.objects.get(topic_id=topic_id_in,problem_name=problem_name)
				except:
					return HttpResponse('The problem has not been created.')






			#Read the student answer. This should be the only part that goes into the process method itself.
			if read_student == True:
				step_num = jsaon.loads(request.POST['step_number'])
				student_ans_temp = json.loads(request.POST['student_answer'])

				#Check if the student wrote more than one substep in one line. 
				#The substep must be separated by an = sign. 
				#TO DO: what if the substep does not have an = sign?
				for i in range(len(student_ans_temp)):
					student_ans_temp2 = student_ans_temp[i].split('=')
					if len(student_ans_temp2) > 2:
						for i in range(1,len(student_ans_temp2)):
							student_ans.append(student_ans_temp2[0] + '=' + student_ans_temp2[i])
					else:
						student_ans = student_ans_temp

				#Read the step from the database. Based on this it will check on the 
				#substeps and the respective error messages.

				step_n = 'Step' + ' ' + str(step_num)
				
				try:
					step_in = Step.objects.get(problem_id=problem_in,step_name=step_n)
				except:
					return HttpResponse('The step has not been created yet.')

				# Validate the student problem info. Create the problem if it does not exists yet.
				# The number of tries will not be modified yet. It is modified at the end of the prpblem, 
				# when the student has succesfully solved the problem, or at every step.
				# TO DO: Check the definition of a wrong answer. Should it be per step or how?

				try:
					student_prob = StudentProblem.objects.get(student_id=student_id_in,problem_id=problem_in)
				except:
					StudentProblem.objects.create(
						student_id=student_id_in,
						problem_id=problem_in,
						answer_file='file path',
					)
					student_prob = StudentProblem.objects.get(student_id=student_id_in,problem_id=problem_in)

				#Read or create the step db realted with the student. 
				try:
					student_step = StudentStep.objects.get(problem_student_id=problem_in,step_student_id=step_in)
					student_step.number_of_substeps = len(student_ans)
				except:
					StudentStep.objects.create(
						problem_student_id=problem_in,
						step_student_id=step_in,
						number_of_substeps = len(student_ans),
						)
					student_step = StudentStep.objects.get(problem_student_id=problem_in,step_student_id=step_in)


				for j in range(student_step.number_of_substeps):
					data_est = student_ans[j]
					for l in range(step_in.number_of_substeps):
 						substep_name_in = 'Substep' + ' ' + str(j)
 						
 						try:
 							data_sol = Substep.object.get(step_id=step_in,substep_name=substep_name_in)
 						except:
 							return HttpResponse('The substep has not been created yet.')

 						for s in ['\\left','\\right']:
 							data_est_sim = data_est[i].replace(s,'')
 							data_sol_sim = data_sol.answer.replace(s,'')

 						data_est_sympy=process_sympy(data_est_sim)
 						data_sol_sympy=process_sympy(data_sol_sim)

 						data_sol_sympy=str(data_sol_sympy).replace('{1}','1')
 						data_sol_sympy=sympy.simplify(data_sol_sympy.replace('{2}','2'))

 						data_est_sympy=str(data_est_sympy).replace('{1}','1')
 						data_est_sympy=sympy.simplify(data_est_sympy.replace('{2}','2'))

 						data_sim=sympy.simplify(data_est_sympy-data_sol_sympy)

 						if data_sim == 0:
 							student_step.succesful_attemps = student_step.succesful_attemps + 1
 							data = True
 							break

 						elif data_sim != 0:
 							student_step.fail_attemps = student_step.fail_attemps + 1
 							data = False
 							i_temp = i

 				#datax = json.dumps(data)
 				#print ("Hola, hiciste un ajax? ")
 			'''
			