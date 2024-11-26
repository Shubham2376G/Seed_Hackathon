
!pip install pymupdf
!pip install fillpdf

import datetime

from fillpdf import fillpdfs

def report_gen(name, age, gender, symptoms, ai_report, date, logs):

  form_fields=list(fillpdfs.get_form_fields("Report_template/template_1").keys())

  data_dict={
      form_fields[0]:"John Doe",
      form_fields[1]:"Male",
      form_fields[2]:"30",
      form_fields[3]:"Positive",
      form_fields[4]:"No significant history.",
      form_fields[5]:"Report generated using AI.",
      form_fields[6]:str(datetime.datetime.now()),
  }


  data_dict[0]=name
  data_dict[1]=age
  data_dict[2]=gender
  data_dict[3]=symptoms
  data_dict[4]=ai_report
  data_dict[5]=str(datetime.datetime.now().date())
  data_dict[6]=logs


  fillpdfs.write_fillable_pdf("/content/final_diagnosis.pdf",f"Records/{name}.pdf",data_dict)
