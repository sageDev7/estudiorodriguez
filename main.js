/* Kit base sageDev — main.js (sirve para el index y las páginas internas: todo está protegido con «if»). */
(function () {
  "use strict";

  /* ---------- WhatsApp: número único; cada botón .js-wa trae su propio data-msg ---------- */
  var WA_NUMBER = "5493442407239";
  function waUrl(msg) { return "https://wa.me/" + WA_NUMBER + "?text=" + encodeURIComponent(msg); }
  document.querySelectorAll(".js-wa").forEach(function (a) {
    a.href = waUrl(a.getAttribute("data-msg") || "Hola, quisiera hacer una consulta.");
    a.target = "_blank"; a.rel = "noopener";
  });
  /* links a páginas que todavía no existen */
  document.querySelectorAll("[data-soon]").forEach(function (a) { a.addEventListener("click", function (e) { e.preventDefault(); }); });

  var body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- header: transparente arriba, sólido al scrollear ---------- */
  var hdr = document.getElementById("hdr");
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle("sc", window.scrollY > 40); };
    onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- menú mobile: la hamburguesa se transforma en cruz (un solo botón) ---------- */
  var burger = document.getElementById("burger");
  function setNav(open) {
    body.classList.toggle("nav-open", open);
    if (!burger) return;
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  }
  if (burger) {
    burger.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
    var ov = document.getElementById("mnavOv"); if (ov) ov.addEventListener("click", function () { setNav(false); });
    document.querySelectorAll(".mnav a").forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
  }

  /* ---------- reveals (usar .on, no .in, para otros estados) ---------- */
  var items = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- flotante de WhatsApp: se oculta en contacto y footer ---------- */
  var fab = document.getElementById("waFloat");
  if (fab && "IntersectionObserver" in window) {
    var hidden = new Set();
    var fio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) hidden.add(en.target); else hidden.delete(en.target); });
      fab.classList.toggle("hide", hidden.size > 0);
    });
    document.querySelectorAll("#contacto, #ftr").forEach(function (el) { fio.observe(el); });
  }

  /* ---------- formulario: se envía por email (FormSubmit) o por WhatsApp ----------
     Si el proyecto no lleva el botón de WhatsApp, borrar #formWaBtn del HTML: el resto sigue andando.
     El email es obligatorio solo para el envío por email. */
  var form = document.getElementById("contactForm");
  var modal = document.getElementById("okModal");
  if (form) {
    var btn = document.getElementById("formSubmitBtn"), waBtn = document.getElementById("formWaBtn");
    var email = document.getElementById("fEmail"), iframe = document.getElementById("formsubmit-iframe");
    var btnTxt = btn ? btn.textContent : "", sending = false;
    var valid = function (input, porEmail) {
      var v = input.value.trim();
      var ok = input === email ? (v === "" ? !porEmail : /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) : v !== "";
      input.closest(".field").classList.toggle("err", !ok);
      return ok;
    };
    var check = function (porEmail) {
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (i) { if (!valid(i, porEmail)) ok = false; });
      if (email && !valid(email, porEmail)) ok = false;
      if (!ok) { var f = form.querySelector(".field.err input,.field.err select,.field.err textarea"); if (f) f.focus(); }
      return ok;
    };
    form.addEventListener("submit", function (e) {
      /* sin FormSubmit (todavía no hay email): Enter en un campo envía por WhatsApp */
      if (!btn) { e.preventDefault(); if (waBtn) waBtn.click(); return; }
      if (!check(true)) { e.preventDefault(); return; }
      sending = true; btn.disabled = true; btn.textContent = "Enviando...";
    });
    if (waBtn) waBtn.addEventListener("click", function () {
      if (!check(false)) return;
      var val = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ""; };
      var txt = "Hola, soy " + val("fNombre") + "." + (val("fArea") ? " Quisiera hacer una consulta sobre " + val("fArea") + "." : "") +
        "\n\n" + val("fMsg") + "\n\nTeléfono: " + val("fTel") + (val("fEmail") ? "\nEmail: " + val("fEmail") : "");
      window.open(waUrl(txt), "_blank", "noopener");
    });
    form.querySelectorAll("input:not([type=hidden]),select,textarea").forEach(function (i) {
      var re = function () { var f = i.closest(".field"); if (f && f.classList.contains("err")) valid(i, false); };
      i.addEventListener("input", re); i.addEventListener("change", re);
    });
    if (iframe) iframe.addEventListener("load", function () {
      if (!sending) return;
      sending = false; form.reset(); btn.disabled = false; btn.textContent = btnTxt;
      if (modal) modal.classList.add("show");
    });
  }
  if (modal) modal.addEventListener("click", function (e) { if (e.target === modal || e.target.hasAttribute("data-close")) modal.classList.remove("show"); });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    setNav(false); if (modal) modal.classList.remove("show");
  });

  /* ---------- situaciones frecuentes: pestañas por área + caso elegido ---------- */
  var tabs = document.querySelectorAll(".tab"), lista = document.getElementById("oriLista");
  function verCaso(id) {
    var caso = document.getElementById(id); if (!caso || !lista) return;
    document.querySelectorAll(".caso").forEach(function (c) { c.classList.toggle("on", c === caso); });
    lista.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-caso") === id); });
  }
  function verArea(area, caso) {
    if (!lista) return;
    tabs.forEach(function (t) { var on = t.getAttribute("data-tab") === area; t.classList.toggle("on", on); t.setAttribute("aria-selected", on ? "true" : "false"); });
    var primero = null;
    lista.querySelectorAll("li").forEach(function (li) {
      var on = li.getAttribute("data-area") === area; li.hidden = !on;
      if (on && !primero) primero = li.querySelector("button").getAttribute("data-caso");
    });
    verCaso(caso || primero);
  }
  tabs.forEach(function (t) { t.addEventListener("click", function () { verArea(t.getAttribute("data-tab")); }); });
  if (lista) lista.addEventListener("click", function (e) {
    var b = e.target.closest("button"); if (!b) return;
    verCaso(b.getAttribute("data-caso"));
    if (window.innerWidth <= 1024) { var p = document.querySelector(".ori-panel"); if (p) p.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); }
  });
  document.querySelectorAll(".js-tab").forEach(function (a) { a.addEventListener("click", function () { verArea(a.getAttribute("data-tab")); }); });

  /* desde las páginas internas: index.html?caso=c-xxx#situaciones abre ese caso */
  var qCaso = new URLSearchParams(location.search).get("caso");
  if (qCaso && lista) {
    var qBtn = lista.querySelector('[data-caso="' + qCaso + '"]');
    if (qBtn) verArea(qBtn.closest("li").getAttribute("data-area"), qCaso);
  }

  /* ---------- pieza del hero: rota preguntas del feed y abre ese caso ---------- */
  var pieza = document.getElementById("heroPieza"), hpLink = document.getElementById("hpLink");
  if (pieza && hpLink) {
    var rot = [
      ["Der. Laboral", "¿Te pidieron que renuncies <span>para volver a contratarte?</span>", "c-renuncia", "laboral"],
      ["Der. Civil", "Falleció un familiar. <span>¿Dejó bienes o deudas?</span>", "c-herencia", "civil"],
      ["Der. Comercial", "Tu socio toma decisiones sin consultarte. <span>¿Puede hacerlo?</span>", "c-socio", "comercial"],
      ["Der. Laboral", "¿Te llegó un telegrama <span>y no sabés qué hacer?</span>", "c-telegrama", "laboral"],
      ["Der. Comercial", "¿Te rechazaron un cheque <span>y no sabés qué hacer?</span>", "c-cheque", "comercial"],
      ["Der. Civil", "Terminó el contrato. <span>¿Pero no te devuelven el inmueble?</span>", "c-alquiler", "civil"]
    ], ri = 0;
    hpLink.addEventListener("click", function () { verArea(rot[ri][3], rot[ri][2]); });
    if (!reduce) setInterval(function () {
      if (document.hidden) return;
      pieza.classList.add("fade");
      setTimeout(function () {
        ri = (ri + 1) % rot.length;
        document.getElementById("hpArea").textContent = rot[ri][0];
        document.getElementById("hpQ").innerHTML = rot[ri][1];
        var dots = document.querySelectorAll("#hpDots i");
        dots.forEach(function (d, i) { d.classList.remove("on"); d.classList.toggle("done", i < ri); });
        if (dots[ri]) { void dots[ri].offsetWidth; dots[ri].classList.add("on"); }
        pieza.classList.remove("fade");
      }, 500);
    }, 5200);
  }

  var yr = document.getElementById("yr"); if (yr) yr.textContent = new Date().getFullYear();
})();
