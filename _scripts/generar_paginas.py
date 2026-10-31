"""Páginas internas del Estudio Jurídico Rodríguez: estudio + una página por área.
Toma head, header y footer del index (los links #ancla pasan a ./index.html#ancla) y arma cada
página con su contenido como datos. Se puede volver a correr cuando cambia el index.
Después correr generar_extras.py (privacidad/404) y este script vuelve a aplicar sus ajustes con --post.

  python _scripts/generar_paginas.py          páginas internas
  python _scripts/generar_paginas.py --post   ajustes a privacidad/404 tras generar_extras
"""
import re, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent
idx = (D / "index.html").read_text(encoding="utf8")

head_tpl = idx[:idx.index("<title>")]
links_head = idx[idx.index('<link rel="preconnect"'):idx.index("</head>")]
links_head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", links_head, flags=re.S)
top = idx[idx.index("<!-- ============ HEADER ============ -->"):idx.index("<main>")]
f0 = idx.index("<!-- ============ FOOTER ============ -->")
foot = idx[f0:idx.index('<a class="wa-float', f0)]
scripts = idx[idx.index('<a class="wa-float'):idx.index("</body>")]

def interna(s):
    return re.sub(r'href="#(?!")', 'href="./index.html#', s)
top_i, foot_i = interna(top), interna(foot)

WA = "Hola, quisiera hacer una consulta."

def caso_html(cid, on):
    m = re.search(r'<article class="caso[^"]*" id="' + cid + r'">.*?</article>', idx, re.S)
    art = re.sub(r'class="caso[^"]*"', 'class="caso on"' if on else 'class="caso"', m.group(0), count=1)
    return "        " + art

def page(fn, title, desc, body, activo=None):
    t = top_i
    if activo:
        t = t.replace(f'href="./{activo}"', f'href="./{activo}" aria-current="page"')
    html = (head_tpl + f"<title>{title}</title>\n"
            f'<link rel="icon" type="image/png" href="./favicon.png">\n<link rel="apple-touch-icon" href="./favicon.png">\n'
            f'<meta name="description" content="{desc}">\n<meta name="theme-color" content="#18191B">\n'
            f'<meta property="og:type" content="website">\n<meta property="og:locale" content="es_AR">\n'
            f'<meta property="og:site_name" content="Estudio Jurídico Rodríguez">\n<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{desc}">\n<meta property="og:image" content="https://i.imgur.com/oLm8uv9.png">\n'
            f'<meta name="twitter:card" content="summary">\n'
            + links_head + "</head>\n<body>\n\n" + t + "<main>\n" + body + "\n</main>\n\n" + foot_i + scripts + "</body>\n</html>\n")
    (D / fn).write_text(html, encoding="utf8", newline="\n")
    print("ok", fn)

def page_hero(foto, ruta, h1, sub):
    migas = "".join(f'<i class="ti ti-chevron-right" aria-hidden="true"></i><span>{m}</span>' for m in ruta)
    return f'''
<!-- ============ CABECERA (negro + foto B/N, cuñas) ============ -->
<section class="page-hero">
  <div class="page-hero-bg" style="background-image:url(img/{foto})" aria-hidden="true"></div>
  <span class="shard shard-br" aria-hidden="true"></span>
  <span class="dots dots-tl dots-on-dark" aria-hidden="true"></span>
  <div class="wrap">
    <nav class="ruta rise" aria-label="Ruta"><a href="./index.html">Inicio</a>{migas}</nav>
    <h1 class="page-h1 rise d1">{h1}</h1>
    <p class="page-sub rise d2">{sub}</p>
    <div class="hero-ctas rise d3">
      <a class="btn btn-oro js-wa" href="#" data-msg="{WA}">Consultar por WhatsApp</a>
      <a class="btn btn-line" href="./index.html#contacto">Ir al contacto</a>
    </div>
  </div>
</section>
'''

def sec_head(ey, h2, lead=""):
    l = f'\n      <p class="lead">{lead}</p>' if lead else ""
    return f'''    <div class="sec-head reveal">
      <p class="eyebrow eyebrow-doble">{ey}</p>
      <h2 class="h2">{h2}</h2>{l}
    </div>'''

