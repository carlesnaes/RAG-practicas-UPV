from langchain.schema import Document


def cargar_chunks_manual(role):
    docs = []

    # Chunk 1: Requisitos curriculares
    docs.append(Document(
        page_content=(
            "Para poder realizar prácticas curriculares en la ETSINF de la Universitat Politècnica de València (UPV), "
            "es obligatorio haber superado completamente el primer curso del grado. "
            "Esto significa que el estudiante debe tener aprobadas todas las asignaturas de primer curso antes de poder iniciar las prácticas. "
            "Sin embargo, esto es solo para grados, los dobles grados no pueden hacer prácticas curriculares. "
            "Este requisito garantiza que el alumno tenga una base académica mínima adecuada para enfrentarse a un entorno profesional. "
            "Cuando tenga el primer curso superado, podrá realizar prácticas externas curriculares. "
            "Es un requisito indispensable para poder realizar prácticas curriculares en la ETSINF de la UPV."
        ),
        metadata={"source": "manual", "categoria": "requisitos_curriculares", "role": role}
    ))

    # Chunk 2: Dobles grados
    docs.append(Document(
        page_content=(
            "En los dobles grados como el Doble Grado en Ciencia de Datos e Ingeniería de Organización Industrial, "
            "el Doble Grado en Ingeniería Informática y Matemáticas, y el Doble Grado en Ingeniería Informática y Administración y Dirección de Empresas, "
            "no se pueden realizar prácticas curriculares debido a que estas titulaciones no contemplan asignaturas optativas en su plan de estudios. "
            "Sin embargo, sí es posible realizar prácticas extracurriculares, con un máximo de 1800 horas. "
            "Estas prácticas permiten al estudiante adquirir experiencia profesional adicional, aunque no forman parte del cómputo académico del grado. "
            "En resumen, las prácticas curriculares no se pueden hacer en un Doble Grado."
        ),
        metadata={"source": "manual", "categoria": "dobles_grados", "role": role}
    ))

    # Chunk 3: Requisitos generales de prácticas
    docs.append(Document(
        page_content=(
            "Requisitos: Para poder realizar prácticas externas en la Universitat Politècnica de València (UPV), "
            "el estudiantado debe cumplir los siguientes requisitos generales: estar matriculado o matriculada durante "
            "todo el periodo de prácticas, no haber finalizado la titulación ni superado el 100% de los créditos, "
            "y estar inscrito o inscrita en la base de datos curricular del Servicio Integrado de Empleo (SIE). "
            "Además, en función del tipo de prácticas, se exige lo siguiente: "
            "para prácticas curriculares, haber superado todas las asignaturas de primer curso y estar matriculado o matriculada "
            "en los créditos correspondientes; para prácticas extracurriculares, los requisitos son haber superado al menos el 50% "
            "de los créditos de la titulación. Estos criterios garantizan que el estudiantado se encuentre en una situación académica adecuada."
        ),
        metadata={"source": "manual", "categoria": "requisitos_practicas", "role": role}
    ))

    # Chunk 4: Evaluación de prácticas
    docs.append(Document(
        page_content=(
            "La evaluación de las prácticas externas en la Universitat Politècnica de València (UPV) la realiza el tutor académico UPV. "
            "Esta evaluación se basa en los informes elaborados por el propio estudiante y por el tutor o tutora de la entidad colaboradora. "
            "Ambos documentos deben reflejar el desarrollo y cumplimiento del plan formativo, sirviendo como base para la calificación final."
        ),
        metadata={"source": "manual", "categoria": "evaluacion_practicas", "role": role}
    ))

    # Chunk 5: Rescisión de prácticas
    docs.append(Document(
        page_content=(
            "Rescisión de prácticas: Qué hacer para rescindir una práctica. "
            "Una práctica externa puede ser rescindida en cualquier momento por causas justificadas, según lo establecido en el convenio de cooperación educativa. "
            "La solicitud de rescisión puede ser realizada por la Universitat Politècnica de València, la empresa o entidad colaboradora, o el propio estudiante. "
            "Es obligatorio que todas las partes involucradas informen con suficiente antelación. "
            "Para formalizar la rescisión, debe enviarse el documento correspondiente debidamente cumplimentado y firmado electrónicamente por todas las partes "
            "a la Unidad de Prácticas en Empresa (upe_inf@etsinf.upv.es), preferiblemente en un plazo de 7 días naturales desde la causa de la rescisión. "
            "Este procedimiento está regulado por el Reglamento de Prácticas Externas de la UPV."
        ),
        metadata={"source": "manual", "categoria": "rescision_practicas", "role": role}
    ))

    # Chunk 6: Duración de prácticas
    docs.append(Document(
        page_content=(
            "La dedicación máxima semanal en prácticas externas en la UPV es de 40 horas, según el Reglamento oficial. "
            "No obstante, en la ETSINF se recomienda una dedicación de 20 horas semanales durante el periodo lectivo "
            "y 40 horas en periodo no lectivo, para garantizar la compatibilidad con la carga académica."
        ),
        metadata={"source": "manual", "categoria": "duracion_practicas", "role": role}
    ))

    # Chunk 7: Créditos de prácticas
    docs.append(Document(
        page_content=(
            "Las prácticas curriculares forman parte del plan de estudios oficial y, por tanto, computan créditos ECTS. "
            "En cambio, las prácticas extracurriculares no están integradas en el plan de estudios y, aunque tienen los mismos fines formativos, "
            "no computan créditos. Sin embargo, pueden figurar en el expediente académico como experiencia profesional complementaria."
        ),
        metadata={"source": "manual", "categoria": "creditos_practicas", "role": role}
    ))

    # Chunk 8: Matrícula y ajustes
    docs.append(Document(
        page_content=(
            "Matrícula y ajustes: En los grados simples de la Universitat Politècnica de València (UPV), donde existe optatividad, es posible cambiar asignaturas optativas por prácticas curriculares. "
            "Este cambio se realiza mediante un ajuste de matrícula desde la Secretaría virtual: Solicitudes > Solicitud Baja de Matrícula > Baja parcial > Ajuste prácticas externas. "
            "Este ajuste también permite hacer el cambio inverso, es decir, dar de baja las prácticas externas y matricular asignaturas optativas. "
            "En cambio, en los dobles grados que no contemplan optatividad, no es posible realizar este tipo de sustituciones."
        ),
        metadata={"source": "manual", "categoria": "matricula_ajustes", "role": role}
    ))

    # Chunk 9: Plazos de verano
    docs.append(Document(
        page_content=(
            "Prácticas en verano: En la ETSINF de la Universitat Politècnica de València (UPV), se permite realizar prácticas externas durante el verano, siempre que el estudiante no se haya titulado antes. "
            "El período autorizado para realizar prácticas finaliza el 31 de agosto. "
            "Aunque es posible realizar prácticas durante el mes de agosto, dicho mes se considera inhábil para la tramitación administrativa. "
            "Por tanto, si la práctica comienza entre el 26 de julio y el 10 de septiembre, la documentación debe entregarse como fecha límite el 16 de julio. "
            "Esta regla específica prevalece sobre el requisito general de entregar la documentación con al menos 10 días de antelación. "
            "Es decir, si una práctica tiene fecha de inicio el 28 de julio o el 10 de agosto, la tramitación también debe haberse completado antes del 16 de julio."
        ),
        metadata={"source": "manual", "categoria": "plazos_verano", "role": role}
    ))

    # Chunk 10: Compatibilidad con TFG
    docs.append(Document(
        page_content=(
            "Compatibilidad con el TFG y final de titulación: En la ETSINF de la Universitat Politècnica de València (UPV), "
            "los estudiantes pueden realizar prácticas externas mientras no hayan alcanzado las condiciones de titulación. "
            "Esto implica no haber entregado ni superado el Trabajo Fin de Grado (TFG) y no haber evaluado el 100% de los créditos. "
            "En el momento en que se entrega el TFG o se tienen todos los créditos superados, el estudiante debe rescindir el convenio de prácticas. "
            "Por tanto, si estás en el último semestre y solo te queda el TFG, puedes hacer prácticas siempre que no lo hayas entregado ni superado aún."
        ),
        metadata={"source": "manual", "categoria": "compatibilidad_TFG", "role": role}
    ))

    # Chunk 11: Bolsa económica
    docs.append(Document(
        page_content=(
            "Bolsa económica de las prácticas: Según la normativa de la Universitat Politècnica de València (UPV), todas las prácticas externas deben incluir una bolsa económica de ayuda al estudio, "
            "salvo que exista una exención aprobada por la estructura responsable del título y el vicerrectorado con competencia en empleo. "
            "La bolsa mínima establecida por la UPV es de 4,60 euros brutos por hora de práctica. "
            "Antes de firmar el convenio, el estudiante puede negociar directamente con la empresa las condiciones económicas, siempre respetando el mínimo establecido. "
            "Esta bolsa es obligatoria incluso para las prácticas realizadas en la propia UPV."
        ),
        metadata={"source": "manual", "categoria": "bolsa_economica", "role": role}
    ))

    # Chunk 12: Firmas electrónicas
    docs.append(Document(
        page_content=(
            "En los convenios de prácticas, no se permite el uso de firmas manuscritas ni escaneadas. "
            "Es obligatorio que todas las partes firmen el documento mediante firma electrónica reconocida, es decir, utilizando un certificado digital válido. "
            "Este requisito garantiza la autenticidad, integridad y validez legal del convenio. "
            "Firmas electrónicas simples, sin respaldo de un certificado oficial, no serán admitidas. "
            "Una vez firmado el documento, se puede comprobar la validez de las firmas electrónicas a través del portal oficial de la administración electrónica: "
            "https://valide.redsara.es/valide/validarFirma/ejecutar.html"
        ),
        metadata={"source": "manual", "categoria": "firmas", "role": role}
    ))

    # Chunk 13: Prácticas curriculares curso superior
    docs.append(Document(
        page_content=(
            "Los estudiantes matriculados en segundo curso o en cursos superiores de un grado simple de la UPV pueden realizar prácticas curriculares, "
            "siempre que hayan superado completamente todas las asignaturas del primer curso del grado. "
            "Este requisito es obligatorio únicamente para poder acceder a las prácticas curriculares, "
            "pero las prácticas curriculares no son obligatorias en ningún grado de la ETSINF. Su realización es siempre opcional."
        ),
        metadata={"source": "manual", "categoria": "practicas_curriculares", "role": role}
    ))

    # Chunk 14: Prácticas en el extranjero
    docs.append(Document(
        page_content=(
            "La Universitat Politècnica de València (UPV) se encuentra en España, por tanto, la tramitación de prácticas en todos los demás países que no son España, como por ejemplo Francia, Alemania o cualquier país, se considera práctica en el extranjero. "
            "Para este tipo de prácticas, la normativa establece requisitos específicos: la documentación debe entregarse con al menos 30 días de antelación a la fecha de inicio de la práctica. "
            "Además, es obligatorio contratar un seguro privado que cubra la estancia en el extranjero y consultar con la Unidad de Prácticas cualquier particularidad del destino. "
            "Respecto al seguro, es importante mencionar que visites este documento para tener toda la información necesaria: https://www.upv.es/contenidos/siepract/download/17801/"
        ),
        metadata={"source": "manual", "categoria": "practicas_extracurriculares", "role": role}
    ))

    # Chunk 15: Cómo generar un convenio de prácticas
    docs.append( Document(
    page_content=(
        "Generación del convenio: El convenio de cooperación educativa debe generarse, crearse o realizarse a través de la herramienta “Calcula tu práctica” "
        "(https://www.sie.upv.es/meta1b/Piniciocal.aspx?lang=ES). "
        "Esta aplicación permite al estudiante rellenar los datos acordados con la empresa y las demás condiciones de la práctica, como horarios, fechas y bolsa económica. "
        "Una vez cumplimentado, el convenio debe ser firmado electrónicamente por todas las partes implicadas: el representante de la empresa, el tutor o tutora de empresa, el tutor o tutora UPV y el propio estudiante. "
        "Para más información sobre cómo utilizar la herramienta, se puede consultar el manual disponible en la web: "
        "https://www.upv.es/entidades/etsinf/wp-content/uploads/2025/01/Manual-Calculadora-ESTUDIANTES-v4.pdf"
    ),
    metadata={"source": "manual", "categoria": "convenio_calcula_practica"}
    ))

    # Chunk 16: Prácticas extracurriculares
    docs.append(Document(
    page_content=(
        "Requisitos para realizar prácticas extracurriculares: Para poder realizar prácticas extracurriculares en la Universitat Politècnica de València (UPV), "
        "el estudiante debe haber superado al menos el 50% de los créditos de su titulación. "
        "Esto significa que no se pueden realizar prácticas extracurriculares en los primeros cursos del grado o doble grado. "
        "Por ejemplo, en un grado de 4 años no se alcanza el 50% hasta aproximadamente el tercer curso, "
        "y en un doble grado de 5 años no se alcanza hasta haber superado dos años y medio de estudios. "
        "Además, es imprescindible estar matriculado durante todo el periodo de prácticas y no haber finalizado la titulación ni superado el 100% de los créditos."
    ),
    metadata={"source": "manual", "categoria": "practicas_extracurriculares", "role": role}
    ))

    # Chunk 17: Prácticas en la propia UPV
    docs.append(Document(
    page_content=(
        "⚠️ Este procedimiento aplica únicamente a prácticas en las que la Universitat Politècnica de València (UPV) actúa como entidad colaboradora, es decir, cuando la práctica se realiza en una unidad, departamento o servicio de la propia UPV. "
        "🚫 Este procedimiento NO aplica a la mayoría de las prácticas externas realizadas en empresas externas. "
        "Solo en estos casos específicos dentro de la UPV es necesario enviar por email los siguientes 5 documentos correctamente cumplimentados y firmados electrónicamente, al menos 10 días antes del inicio de la práctica: "
        "1) Compromiso presupuestario del responsable, "
        "2) Convenio de prácticas, "
        "3) Documento 'Datos' del estudiante, "
        "4) Documento 'Seguro' del estudiante, "
        "5) Fotocopia del DNI/NIE del estudiante."
    ),
    metadata={"source": "manual", "categoria": "upv_entidad_colaboradora", "role": role}
    ))


    # Chunk 18: Prácticas en empresa externa
    docs.append(Document(
    page_content=(
        "En la Universitat Politècnica de València (UPV), la mayoría de las prácticas externas se realizan en empresas externas (entidades privadas o públicas ajenas a la UPV). "
        "En estos casos, no se requieren los 5 documentos específicos que aplican cuando la UPV actúa como entidad colaboradora. "
        "El procedimiento general consiste en formalizar un convenio de cooperación educativa entre la empresa, el estudiante y la UPV, y designar un tutor o tutora en la empresa. "
        "⚠️ Este es el procedimiento habitual salvo que la práctica se realice en una unidad, departamento o servicio interno de la UPV."
    ),
    metadata={"source": "manual", "categoria": "empresa_externa", "role": role}
    ))

    # Chunk 19: Compatibilidad entre trabajo y prácticas
    docs.append(Document(
    page_content=(
        "Un estudiante puede trabajar y realizar prácticas en la misma empresa o institución, "
        "siempre que las tareas desempeñadas como trabajador no estén relacionadas con los estudios vinculados a la práctica. "
        "Es decir, el contrato laboral y las prácticas deben ser actividades independientes y no solaparse en contenidos o funciones."
    ),
    metadata={
        "source": "manual",
        "categoria": "compatibilidad_trabajo_practicas",
        "role": role
    }
    ))

    # Chunk 20: Prácticas externas simultáneas
    docs.append(Document(
    page_content=(
        "Un estudiante puede realizar prácticas externas simultáneamente en varias empresas o instituciones, "
        "siempre que estas sean compatibles con su carga académica. Además, la suma de las horas de todas las prácticas "
        "no debe superar las 40 horas semanales, ya que este es el límite máximo permitido por la normativa."
    ),
    metadata={"source": "manual", "categoria": "practicas_simultaneas", "role": role}
    ))


    # Chunk 21: Recuperación de días
    docs.append(Document(
    page_content=(
        "La asistencia a exámenes parciales o finales no se considera días a recuperar en las prácticas externas, siempre que esté justificada. "
        "Es decir, no es obligatorio recuperar esas horas si el estudiante falta debido a la realización de pruebas académicas oficiales."
    ),
    metadata={
        "source": "manual",
        "categoria": "recuperacion_dias_examenes",
        "role": role
    }
    ))

    # Chunk 22: Tutor de prácticas
    docs.append(Document(
    page_content=(
        "La figura del tutor de prácticas es independiente del firmante del convenio por parte de la empresa o institución, "
        "por lo que ambas figuras pueden coincidir o no. "
        "Sin embargo, el tutor asignado por la UPV y el tutor designado por la empresa no pueden ser la misma persona en ningún caso."
    ),
    metadata={
        "source": "manual",
        "categoria": "tutores_y_firmantes",
        "role": role
    }
    ))

    # Chunk 23: Programas especiales de prácticas
    docs.append(Document(
        page_content=(
            "Un programa especial para la realización de prácticas es una modalidad gestionada directamente por la UPV que permite a los estudiantes acceder a prácticas específicas en determinadas empresas o instituciones. "
            "Algunos ejemplos de estos programas son: prácticas dentro de la UPV, prácticas en Ford España, becas Santander CRUE CEPYME, prácticas en el Ayuntamiento de Valencia, la Diputación de Valencia o Consellerías."
            "Los requisitos y plazos varían según la convocatoria."
        ),
        metadata={
            "source": "manual",
            "categoria": "programas_especiales_practicas",
            "role": role
        }
    ))

    # Chunk 24: Declaración de la renta para estudiantes en prácticas
    docs.append(Document(
    page_content=(
        "Si un estudiante percibe ingresos por la realización de prácticas externas, debe consultar con la Agencia Tributaria para determinar "
        "si tiene la obligación de presentar la declaración de la renta en función de su situación personal. "
        "Para más información oficial se recomienda visitar www.agenciatributaria.es."
    ),
    metadata={
        "source": "manual",
        "categoria": "declaracion_renta_practicas",
        "role": role
    }
    ))




    return docs
