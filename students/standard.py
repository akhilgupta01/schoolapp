from students.students import Student
class Section:
    def __init__(self, name:str):
        self.name = name
        self.students = []

    def attr_check(self, attr_name, student:Student, stats:dict):
        passed = False
        current_count = sum(1 for s in self.students if s.get_attr(attr_name) == student.get_attr(attr_name))
        threshold = stats[attr_name][student.get_attr(attr_name)]/stats['total_sections']
        if (current_count < threshold):
            passed = True
        return passed

    def composite_attr_check(self, attr_names, student:Student, stats:dict):
        passed = False
        current_count = sum(1 for s in self.students if all(s.get_attr(attr_name) == student.get_attr(attr_name) for attr_name in attr_names))
        threshold = stats[str(attr_names)][tuple([student.get_attr(attr_name) for attr_name in attr_names])]/stats['total_sections']
        if (current_count < threshold):
            passed = True
        return passed

    def can_accomodate(self, student:Student, allocation_order:list, stats:dict):
        for criteria in allocation_order:
            if isinstance(criteria, list):
                if not self.composite_attr_check(criteria, student, stats):
                    return False
            else:
                if not self.attr_check(criteria, student, stats):
                    return False
        return True
        

    def add_student(self, student:Student):
        student.new_section = self.name
        self.students.append(student)
    
    def __str__(self):
        student_details = "\n".join([str(student) for student in self.students])
        return f"{self.name} student_count={len(self.students)}\n{student_details}"
