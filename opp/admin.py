from django.contrib import admin
from django.db import models
from .models import Country,Author,Publisher,Book,Chapter,Topic,Subject
from .models import Problem,ProblemNumeral,Step,Substep
from .models import Student,School
from .models import StudentProblem, StudentStep

# Register your models here.
class ChapterInLine(admin.TabularInline):
	model = Chapter

class SubjectInLine(admin.TabularInline):
	model = Subject.book.through

class SubjectChapterInLine(admin.TabularInline):
	model = Subject.chapter.through

class BookInLine(admin.TabularInline):
	model = Book

class BookAuthorInLine(admin.TabularInline):
	model = Book.authors.through




class ProblemInLine(admin.TabularInline):
	model = Problem


class ProblemNumeralInLine(admin.TabularInline):
	model= ProblemNumeral


class StepInLine(admin.TabularInline):
	model= Step

class SubstepInLine(admin.TabularInline):
	model= Substep

class CountryAdmin(admin.ModelAdmin):
	list_display=('country_name',)

class BookAdmin(admin.ModelAdmin):
	list_display=('book_title',)
	filter_horizontal = ('authors',)
	inlines = [ChapterInLine,SubjectInLine]

class ChapterAdmin(admin.ModelAdmin):
	list_display=('book','chapter_name')
	inlines = [SubjectChapterInLine]

class AuthorAdmin(admin.ModelAdmin):
	list_display=('first_name','last_name')
	inlines = [BookAuthorInLine,]

class PublisherAdmin(admin.ModelAdmin):
	list_display=('publisher_name',)
	inlines = [BookInLine,]

class TopicAdmin(admin.ModelAdmin):
	list_display=('topic_name',)
	#To DO: Validate to make sure it is unique
	inlines = [ProblemInLine,]

class SubjectAdmin(admin.ModelAdmin):
	list_display=('subject_name','level')
	#To DO: Validate to make sure it is unique
	
class ProblemAdmin(admin.ModelAdmin):
	list_display=('topic_id','problem_name')
	inlines = [ProblemNumeralInLine,]

class ProblemNumeralAdmin(admin.ModelAdmin):
	list_display=('problem_id','numeral_name')
	inlines = [StepInLine,]
class StepAdmin(admin.ModelAdmin):
	list_display=('problem_num_id','step_number')
	inlines = [SubstepInLine,]

class SubstepAdmin(admin.ModelAdmin):
	list_display=('step_id','substep_name')

class SchoolAdmin(admin.ModelAdmin):
	list_display=('school_name',)

class StudentAdmin(admin.ModelAdmin):
	list_display=('student_name','number_solved_problems')

class StudentProblemAdmin(admin.ModelAdmin):
	list_display=('student_id','problem_id')

class StudentStepAdmin(admin.ModelAdmin):
	list_display=('problem_student_id','step_id')

admin.site.register(Country,CountryAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Chapter,ChapterAdmin)

admin.site.register(Topic,TopicAdmin)
admin.site.register(Subject,SubjectAdmin)

admin.site.register(Problem,ProblemAdmin)
admin.site.register(ProblemNumeral,ProblemNumeralAdmin)
admin.site.register(Step,StepAdmin)
admin.site.register(Substep,SubstepAdmin)

admin.site.register(School,SchoolAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(StudentProblem,StudentProblemAdmin)
admin.site.register(StudentStep,StudentStepAdmin)
