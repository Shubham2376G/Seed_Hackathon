
import datetime

from fillpdf import fillpdfs

def report_gen(name, age, gender, symptoms, ai_report, date, logs):

  form_fields=list(fillpdfs.get_form_fields("Report_template/template_1.pdf").keys())

  data_dict={
      form_fields[0]:name,
      form_fields[1]:age,
      form_fields[2]:gender,
      form_fields[3]:symptoms,
      form_fields[4]:ai_report,
      form_fields[5]:str(datetime.datetime.now().date()),
      form_fields[6]:logs,
  }



  # fillpdfs.write_fillable_pdf("Report_template/template_1.pdf",f"{name}.pdf",data_dict)
  fillpdfs.write_fillable_pdf("Report_template/template_1.pdf",f"Records/{name}.pdf",data_dict)
