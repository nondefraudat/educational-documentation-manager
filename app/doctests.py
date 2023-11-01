from docxtpl import DocxTemplate

template = DocxTemplate('templates/word/annotation.docx')
for tag in template.get_undeclared_template_variables():
    print(tag)