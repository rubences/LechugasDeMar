from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from fpdf import FPDF, HTMLMixin

def app():
    put_markdown('#Informe')
#group all the inputs to make a form
    data = input_group("Basic info",[
    input('Input yourname', name='name', required=True),
    checkbox("Languages of choice", ['JAVA', 'Python', 'C', 'C++'], name='loc'),
    select("Experience", ['0 - 1', '1 - 2', '2+'], name='yoe', required=True),
    radio("Gender", options=['Male', 'Female', 'Other'],name='gndr', required=True),
    textarea('Tell something about yourself', rows=3, name='abt', required=True),
    file_upload('Profile Image',placeholder='Choose file',accept='image/*',name='dp', required=True)])
    put_text("Hemos estudiado cuántas visitas recibe en el día el cliente y cuántas de ellas convierten y cuántas no (en %)")
    put_text("También hemos estudiado cuántas hay de cada una por tipo de conversión (CALL o FORM)")
    put_text("Además hemos estudiado el porcentaje de usuarios recurrentes sobre el total de usuarios")
    put_text("Y por último hemos estudiado el coche más visitado y si es el que más convierte")

#extracting image from input
    img = data['dp']
    with open('img.jpg', 'wb') as file:
        file.write(img['content'])
    with open('img.jpg', 'rb') as file:
        img = file.read()
    #display image
    put_image(img)
    put_markdown("____")
    # making a list of chosen languages
    loc = "<ul>"
    for i in data['loc']:
        loc += '<li>' + i + '</li>'
        loc += '</ul>'
    # formatting the data with html
    res = f"""
    <b>Name:</b> {data['name']}<br>
    <b>Languages of choice:</b> {loc}<br>
    <b>Experience:</b> {data['yoe']}<br>
    <b>Gender:</b> {data['gndr']}<br>
    <b>About:</b> {data['abt']}<br>"""
    # displaying the data
    put_html(res)
    # giving user option to choose whether pdf to be generated or not
    choice = actions('Generate PDF?', ['Generate','Cancel'])
    put_markdown("___")
    if choice == 'Generate':
        file_name = input('Name of pdf file?')
        generate_pdf(res, file_name)
        put_markdown("**PDF file generated**")
    else:
        put_markdown("PDF not generated")
# code to generate pdf
class MyFPDF(FPDF, HTMLMixin):
    pass
def generate_pdf(data,file_name):
    pdf = MyFPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(190, 15, 'Professional Info', ln=1, align='C')
    pdf.image('img.jpg', 85, 30, 40)
    pdf.line(10, 80, 200, 80)
    pdf.cell(60, 60, '', ln=2)
    pdf.write_html(data)
    pdf.output(f'{file_name}.pdf', 'F')
# main function
if __name__ == '__main__':
    start_server(app, port=32420, debug=True)