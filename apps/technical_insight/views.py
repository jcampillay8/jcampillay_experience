from django import forms
import django
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.urls import reverse

@login_required(login_url='login')
def technical_insight(request):
    return render(request, 'technical_insight/technical_insight_home.html',{'current_pages': ['about_me_home','technical_insight']})

@login_required(login_url='login')
def knowledge_skills(request):
    return render(request, 'technical_insight/knowledge_skill.html',{'current_pages': ['about_me_home','technical_insight']})

@login_required(login_url='login')
def knowledge_skills_describe(request, id):

    if id == 49:
        # Obtén la URL completa proyecto --> Portfolio Website
        knowledge_skills_url = reverse('knowledge_skills_describe', args=[9])
        context = {
            'current_pages': ['about_me_home','technical_insight'],
            'knowledge_skills_url': knowledge_skills_url,
            'title_technology' : 'Python 3',
            'publication_date' : '02-06-2024',
            'author' : 'Jaime Campillay',
            'type_technology' : _('Program Language'),
            'title2_technology' : _('Why Python?'),
            'technology_image' : 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg'
          
            # 'end_date' : 2024,
            # 'start_date' : 2024,
            # 'project_name' : _('Website Portfolio with Django'),
            # 'company_name' : _('Entrepreneurship'),
            # 'description_project' : _(''' Este proyecto de emprendimiento consiste en un sitio web desarrollado con Django, destinado a ofrecer servicios de desarrollo web personalizados. El sitio web proporciona una plataforma integral donde se muestran los servicios ofrecidos, incluyendo diseño y desarrollo de sitios web, integración de bases de datos y creación de aplicaciones web interactivas.
            # El sitio web también presenta una sección detallada de los proyectos realizados, destacando las tecnologías utilizadas como Django, Python, PostgreSQL, HTML, CSS y JavaScript. Estos proyectos demuestran la capacidad para resolver problemas complejos y entregar soluciones eficientes.
            # Además, el sitio incluye una sección "Sobre Mí", que ofrece información sobre el desarrollador, sus intereses en ingeniería, naturaleza, senderismo y música, proporcionando una conexión personal con los visitantes. La sección de contacto facilita la comunicación con los clientes, y los gráficos y visualizaciones se utilizan para ilustrar datos y logros de manera clara y atractiva. Este sitio web no solo muestra el trabajo y las habilidades del desarrollador, sino que también ofrece una experiencia completa y accesible para los usuarios.'''),
            # 'technology_list' : 'Python, Django, Dash & Plotly, JavaScript, HTML5, CSS3, Bootstrap 5, jQuery, FontAwesome, Ajax, PostgreSQL, AWS EC2, AWS S3, AWS DRS, Git, Json, Vim, Linux',
            # 'company_description_part_1' : _(''),
            # 'company_description_part_2' : _(''),
            # 'image_path' : "images/project/banner-slide-9.jpg"
        }
        return render(request, 'technical_insight/knowledge_skills_describe.html', context)
        
    elif id == 8:
        # Obtén la URL completa proyecto --> Cloud Strategy - Redbanc
        project_url = reverse('projects_describe', args=[8])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            # 'end_date' : 2023,
            # 'start_date' : 2023,
            # 'project_name' : _('Cloud Strategy'),
            # 'company_name' : _('Redbanc'),
            # 'description_project' : _('El proyecto de asesoría "Estrategia Nube" para Redbanc se centra en la migración de sus operaciones de infraestructura On Premise a la nube, evaluando factores como seguridad, escalabilidad, flexibilidad y costos. Se destacan ventajas como la capacidad de escalar recursos según demanda, reducción de costos operativos, y mejora en la disponibilidad del servicio. La estrategia más viable para Redbanc es una migración híbrida, combinando recursos On Premise y en la nube, utilizando servicios de nube pública para cargas fluctuantes y privada para datos sensibles. Esto incluye tecnologías como Docker y Kubernetes para facilitar la portabilidad y gestión de aplicaciones, asegurando la integridad y seguridad de las operaciones críticas mientras se optimiza la infraestructura tecnológica y la capacidad de respuesta al mercado.'),
            # 'technology_list' : 'Python, Power Point',
            # 'company_description_part_1' : _('Redbanc es una empresa chilena especializada en la provisión de servicios de interconexión y procesamiento de transacciones electrónicas. Fundada en 1987, Redbanc se ha convertido en una pieza fundamental del sistema financiero chileno, ofreciendo una infraestructura robusta y segura para la operación de cajeros automáticos y otros servicios de pago electrónico. La compañía facilita la integración de diversas instituciones financieras, permitiendo a los usuarios realizar transacciones bancarias de manera eficiente y segura.'),
            # 'company_description_part_2' : _('Con una red extensa de cajeros automáticos a nivel nacional, Redbanc se dedica a garantizar la disponibilidad y el buen funcionamiento de estos dispositivos, mejorando así la accesibilidad a los servicios bancarios para todos los chilenos. Su estrategia se basa en la innovación tecnológica y en el mantenimiento de altos estándares de seguridad y calidad. Además, Redbanc colabora activamente con las instituciones financieras del país para desarrollar soluciones que respondan a las necesidades cambiantes del mercado, contribuyendo al desarrollo y modernización del sistema financiero chileno.'),
            # 'image_path' : "images/project/banner-slide-4.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)

    else:
        # Otra lógica para proyectos diferentes
        return render(request, 'technical_insight/technical_insight_home.html', context)


