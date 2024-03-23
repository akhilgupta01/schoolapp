import pandas as pd
import random
from students.standard import Section
from students.students import Student

class StudentAllocator:
    allocation_order = ['House', 'Gender', 'AcademicBand', ['House', 'Gender'], 'RTE']

    def __init__(self, students_df, target_sections:list):
        self.students_df = students_df
        self.new_sections = [Section(section) for section in target_sections]
        self.stats = self.__gather_stats()
    
    def __gather_stats(self):
        stats = {}
        for col in self.allocation_order:
            stats[str(col)] = self.students_df[col].value_counts().to_dict()
        stats['total_sections'] = len(self.new_sections)
        return stats
        
    def __allocate(self, for_allocation, allocation_order):
        not_allocated = []
        for student_row in for_allocation:
            student = Student(student_row.to_dict())
            student_added = False
            random.shuffle(self.new_sections)
            for section in self.new_sections:
                if section.can_accomodate(student, allocation_order, self.stats):
                    section.add_student(student)
                    student.set_attr('Target Section', section.name)
                    student_added = True
                    break
            if not student_added:
                not_allocated.append(student_row)
        return not_allocated

    
    def allocate(self):
        not_allocated = []
        for index, student_row in self.students_df[self.students_df['Target Section'].isnull()].iterrows():
            not_allocated.append(student_row)
        allocation_criteria = [] + self.allocation_order
        while len(not_allocated) > 0 and len(allocation_criteria) > 0:
            not_allocated = self.__allocate(not_allocated, allocation_criteria)
            allocation_criteria = allocation_criteria[:-1]
        
        allocated_students_df = pd.DataFrame([student.to_dict() for section in self.new_sections for student in section.students])
        return allocated_students_df