# ---------------------------------------------------------------- ÁREAS
AREAS = {
  "laboral": dict(
    nombre="Derecho laboral", foto="laboral.jpg", ic="ti-briefcase",
    desc="Derecho laboral en Concepción del Uruguay: despidos, indemnizaciones, accidentes de trabajo y asesoramiento a empleadores. Estudio Jurídico Rodríguez, desde 1933.",
    sub="Te asesoramos ante despidos, indemnizaciones, accidentes de trabajo y todo lo vinculado a la relación laboral, desde su inicio hasta su finalización.",
    temas=[("Despidos e indemnizaciones", "Revisamos la liquidación final y reclamamos lo que corresponde según tu antigüedad y tu situación."),
           ("Accidentes y enfermedades laborales", "Reclamos ante la ART y el empleador por accidentes de trabajo, en el trayecto o enfermedades profesionales."),
           ("Trabajo no registrado", "Si trabajás sin registrar o con un sueldo menor al real, te asesoramos para regularizar y reclamar."),
           ("Cambios en las condiciones", "Modificaciones de horario, tareas o sueldo que te perjudican: cuándo podés rechazarlas."),
           ("Telegramas y renuncias", "Redactamos y respondemos telegramas, y te asesoramos antes de firmar una renuncia o un acuerdo."),
           ("Asesoramiento a empleadores", "Contratación, licencias, certificados médicos, sanciones y prevención de juicios laborales.")],
    emp=("Empresas y empleadores", ["Altas y contratos de personal en regla.", "Control de licencias y certificados médicos.", "Sanciones y despidos con el procedimiento correcto.", "Prevención de juicios laborales."]),
    par=("Trabajadores", ["Cálculo y reclamo de indemnizaciones.", "Reclamos ante la ART.", "Respuesta a telegramas y cartas documento.", "Regularización del trabajo no registrado."]),
    casos=[("c-renuncia", "Te pidieron que renuncies para volver a contratarte"), ("c-condiciones", "Te cambiaron las condiciones de trabajo"),
           ("c-telegrama", "Te llegó un telegrama laboral"), ("c-certificado", "Tu empleado presentó un certificado médico")]),
  "civil": dict(
    nombre="Derecho civil", foto="civil.jpg", ic="ti-home",
    desc="Derecho civil en Concepción del Uruguay: sucesiones, contratos, alquileres, daños y perjuicios y familia. Estudio Jurídico Rodríguez, desde 1933.",
    sub="Te acompañamos en sucesiones, contratos, daños y perjuicios y cuestiones de familia, con la seriedad que cada situación necesita.",
    temas=[("Sucesiones", "Inicio y trámite de la sucesión, declaratoria de herederos e inscripción de los bienes."),
           ("Contratos y alquileres", "Redacción y revisión de contratos, reclamos por incumplimiento y desalojos."),
           ("Daños y perjuicios", "Accidentes de tránsito, reclamos a aseguradoras y daños a tu persona o a tus bienes."),
           ("Propiedades", "Compraventas, condominios entre herederos, usurpaciones y defectos de construcción."),
           ("Familia", "Divorcios, cuota alimentaria, régimen de comunicación y acuerdos familiares."),
           ("Cobro de deudas", "Reclamo de sumas de dinero entre particulares, con documento o sin él.")],
    emp=("Empresas", ["Contratos de locación y de servicios.", "Reclamos por daños a la empresa.", "Cobro de deudas.", "Siniestros y reclamos a aseguradoras."]),
    par=("Particulares y familias", ["Sucesiones y herencias.", "Accidentes de tránsito.", "Alquileres y desalojos.", "Cuestiones de familia."]),
    casos=[("c-herencia", "Falleció un familiar y no sabés si dejó bienes o deudas"), ("c-choque", "Te chocaron y el otro no tenía seguro"),
           ("c-alquiler", "Terminó el alquiler y no te devuelven el inmueble"), ("c-condominio", "Heredaste una propiedad con tus hermanos y uno no quiere vender")]),
  "comercial": dict(
    nombre="Derecho comercial", foto="comercial.jpg", ic="ti-building",
    desc="Derecho comercial en Concepción del Uruguay: sociedades, contratos comerciales, conflictos entre socios y cobro de cheques. Estudio Jurídico Rodríguez, desde 1933.",
    sub="Constitución de sociedades, contratos comerciales y resolución de conflictos entre empresas. Asesoramiento para que tu negocio esté protegido.",
    temas=[("Constitución de sociedades", "Te ayudamos a elegir el tipo societario (SAS, SRL, SA) y lo constituimos."),
           ("Contratos comerciales", "Contratos con clientes, proveedores y distribuidores, y alquileres comerciales."),
           ("Conflictos entre socios", "Decisiones sin consulta, falta de información o la salida de un socio."),
           ("Cheques y facturas impagas", "Cheques rechazados, facturas y pagarés: reclamo extrajudicial y vía ejecutiva."),
           ("Incumplimientos", "Proveedores o clientes que no cumplen lo acordado: intimación y reclamo."),
           ("Compra y venta de negocios", "Transferencia de fondos de comercio y control de las deudas anteriores.")],
    emp=("Empresas", ["Constitución y reformas de estatutos.", "Revisión de contratos antes de firmar.", "Cobro de deudas comerciales.", "Conflictos societarios."]),
    par=("Emprendedores", ["Elección del tipo de sociedad.", "Acuerdo entre socios desde el inicio.", "Primeros contratos con proveedores.", "Alquiler del local comercial."]),
    casos=[("c-socio", "Tu socio toma decisiones sin consultarte"), ("c-proveedor", "Tu proveedor no cumplió con la entrega"),
           ("c-cheque", "Te rechazaron un cheque"), ("c-emprender", "Vas a emprender con un socio")]),
}

