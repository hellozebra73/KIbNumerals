from django.db import models

# Create your models here.
#Felipe models
class student_ans(models.Model):
    number=models.CharField(max_length=100)
    text=models.CharField(max_length=100)
    solucion=models.CharField(max_length=100)
    def __str__(self):
        return self.number

#Karla models
class Country(models.Model):
	# The country ID follows the international standard for country codes: i.e COL
	country_id = models.SlugField(primary_key=True,verbose_name='Country code')
	country_name = models.CharField(max_length = 500,verbose_name='Country')
	def __str__(self):
		return self.country_name

class Publisher(models.Model):
	publisher_name = models.CharField(max_length=100)
	address = models.CharField(max_length=100, verbose_name='Address')
	#TO DO: add these two databases
	#city = models.CharField(max_length=100)
	#state_province = models.CharField(max_length=100)
	country = models.ManyToManyField(Country)
	website = models.URLField(blank=True)
	def __str__(self):
		return self.publisher_name

class Author(models.Model):
	first_name = models.CharField(max_length=100, verbose_name='First name')
	last_name = models.CharField(max_length=100, verbose_name='Last name')
	email = models.EmailField()
	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)

class Book(models.Model):
	book_title = models.CharField(max_length=100,verbose_name='Book title')
	authors = models.ManyToManyField(Author)
	publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE,primary_key=False)
	publication_date = models.DateField(blank=True)
	def __str__(self):
		return self.book_title

class Chapter(models.Model):
	chapter_number = models.PositiveIntegerField(default='0')
	chapter_name = models.CharField(max_length=100,verbose_name='Chapter name')
	book = models.ForeignKey(Book,on_delete=models.CASCADE,primary_key=False)
	def __unicode__(self):
		return '%s %s' % (self.book, self.chapter_name)

class Subject(models.Model):
	# The subject code has to be predefined
	subject_id = models.SlugField(primary_key=True,verbose_name='Subject code')
	subject_name = models.CharField(max_length=500,verbose_name='Subject')
	description = models.TextField(blank=True)
	level=models.CharField(max_length=100,choices=(
		('Primary','Primary-school'),
		('Secondary','Secondary-school'),
		('SH','High-school'),
		('UG','Undergrad'),
		('Grad','Graduate')))
	country=models.ManyToManyField(Country)
	book=models.ManyToManyField(Book)
	chapter=models.ManyToManyField(Chapter)
	def __str__(self):
		return self.subject_name

class Topic(models.Model):
	topic_id=models.SlugField(primary_key=True,verbose_name='Topic ID')
	topic_name=models.CharField(max_length=500,verbose_name='Topic name')
	description = models.TextField(blank=True)

	def __str__(self):
		#TO DO: return subject name -- through??
		return '%s: %s' % (self.topic_id, self.topic_name)

class Problem(models.Model):
	topic_id=models.ForeignKey(Topic,primary_key=False,on_delete=models.CASCADE,verbose_name='Topic ID')
	problem_name=models.CharField(max_length=500,verbose_name='Problem name')
	text=models.TextField()
	#TO DO: This can be a FileField or a FilePathField.
	template=models.CharField(max_length=500,verbose_name='Problem Template', default='')
	#TO DO: How to take into account the number of steps.
	number_of_numerals=models.PositiveIntegerField(default=1)

	class Meta:
		unique_together = (('topic_id','problem_name'),)
	def __str__(self):
		return '%s %s' % (self.topic_id, self.problem_name)

class ProblemNumeral(models.Model):
	problem_id=models.ForeignKey(Problem, primary_key=False, on_delete=models.CASCADE,verbose_name='Problem ID')
	numeral_name=models.CharField(max_length=500, verbose_name='Numeral name', default='a', blank=True)
	#NOTE: This will be changed to a numeral a, b, c .... and that will be send to the front.
	numeral_number=models.PositiveIntegerField(default=0)
	question=models.TextField()
	explanation=models.TextField()
	#TO DO: Count the number of steps automatically -- form?.
	number_of_steps=models.PositiveIntegerField(default=1)
	class Meta:
		unique_together=(('problem_id','numeral_number'),)
	def __unicode__(self):
		return '%s %s' %(self.problem_id,self.numeral_number)

class Step(models.Model):
	problem_num_id=models.ForeignKey(ProblemNumeral,primary_key=False,on_delete=models.CASCADE,verbose_name='Problem Numeral ID')
	step_name=models.CharField(max_length=500, verbose_name='Step name', blank=True)
	step_number=models.PositiveIntegerField(default=0)
	explanation=models.TextField()
	video=models.CharField(max_length=500)
	instruction = models.TextField()
	#TO DO: Count autoatically the number of steps. Include count method.
	number_of_substeps=models.PositiveIntegerField(default=0)
	class Meta:
		unique_together=(('problem_num_id','step_number'),)
	def __unicode__(self):
		return '%s %s' %(self.problem_num_id.numeral_name,self.step_number)

class Substep(models.Model):
	step_id=models.ForeignKey(Step,primary_key=False,on_delete=models.CASCADE,verbose_name='Step ID')
	substep_name=models.CharField(max_length=500,verbose_name='Substep name')
	answer=models.TextField()
	hint = models.TextField()
	class Meta:
		unique_together=(('step_id','substep_name'),)
	def __str__(self):
		return '%s %s' % (self.step_id,self.substep_name)

class School(models.Model):
	school_id = models.SlugField(primary_key=True,verbose_name='School code')
	school_name = models.CharField(max_length = 500,verbose_name='School')
	def __str__(self):
		return self.school_name

class Student(models.Model):
    student_name=models.CharField(max_length=100)
    number_solved_problems=models.IntegerField(default='0')
    country=models.ForeignKey(Country,primary_key=False,on_delete=models.CASCADE,verbose_name='Country name')
    school=models.ManyToManyField(School)
    def __str__(self):
        return self.student_name

class StudentProblem(models.Model):
	student_id=models.ForeignKey(Student,primary_key=False,on_delete=models.CASCADE,verbose_name='Student ID')
	problem_id=models.ForeignKey(Problem,primary_key=False,on_delete=models.CASCADE,verbose_name='Problem ID')
	#TO DO: Change this with a ModelForm - make it increase from outside.
	succesful_attemps=models.IntegerField(default='0')
	fail_attemps=models.IntegerField(default='0')
	#TO DO: The total number is calculated with a count method. Autofill.
	answer_file=models.CharField(max_length=100,verbose_name='answer_file')

	class Meta:
		unique_together = (('student_id','problem_id'),)

	def __str__(self):
		return '%s %s' %(self.problem_id.problem_name, self.student_id.student_name)

class StudentStep(models.Model):
	problem_student_id = models.ForeignKey(StudentProblem, on_delete=models.CASCADE, primary_key=False)
	step_id = models.ForeignKey(Step, on_delete=models.CASCADE,primary_key=False)
	succesful_attemps=models.IntegerField(default='0')
	fail_attemps=models.IntegerField(default='0')
	#This is defined by the students input.
	number_of_substeps=models.IntegerField(default='0')

	class Meta:
		unique_together = (('problem_student_id','step_id'),)

	def __str__(self):
		return self.step_id.step_id
