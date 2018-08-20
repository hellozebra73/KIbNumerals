from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import Template, Context
from django.template.context_processors import csrf
#from django.views import View
from django.views.generic import View
from django.core import serializers

import json

from opp.models import *

# sympy
import sys,os
import sympy
from sympy.abc import x, y, z, a, b, c, f, t, k, n
from sympy import Eq, simplify, exp, cos, sin, Ne

from latex2sympy.process_latex import process_sympy

def index(request):
	return render(request, 'index.html')

#NOTE: Generic views is an option to call the DB form the template.

class ProblemConstructor:
    def __init__(self, topic_id_in, problem_name_in):
    	#Call to the db Problem.
    	try:
    		self.prob_in = Problem.objects.get(topic_id=topic_id_in,problem_name=problem_name_in)
    	except:
    		self.prob_in = 'None'
    #check if the problem exists.
    def ProblemExist(self):
    	if self.prob_in == 'None':
    		return HttpResponse('The problem does not exist.')
    	else:
    		return self.prob_in

class ProblemNumeralConstructor:
	#Here problem id is the object of the problem NOT just the id.
    def __init__(self, problem_id_in = 'None', numeral_number_in = 'None'):
    	#Call to the db ProblemNumeral.
    	try:
    		if problem_id_in != 'None' and numeral_number_in == 'None':
    			self.prob_num_in = ProblemNumeral.objects.filter(problem_id=problem_id_in)
    		elif problem_id_in == 'None' and numeral_number_in != 'None':
    			self.prob_num_in = ProblemNumeral.objects.filter(numeral_number=numeral_number_in)
    		elif problem_id_in != 'None' and numeral_number_in != 'None':
    			self.prob_num_in = ProblemNumeral.objects.get(problem_id=problem_id_in, numeral_number=numeral_number_in)
    	except:
    		self.prob_num_in = 'None'
    def ProblemNumeralExist(self):
    	if self.prob_num_in == 'None':
    		return HttpResponse('The problem numeral does not exist.')
    	else:
    		return self.prob_num_in

class StepConstructor:
    def __init__(self, s_number = 'None', prob_num_in = 'None'):
    	try:
    		if s_number != 'None' and prob_num_in == 'None':
    			self.step_base = Step.objects.filter(step_number=s_number)
    		elif s_number == 'None' and prob_num_in != 'None':
    			self.step_base = Step.objects.filter(problem_num_id=prob_num_in)
    		elif s_number != 'None' and prob_num_in != 'None':
    			self.step_base = Step.objects.get(step_number=s_number, problem_num_id=prob_num_in)
    	except:
    		self.step_base = 'None'
    def StepExist(self):
    	if self.step_base == 'None':
    		return HttpResponse('The step does not exist.')
    	else:
    		return self.step_base

class SubstepConstructor:
    def __init__(self, s_id, sub_name):
    	try:
    		self.substep_base=Substep.objects.get(step_id=s_id,substep_name=sub_name)
    	except:
    		self.substep_base = 'None'
    #check if the step exists.
    def SubstepExist(self):
    	if self.substep_base == 'None':
    		return HttpResponse('The substep does not exist.')
    	else:
    		return self.substep_base

class SymbolConstructor:
	#TO DO: Define this automatically from the beginning of the problem.
	#Database with symbols based on the problems???
	def __init__(self,symbols):
		self.symbol = []
		for symbol in symbols:
			self.symbol.append(sympy.Symbol(symbol))

class StudentConstructor:
	#Definition of the student id. Temporarily it is a surrogate key.
	#TO DO: Define this as a method. This must go on the login part. We could do it as a form meanwhile.
	def __init__(self,student_id_in):
		self.student_id = student_id_in
		try:
			self.student_cons = Student.objects.get(id=self.student_id)
		except:
			self.student_cons = 'None'
	#check if the user exists.
	def StudentExist(self):
		if self.student_cons == 'None':
			return HttpResponse('The substep does not exist.')
		else:
			return self.student_cons

class CleanStudentAns:
	def __init__(self,student_ans_in):
		self.data_st = []
		for i in range(len(student_ans_in)):
			student_ans_2 = student_ans_in[i].split('=')
			if len(student_ans_2) > 2:
				for i in range(1,len(student_ans_2)):
					self.data_st.append(student_ans_2[0] + '=' + student_ans_2[i])
			else:
				self.data_st=student_ans_in

class StudentProblemCons:
	def __init__(self,st_id,p_id):
		try:
			self.p_student = StudentProblem.objects.get(student_id = st_id,problem_id = p_id)
			tries = self.p_student.succesful_attemps + 1
			StudentProblem.objects.filter(student_id = st_id,problem_id = p_id).update(succesful_attemps=tries)
		except:
			StudentProblem.objects.create(
				student_id = st_id,
				problem_id = p_id,
			)
			self.p_student = StudentProblem.objects.get(student_id = p_student_id,problem_id = p_id)