for k, a in AREAS.items():
    pal = a["nombre"].split()
    h1 = f'{pal[0]} <span class="oro">{pal[1]}.</span>'
    temas = "\n".join(f'''      <article class="tema reveal{' d1' if i % 3 == 1 else ' d2' if i % 3 == 2 else ''}">
        <span class="tema-n">0{i+1}</span>
        <h3>{t}</h3>
        <p>{p}</p>
      </article>''' for i, (t, p) in enumerate(a["temas"]))
    def aud(n, titulo, items, btn, cls):
        lis = "".join(f"<li>{x}</li>" for x in items)
        return f'''      <article class="aud reveal">
        <span class="aud-n" aria-hidden="true">{n}</span>
        <h3>{titulo}</h3>
        <ul class="aud-lista">{lis}</ul>
        <a class="btn {cls} js-wa" href="#" data-msg="Hola, quisiera hacer una consulta de {a['nombre'].lower()} ({titulo.lower()}).">{btn}</a>
      </article>'''
    casos = "\n".join(f'        <li><button{" class=\"on\"" if i == 0 else ""} data-caso="{c}">{q}</button></li>' for i, (c, q) in enumerate(a["casos"]))
    paneles = "\n".join(caso_html(c, i == 0) for i, (c, q) in enumerate(a["casos"]))
    otras = " · ".join(f'<a href="./derecho-{o}.html">{AREAS[o]["nombre"]}</a>' for o in AREAS if o != k)
    body = page_hero(a["foto"], ["Áreas", a["nombre"]], h1, a["sub"]) + f'''
<!-- ============ QUÉ ABARCA (gris) ============ -->
<section class="sec sec-crema">
  <span class="shard shard-bl" aria-hidden="true"></span>
  <span class="cl cl-l" aria-hidden="true"></span>
  <span class="dots dots-tl" aria-hidden="true"></span>
  <span class="dots dots-br" aria-hidden="true"></span>
  <div class="wrap">
{sec_head("Qué abarca", 'Temas en los que <span class="oro">intervenimos.</span>')}
    <div class="temas">
{temas}
    </div>
  </div>
</section>

<!-- ============ PARA QUIÉN (negro) ============ -->
<section class="sec sec-dark asesoramos">
  <span class="shard shard-tr" aria-hidden="true"></span>
  <span class="dots dots-bl dots-on-dark" aria-hidden="true"></span>
  <div class="wrap">
{sec_head("A quién asesoramos", f'Dos miradas, <span class="oro">el mismo cuidado.</span>')}
    <div class="aud-grid">
{aud("I", a["emp"][0], a["emp"][1], "Consultar", "btn-oro")}
{aud("II", a["par"][0], a["par"][1], "Consultar", "btn-line")}
    </div>
  </div>
</section>

<!-- ============ SITUACIONES DEL ÁREA (gris) + consulta ============ -->
<section class="sec sec-crema">
  <span class="shard shard-br" aria-hidden="true"></span>
  <span class="cl cl-l" aria-hidden="true"></span>
  <span class="dots dots-tr" aria-hidden="true"></span>
  <div class="wrap">
{sec_head("Situaciones frecuentes", 'Lo que más <span class="oro">nos consultan.</span>', "Elegí tu caso: te mostramos lo primero que conviene hacer y podés escribirnos con el tema ya planteado.")}
    <div class="ori reveal">
      <div class="ori-col">
      <ul class="ori-lista" id="oriLista">
{casos}
      </ul>
      <p class="ori-nota"><i class="ti ti-info-circle" aria-hidden="true"></i>Información orientativa: cada caso necesita un análisis propio.</p>
      </div>
      <div class="ori-panel">
{paneles}
      </div>
    </div>
    <div class="cta-linea reveal">
      <p><b>¿Tu caso es distinto?</b> Contanos tu situación por WhatsApp y te decimos cómo seguir. <span class="otras">También: {otras}</span></p>
      <div class="cta-btns">
        <a class="btn btn-dark js-wa" href="#" data-msg="Hola, quisiera hacer una consulta de {a['nombre'].lower()}.">Consultar por WhatsApp</a>
      </div>
    </div>
  </div>
</section>
'''
    page(f"derecho-{k}.html", f"{a['nombre']} en Concepción del Uruguay | Estudio Jurídico Rodríguez", a["desc"], body, f"derecho-{k}.html")