@login_required(login_url='login')
def professional_project_home(request):
    return render(request, 'portfolio/portfolio_home.html',{'current_pages': ['portfolio','portfolio_home']})


@login_required(login_url='login')
def projects_describe(request, id):
    
    if id == 9:
        # Obtén la URL completa proyecto --> Portfolio Website
        project_url = reverse('projects_describe', args=[9])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            'end_date' : 2024,
            'start_date' : 2024,
            'project_name' : _('Website Portfolio with Django'),
            'company_name' : _('Entrepreneurship'),
            'description_project' : _(''' Este proyecto de emprendimiento consiste en un sitio web desarrollado con Django, destinado a ofrecer servicios de desarrollo web personalizados. El sitio web proporciona una plataforma integral donde se muestran los servicios ofrecidos, incluyendo diseño y desarrollo de sitios web, integración de bases de datos y creación de aplicaciones web interactivas.
            El sitio web también presenta una sección detallada de los proyectos realizados, destacando las tecnologías utilizadas como Django, Python, PostgreSQL, HTML, CSS y JavaScript. Estos proyectos demuestran la capacidad para resolver problemas complejos y entregar soluciones eficientes.
            Además, el sitio incluye una sección "Sobre Mí", que ofrece información sobre el desarrollador, sus intereses en ingeniería, naturaleza, senderismo y música, proporcionando una conexión personal con los visitantes. La sección de contacto facilita la comunicación con los clientes, y los gráficos y visualizaciones se utilizan para ilustrar datos y logros de manera clara y atractiva. Este sitio web no solo muestra el trabajo y las habilidades del desarrollador, sino que también ofrece una experiencia completa y accesible para los usuarios.'''),
            'technology_list' : 'Python, Django, Dash & Plotly, JavaScript, HTML5, CSS3, Bootstrap 5, jQuery, FontAwesome, Ajax, PostgreSQL, AWS EC2, AWS S3, AWS DRS, Git, Json, Vim, Linux',
            'company_description_part_1' : _('Este es mi proyecto'),
            'company_description_part_2' : _('Este es mi proyecto'),
            'image_path' : "images/project/banner-slide-9.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)
    elif id == 8:
        # Obtén la URL completa proyecto --> Cloud Strategy - Redbanc
        project_url = reverse('projects_describe', args=[8])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            'end_date' : 2023,
            'start_date' : 2023,
            'project_name' : _('Cloud Strategy'),
            'company_name' : _('Redbanc'),
            'description_project' : _('El proyecto de asesoría "Estrategia Nube" para Redbanc se centra en la migración de sus operaciones de infraestructura On Premise a la nube, evaluando factores como seguridad, escalabilidad, flexibilidad y costos. Se destacan ventajas como la capacidad de escalar recursos según demanda, reducción de costos operativos, y mejora en la disponibilidad del servicio. La estrategia más viable para Redbanc es una migración híbrida, combinando recursos On Premise y en la nube, utilizando servicios de nube pública para cargas fluctuantes y privada para datos sensibles. Esto incluye tecnologías como Docker y Kubernetes para facilitar la portabilidad y gestión de aplicaciones, asegurando la integridad y seguridad de las operaciones críticas mientras se optimiza la infraestructura tecnológica y la capacidad de respuesta al mercado.'),
            'technology_list' : 'Python, Power Point, Excel, PDF',
            'company_description_part_1' : _('Redbanc es una empresa chilena especializada en la provisión de servicios de interconexión y procesamiento de transacciones electrónicas. Fundada en 1987, Redbanc se ha convertido en una pieza fundamental del sistema financiero chileno, ofreciendo una infraestructura robusta y segura para la operación de cajeros automáticos y otros servicios de pago electrónico. La compañía facilita la integración de diversas instituciones financieras, permitiendo a los usuarios realizar transacciones bancarias de manera eficiente y segura.'),
            'company_description_part_2' : _('Con una red extensa de cajeros automáticos a nivel nacional, Redbanc se dedica a garantizar la disponibilidad y el buen funcionamiento de estos dispositivos, mejorando así la accesibilidad a los servicios bancarios para todos los chilenos. Su estrategia se basa en la innovación tecnológica y en el mantenimiento de altos estándares de seguridad y calidad. Además, Redbanc colabora activamente con las instituciones financieras del país para desarrollar soluciones que respondan a las necesidades cambiantes del mercado, contribuyendo al desarrollo y modernización del sistema financiero chileno.'),
            'image_path' : "images/project/banner-slide-4.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)
    elif id == 7:
        # Obtén la URL completa proyecto --> ALM Financial Tool International Bank
        project_url = reverse('projects_describe', args=[7])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            'end_date' : 2023,
            'start_date' : 2023,
            'project_name' : _('Desarrollo de Herramienta para MItigación de Riesgos en Instituciones Financieras'),
            'company_name' : _('International Bank'),
            'description_project' : _('Desarrollo de una herramienta eficiente para ainstituciones financieras, centradas en la gestión de riesgos cambiarios en inversiones a través de intrumentos derivados. Utilicé Python, y ibliotecas como Pandas, Dash Plotly, Scipy, para construir el módulo Gestión de Riesgos y Estrategia de Cobertura, lo que contribuyó al fortalecimienot de mis habilidades en programación y análisis de datos'),
            'technology_list' : 'Python, PostgreSQL, Dash & Plotly, Pandas, Scipy',
            'company_description_part_1' : _('Banco Internacional es una entidad financiera con sede en Quito, Ecuador. Fundado en 1973, se ha consolidado como uno de los principales bancos del país, ofreciendo una amplia gama de productos y servicios financieros. Estos incluyen cuentas de ahorro y corrientes, préstamos personales y comerciales, tarjetas de crédito, y servicios de banca electrónica. Banco Internacional se distingue por su enfoque en la atención al cliente y su compromiso con la innovación tecnológica para mejorar la experiencia bancaria de sus usuarios.'),
            'company_description_part_2' : _('A lo largo de los años, Banco Internacional ha logrado establecerse como un actor clave en el sector financiero ecuatoriano. Su estrategia se basa en la solidez financiera, la eficiencia operativa y la diversificación de servicios. Con una red de sucursales y cajeros automáticos en todo el país, Banco Internacional se dedica a proporcionar servicios financieros accesibles y de alta calidad. Además, la institución se compromete con la responsabilidad social corporativa, apoyando diversas iniciativas en educación, salud y desarrollo comunitario, contribuyendo así al bienestar de la sociedad ecuatoriana.'),
            'image_path' : "images/project/banner-slide-5.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)
    elif id == 6:
        # Obtén la URL completa proyecto --> ETL SQL BICE Factset
        project_url = reverse('projects_describe', args=[6])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            'end_date' : 2023,
            'start_date' : 2023,
            'project_name' : _('Extracción y Tratamiento de Datos en la Industria Bancaria'),
            'company_name' : _('BICE Inversiones - FactSet'),
            'description_project' : _('En el marco del proyecto, se enfatizó el uso de SQL y la implementación de Stored Procedures para extraer, limpiar y estandarizar grandes cantidades de datos clave. Además, se utilizó la herramienta ETL Talend para asegurar la calidad de los datos antes de su migración desde servidores locales a entornos en la nube. Se destaca la importancia de gestionar eficazmente datos complejos y garantizar su integridad en un entorno crítico para el sector bancario. Los resultados contribuyeron a la optimización de procesos y la mejora en la toma de decisiones dentro de la organización.'),
            'technology_list' : 'SQL Server, Talend, Python, Excel, Factset Cloud, Putty',
            'company_description_part_1' : _('BICE Inversiones es una institución financiera chilena con sede en Santiago, Chile. Fundada en 1978, forma parte del grupo financiero BICE y se especializa en servicios de inversión y asesoría financiera. Ofrece una amplia gama de productos financieros, incluyendo fondos mutuos, gestión de patrimonios, corretaje de valores y asesoría en inversiones.'),
            'company_description_part_2' : _('BICE Inversiones se ha consolidado como un actor relevante en el mercado financiero chileno. Su estrategia se centra en proporcionar soluciones personalizadas y de alto valor a sus clientes. Con un enfoque en la innovación y el servicio al cliente, BICE Inversiones busca maximizar el rendimiento de las inversiones y ofrecer asesoría experta para alcanzar los objetivos financieros de sus clientes.'),
            'image_path' : "images/project/banner-slide-3.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)
    elif id == 5:
        # Obtén la URL completa proyecto --> Hipotecario Garantía
        project_url = reverse('projects_describe', args=[5])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            'end_date' : 2023,
            'start_date' : 2022,
            'project_name' : _('Robot: Automatización BO Hipotecario Garantía'),
            'company_name' : _('Scotiabank - Operaciones Garantía'),
            'description_project' : _('Robot que rescata desde una tabla de Base de Datos los casos a hacer mantención, con el Id Documento se ingresa a una página web interna del Banco para descargar el Informe actualizado enviado desde distintas notarías en formato PDF cuyo contenido es de difícil manejo debido que los informes constantemente vienen con formato ‘sucio’ y son varios campos a rescatar, por lo que se aplican varías formas ingeniosas para dar con la información que se requiere para luego con toda la información ya rescatada, se ingresa a sitio web más antiguo del banco, donde se deben hacer las mantenciones de los clientes ingresando la información rescatada en sus lugares respectivos dentro de sitio web antiguo que no conversa con la página nueva de donde se descargó el informe.'),
            'technology_list' : 'UiPath Reframework, SQL, .Net, Git, Jira Browser Edge, PDF Json File',
            'company_description_part_1' : _('Scotiabank es una institución financiera multinacional con sede en Toronto, Canadá. Fundada en 1832, es uno de los bancos más grandes de Canadá y cuenta con una fuerte presencia internacional. Ofrece una amplia gama de productos y servicios financieros, incluyendo banca personal y comercial, gestión de patrimonios, y banca corporativa.'),
            'company_description_part_2' : _('Scotiabank ha logrado establecerse como un actor importante en el mercado financiero global. Su estrategia se basa en la diversificación geográfica y la inversión en tecnología. Con una red de más de 900 sucursales y 3,600 cajeros automáticos en todo el mundo, Scotiabank se dedica a proporcionar servicios financieros accesibles y de calidad.'),
            'image_path' : "images/project/banner-slide-2.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)
    elif id == 4:
        print('This is 4')
        # Obtén la URL completa proyecto --> Curse Linea Seguro
        project_url = reverse('projects_describe', args=[4])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            'end_date' : 2022,
            'start_date' : 2022,
            'project_name' : _('Robot: Curse Linea Seguros'),
            'company_name' : _('Scotiabank - Corredora Seguros'),
            'description_project' : _('Robot que está corriendo todo el día, chequeando constantemente si ha llegado correo con el asunto de ‘si cliente aceptó o no el Seguro ofrecido’. El robot al encontrar un caso, lee y rescata información desde correo, es cargada a una tabla de Base de Datos y se procede a hacer varias validaciones a través de servicios API los cuales algunos de ellos requieren de una llave que ocupa Python para su uso. El resultado, al cliente en caso de aprobar, le llega un correo con aviso tiene su seguro ya corriendo a la vez que se han sido actualizado los datos del cliente en los sistemas internos del banco, en caso de rechazo se envía correo y se actualiza los datos del cliente en los sistemas internos del banco con los datos de rechazo.'),
            'technology_list' : 'UiPath Reframework, Postman, Servicios API, Python, .Net, Git, Jira, Json File',
            'company_description_part_1' : _('Scotiabank es una institución financiera multinacional con sede en Toronto, Canadá. Fundada en 1832, es uno de los bancos más grandes de Canadá y cuenta con una fuerte presencia internacional. Ofrece una amplia gama de productos y servicios financieros, incluyendo banca personal y comercial, gestión de patrimonios, y banca corporativa.'),
            'company_description_part_2' : _('Scotiabank ha logrado establecerse como un actor importante en el mercado financiero global. Su estrategia se basa en la diversificación geográfica y la inversión en tecnología. Con una red de más de 900 sucursales y 3,600 cajeros automáticos en todo el mundo, Scotiabank se dedica a proporcionar servicios financieros accesibles y de calidad.'),
            'image_path' : "images/project/banner-slide-6.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)
    elif id == 3:
        # Obtén la URL completa proyecto --> Telemarketing
        project_url = reverse('projects_describe', args=[3])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            'end_date' : 2022,
            'start_date' : 2021,
            'project_name' : _('Robot: Procesamiento Telemarketing'),
            'company_name' : _('Scotiabank - Telemarketing & Back Office Operaciones Negocio'),
            'description_project' : _('Robot rescata desde 2 carpetas compartidas, 6 archivos Excel los cuales contienen las ventas hechas durante el día por Telemarketing, la información es depurada y cargada a una tabla de Base Datos donde se aplican varias validaciones según reglas de negocio finalizando en 2 tablas que se llevan a archivos Txt con formato específico con las ventas del día aprobadas más un reporte con los casos rechazados.'),
            'technology_list' : 'UiPath Reframework, SQL, .Net, Git, Jira, Excel',
            'company_description_part_1' : _('Scotiabank es una institución financiera multinacional con sede en Toronto, Canadá. Fundada en 1832, es uno de los bancos más grandes de Canadá y cuenta con una fuerte presencia internacional. Ofrece una amplia gama de productos y servicios financieros, incluyendo banca personal y comercial, gestión de patrimonios, y banca corporativa.'),
            'company_description_part_2' : _('Scotiabank ha logrado establecerse como un actor importante en el mercado financiero global. Su estrategia se basa en la diversificación geográfica y la inversión en tecnología. Con una red de más de 900 sucursales y 3,600 cajeros automáticos en todo el mundo, Scotiabank se dedica a proporcionar servicios financieros accesibles y de calidad.'),
            'image_path' : "images/project/banner-slide-7.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)
    elif id == 2:
        # Obtén la URL completa proyecto --> ReportWorks MobileApp
        project_url = reverse('projects_describe', args=[2])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            'end_date' : 2020,
            'start_date' : 2019,
            'project_name' : _('ReportWorks - Mobile App'),
            'company_name' : _('TECHINT Ingeniería y Construcción'),
            'description_project' : _('Aplicación Android que automatiza los reportes generados por los ‘Apuntadores’ inicialmente en Excel o Papel desde distintas ubicaciones geográficas, depurando los datos ‘sucios’ y adaptándolo al formato correspondiente.'),
            'technology_list' : 'Google Apps Script, Servicio API, AppInventor (MIT), Google SpreadSheet',
            'company_description_part_1' : _('Techint Ingeniería y Construcción es una empresa multinacional con sede en Milán, Italia, y Buenos Aires, Argentina. Fundada en 1945, es una de las compañías más grandes de América Latina en el sector de la ingeniería y la construcción. Techint ofrece una amplia gama de servicios, que incluyen diseño, ingeniería, construcción, operación y mantenimiento de proyectos industriales y de infraestructura.'),
            'company_description_part_2' : _('Techint ha establecido una sólida reputación en el mercado global de la construcción. Su estrategia se basa en la innovación tecnológica y en la excelencia operativa. Con una presencia en más de 45 países, Techint se dedica a entregar proyectos de alta calidad y complejidad, contribuyendo al desarrollo económico y social de las regiones donde opera.'),
            'image_path' : "images/project/banner-slide-1.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)
    elif id == 1:
        # Obtén la URL completa proyecto --> Odoo
        project_url = reverse('projects_describe', args=[1])
        context = {
            'current_pages': ['portfolio', 'portfolio_home'],
            'project_url': project_url,
            'end_date' : 2020,
            'start_date' : 2019,
            'project_name' : _('Implementation & Manage Odoo ERP'),
            'company_name' : _('Clearpix'),
            'description_project' : _('Este proyecto se centra en la implementación y gestión de Odoo, un software de gestión empresarial, en una pyme de Valparaíso dedicada a la venta de prendas de vestir personalizadas y otros objetos. La implementación de Odoo optimiza procesos clave como la gestión de inventarios, ventas, compras y contabilidad. La integración del sistema permite una mayor eficiencia operativa y un mejor control sobre las operaciones diarias, mejorando así la productividad y la capacidad de respuesta al cliente.'),
            'technology_list' : 'Odoo ERP, Python, Excel',
            'company_description_part_1' : _('Clearpix es una empresa fundada en 2016, especializada en la personalización de prendas de vestir. Con un enfoque en la calidad y la creatividad, Clearpix ofrece una amplia gama de productos personalizados para satisfacer las necesidades de sus clientes, combinando diseño innovador y técnicas avanzadas de impresión y bordado.'),
            'company_description_part_2' : _('Fue un emprendimiento con un amigo de Valparaíso'),
            'image_path' : "images/project/banner-slide-8.jpg"
        }
        return render(request, 'portfolio/project_describe.html', context)
    else:
        # Otra lógica para proyectos diferentes
        return render(request, 'technical_insight/technical_insight_home.html', context)