class StudentStepCons:
	def __init__(self,p_st_id,step_id_in):
		try:
			self.step_st = StudentStep.objects.get(problem_student_id=p_st_id,step_id=step_id_in)
			tries = self.step_st.succesful_attemps + 1
			StudentStep.objects.filter(problem_student_id=p_st_id,step_id=step_id_in).update(succesful_attemps=tries)
		except:
			StudentStep.objects.create(
				problem_student_id=p_st_id,
				step_id=step_id_in,
			)
			self.step_st = StudentStep.objects.get(problem_student_id=p_st_id,step_id=step_id_in)

class TemplateProcess(View):
	#TO DO: define __init__.
	def __init__(self,topic_input='Linear_equations',p_name_input='Oppgave 13'):
		#This will be read from the URL.
		self.topic_id_in = topic_input
		self.problem_name_in = p_name_input
		#Loading problem using the constructor to call the problem db.
		self.prob_cons = ProblemConstructor(self.topic_id_in,self.problem_name_in)
		#This number is read from the count method. Here I just use the Problem db.
		self.num_numerals = self.prob_cons.prob_in.number_of_numerals


	#This function is the one that loads and fills the problems is incomplete as it does not fill the number of steps and problem text yet see opp13.html#
	def get(self, request, *args, **kwargs):
		exercise_title=self.problem_name_in
		q1 = {"question": "pregunta 1 blablala", "num": "0"}
		q2 = {"question": "pregunta 2 blablala", "num": "1"}
		arreglo=[q1,q2]
		numerals=[]


		for t in range(1,self.num_numerals+1):
			numeralstest=ProblemNumeralConstructor("None",t)
			numerals.append(numeralstest.prob_num_in[0])

		data=serializers.serialize("json", numerals)





		locals = {
			'props': json.dumps({
				'title': exercise_title,
				'text': self.prob_cons.prob_in.text,
				'totalSteps': self.num_numerals,
				"numerals": data,

			})
		}

		return render(request, 'opp13.html', locals)

class DataAjax(TemplateProcess):
	def __init__(self):
		TemplateProcess.__init__(self)
		#TO DO: All the input from the student will be saved into a .txt file.
		#Read student answer
		#self.student_cons = StudentConstructor('1')
		#student problem db.
		#self.student_prob = StudentProblemCons(self.student_cons.student_cons,self.prob_cons.prob_in)

	#Method to process the ajax. step_ajax!!!
	#Why do we need this ajax?? The steps are send randomly!
	def get(self, request, *args, **kwargs):
		#NOTE: This is sending three numbers!!! I need the actual step!
		#The step number 4 is not even sended with the ajax. It does not enter this function anymore.

		step_number = json.loads(request.GET['step_number'])
		print("step_number")

		print(step_number)

		numeral_number = int(json.loads(request.GET['numeral_number']))


		print(numeral_number)
		numeral=ProblemNumeralConstructor("None",numeral_number).ProblemNumeralExist()


		#getting the data from the steps database
		datax=StepConstructor(step_number,numeral[0]).StepExist()


		print(datax.step_number)


		data=serializers.serialize("json",[datax])




		return HttpResponse(data, content_type='application/json')

class DataProcess(DataAjax):
	def __init__(self):
		DataAjax.__init__(self)
		self.data = False


	#Process method. Here the student answer is processed.
	def post(self, request, *args, **kwargs):
		#Definition of the symbols to be used within sympy.
		symbols = ['theta','x_1','x_2','y_2','y_1']
		symbol_output = SymbolConstructor(symbols)

		#Read student answer
		step_number = json.loads(request.POST['step_number'])
		s_name='Step ' + str(step_number)
		print("\n \n entre aqui2  \n\n")
		#reading student answer and cleaning it.
		student_ans = CleanStudentAns(json.loads(request.POST['student_answer']))
		print("\n \n entre aqui3  \n\n")
		#getting the data from the steps database
		
		datax = json.dumps(True)

		return HttpResponse(datax, content_type='application/json');


class Create(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'create.html')

class loadNumerals(View):
	def post(self, request, *args, **kwargs):
		nombre = request.POST['nombre']
		q1 = {"question": "pregunta 1 blablala", "num": "0"}
		q2 = {"question": "pregunta 2 blablala", "num": "1"}
		arreglo=[q1,q2]
		arreglox= json.dumps(arreglo)


		return HttpResponse(arreglox, content_type='application/json');