# ---------------------------------------------------------------- EL ESTUDIO
estudio = page_hero("pluma.jpg", ["El estudio"], 'Desde <span class="oro">1933.</span>',
                    "Tres generaciones de abogados al servicio de Concepción del Uruguay, en derecho laboral, civil y comercial.") + '''
<!-- ============ GENERACIONES (gris) · Abuelo — Padre — Hijos, de sus piezas ============ -->
<section class="sec sec-crema">
  <span class="shard shard-bl" aria-hidden="true"></span>
  <span class="cl cl-l" aria-hidden="true"></span>
  <span class="dots dots-tl" aria-hidden="true"></span>
  <span class="dots dots-br" aria-hidden="true"></span>
  <div class="wrap">
''' + sec_head("Nuestra historia", 'Tres generaciones, <span class="oro">un mismo compromiso.</span>',
               "Desde ese año acompañamos a Concepción del Uruguay, construyendo confianza generación tras generación.") + '''
    <!-- Si nos pasan los nombres del abuelo fundador y del padre (y años), se suman en cada etapa -->
    <ol class="linea">
      <li class="reveal"><span class="linea-n">1933</span><b>Abuelo</b><p>Funda el estudio y abre sus puertas en Concepción del Uruguay.</p></li>
      <li class="reveal d1"><span class="linea-n">II</span><b>Padre</b><p>Toma la posta, le da continuidad y consolida la confianza de sus clientes.</p></li>
      <li class="reveal d2"><span class="linea-n">Hoy</span><b>Hijos</b><p>La tercera generación, hoy al frente del estudio.</p></li>
    </ol>
  </div>
</section>

<!-- ============ AL FRENTE (negro) · foto con borde diagonal + texto literal de su bio ============ -->
<section class="sec sec-dark foto-diag-sec frente">
  <div class="foto-diag" style="background-image:url(img/hero-firma.jpg)" aria-hidden="true"></div>
  <span class="shard shard-tr" aria-hidden="true"></span>
  <span class="dots dots-bl dots-on-dark" aria-hidden="true"></span>
  <div class="wrap frente-grid">
    <div></div>
    <div class="reveal">
      <p class="eyebrow eyebrow-raya">Quiénes están al frente</p>
      <h2 class="h2">La tercera <span class="oro">generación.</span></h2>
      <p class="frente-txt">Dr. Luis Rodríguez y Dr. Manuel Rodríguez representan hoy la tercera generación al frente del Estudio Jurídico Rodríguez, dedicados al Derecho Laboral, Civil y Comercial. Con el respaldo de más de 90 años de trayectoria familiar, siguen comprometidos con cada caso que los elige.</p>
      <!-- Sumar matrícula y foto de cada uno cuando las pasen -->
      <ul class="bar-list equipo">
        <li><span class="mono" aria-hidden="true">LR</span><div><b>Dr. Luis Rodríguez</b><small>Abogado</small></div></li>
        <li><span class="mono" aria-hidden="true">MR</span><div><b>Dr. Manuel Rodríguez</b><small>Abogado</small></div></li>
      </ul>
    </div>
  </div>
</section>

<!-- ============ CÓMO TRABAJAMOS (gris) + cierre ============ -->
<section class="sec sec-crema">
  <span class="shard shard-br" aria-hidden="true"></span>
  <span class="cl cl-l" aria-hidden="true"></span>
  <span class="dots dots-tr" aria-hidden="true"></span>
  <div class="wrap">
''' + sec_head("Cómo trabajamos", 'Lo que nos <span class="oro">sostiene.</span>') + '''
    <div class="temas temas-3">
      <article class="tema reveal"><span class="tema-n">01</span><h3>Trayectoria</h3><p>Más de 90 años en la ciudad nos dan conocimiento de sus tribunales, sus instituciones y su gente.</p></article>
      <article class="tema reveal d1"><span class="tema-n">02</span><h3>Trato directo</h3><p>Tu consulta la atienden los abogados del estudio, de principio a fin.</p></article>
      <article class="tema reveal d2"><span class="tema-n">03</span><h3>Prevención</h3><p>Preferimos asesorarte antes de que el problema empiece: es más simple y menos costoso.</p></article>
    </div>
    <div class="cta-linea reveal">
      <p><b>¿Querés hacernos una consulta?</b> Escribinos y te respondemos a la brevedad.</p>
      <div class="cta-btns">
        <a class="btn btn-dark js-wa" href="#" data-msg="''' + WA + '''">Consultar por WhatsApp</a>
        <a class="btn btn-line" href="./index.html#contacto">Ir al contacto</a>
      </div>
    </div>
  </div>
</section>
'''
page("estudio.html", "El estudio | Estudio Jurídico Rodríguez, desde 1933 en Concepción del Uruguay",
     "Estudio Jurídico Rodríguez: tres generaciones de abogados en Concepción del Uruguay desde 1933. Hoy, a cargo del Dr. Luis Rodríguez y el Dr. Manuel Rodríguez.",
     estudio, "estudio.html")

# ---------------------------------------------------------------- ajustes a privacidad/404 (después de generar_extras)
if "--post" in sys.argv:
    p = (D / "privacidad.html").read_text(encoding="utf8")
    p = p.replace("nombre, teléfono, email y el mensaje que escribís", "nombre, teléfono, el área de consulta y el mensaje que escribís")
    li = "<li><b>Google Fonts</b> y <b>jsDelivr</b>, que sirven las tipografías y los íconos del sitio.</li>"
    if "Google Maps" not in p:
        p = p.replace(li, li + "\n      <li><b>Google Maps</b>, que muestra el mapa con la ubicación del estudio.</li>")
    p = re.sub(r"<em>(.*?)</em>", r'<span class="oro">\1</span>', p)
    (D / "privacidad.html").write_text(p, encoding="utf8", newline="\n")
    n = (D / "404.html").read_text(encoding="utf8")
    n = re.sub(r"<em>(.*?)</em>", r'<span class="oro">\1</span>', n)
    (D / "404.html").write_text(n, encoding="utf8", newline="\n")
    print("ok post privacidad/404")
