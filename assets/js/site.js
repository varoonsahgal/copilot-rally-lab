/* Rally Lab - site interactions (no dependencies) */
(function () {
  const store = {
    get: (k) => { try { return localStorage.getItem("rally:" + k); } catch (e) { return null; } },
    set: (k, v) => { try { localStorage.setItem("rally:" + k, v); } catch (e) {} },
    del: (k) => { try { localStorage.removeItem("rally:" + k); } catch (e) {} },
    keys: () => { try { return Object.keys(localStorage).filter((k) => k.startsWith("rally:")).map((k) => k.slice(6)); } catch (e) { return []; } },
  };
  window.RallyStore = store;

  /* nav toggle */
  const tog = document.querySelector(".nav-toggle");
  if (tog) tog.addEventListener("click", () => document.querySelector(".nav").classList.toggle("open"));

  /* copy buttons */
  document.querySelectorAll(".prompt").forEach((p) => {
    const btn = p.querySelector(".copy-btn");
    const pre = p.querySelector("pre");
    if (!btn || !pre) return;
    btn.addEventListener("click", async () => {
      const text = pre.innerText.trim();
      try { await navigator.clipboard.writeText(text); }
      catch (e) {
        const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select();
        document.execCommand("copy"); ta.remove();
      }
      btn.textContent = "Copied ✓"; btn.classList.add("copied");
      setTimeout(() => { btn.textContent = "Copy"; btn.classList.remove("copied"); }, 1600);
    });
  });

  /* step check-offs */
  const page = document.body.dataset.page || location.pathname;
  document.querySelectorAll(".step").forEach((step, i) => {
    const key = `step:${page}:${i}`;
    const lab = document.createElement("label");
    lab.className = "done-toggle";
    lab.innerHTML = `<input type="checkbox" aria-label="Mark step ${i + 1} done"> Done`;
    step.appendChild(lab);
    const cb = lab.querySelector("input");
    cb.checked = store.get(key) === "1";
    step.classList.toggle("is-done", cb.checked);
    cb.addEventListener("change", () => {
      cb.checked ? store.set(key, "1") : store.del(key);
      step.classList.toggle("is-done", cb.checked);
      refreshBoards();
    });
  });

  /* generic tracked checkboxes (e.g. errors caught) */
  document.querySelectorAll("input.track[data-key]").forEach((cb) => {
    const key = cb.dataset.key;
    cb.checked = store.get(key) === "1";
    cb.addEventListener("change", () => { cb.checked ? store.set(key, "1") : store.del(key); refreshBoards(); });
  });

  /* lab completion */
  const labId = document.body.dataset.lab;
  const cbtn = document.querySelector("[data-complete]");
  function paintComplete() {
    if (!cbtn) return;
    const done = store.get("lab:" + labId) === "1";
    cbtn.classList.toggle("done", done);
    cbtn.textContent = done ? "Inning complete ✓" : "Mark inning complete";
  }
  if (cbtn) {
    cbtn.addEventListener("click", () => {
      const done = store.get("lab:" + labId) === "1";
      done ? store.del("lab:" + labId) : store.set("lab:" + labId, "1");
      paintComplete(); refreshBoards();
    });
    paintComplete();
  }

  /* scoreboards + lineup state */
  function refreshBoards() {
    document.querySelectorAll("[data-lab-cell]").forEach((td) => {
      const done = store.get("lab:" + td.dataset.labCell) === "1";
      td.textContent = done ? "1" : "0";
      td.classList.toggle("done", done);
    });
    document.querySelectorAll(".scoreboard").forEach((sb) => {
      const sess = sb.dataset.session;
      sb.querySelectorAll("tr[data-row]").forEach((tr) => {
        const s = tr.dataset.row;
        const runs = [...tr.querySelectorAll("[data-lab-cell]")].filter((td) => td.classList.contains("done")).length;
        const hits = store.keys().filter((k) => k.startsWith(`step:s${s}-`)).length;
        const errs = store.keys().filter((k) => k.startsWith(`catch:s${s}`)).length;
        const r = tr.querySelector("[data-r]"), h = tr.querySelector("[data-h]"), e = tr.querySelector("[data-e]");
        if (r) r.textContent = runs; if (h) h.textContent = hits; if (e) e.textContent = errs;
      });
    });
    document.querySelectorAll("[data-lab-link]").forEach((a) => {
      a.classList.toggle("done", store.get("lab:" + a.dataset.labLink) === "1");
    });
  }
  window.refreshBoards = refreshBoards;
  refreshBoards();
  document.querySelectorAll("[data-reset]").forEach((b) => b.addEventListener("click", () => {
    store.keys().filter((k) => !b.dataset.reset || k.includes(b.dataset.reset)).forEach((k) => store.del(k)); location.reload();
  }));

  /* tabs */
  document.querySelectorAll(".tabs").forEach((tabs) => {
    const btns = tabs.querySelectorAll(".tab-list button");
    const panels = tabs.querySelectorAll(".tab-panel");
    btns.forEach((b, i) => b.addEventListener("click", () => {
      btns.forEach((x, j) => x.setAttribute("aria-selected", i === j ? "true" : "false"));
      panels.forEach((p, j) => (p.hidden = i !== j));
    }));
  });

  /* toc highlight */
  const tocLinks = [...document.querySelectorAll(".toc a")];
  if (tocLinks.length && "IntersectionObserver" in window) {
    const map = new Map(tocLinks.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { tocLinks.forEach((a) => a.classList.remove("on")); const a = map.get(en.target.id); if (a) a.classList.add("on"); }
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    map.forEach((_, id) => { const el = document.getElementById(id); if (el) io.observe(el); });
  }
})();

/* ---------------- tiny SVG chart kit ---------------- */
window.RallyChart = (function () {
  const NS = "http://www.w3.org/2000/svg";
  let tip;
  function tipEl() {
    if (!tip) { tip = document.createElement("div"); tip.className = "chart-tip"; document.body.appendChild(tip); }
    return tip;
  }
  function showTip(e, html) { const t = tipEl(); t.innerHTML = html; t.style.opacity = 1; t.style.left = e.clientX + 14 + "px"; t.style.top = e.clientY + 14 + "px"; }
  function hideTip() { if (tip) tip.style.opacity = 0; }
  function el(name, attrs, parent) { const n = document.createElementNS(NS, name); for (const k in attrs) n.setAttribute(k, attrs[k]); if (parent) parent.appendChild(n); return n; }
  const fmt = (v) => (v == null ? "-" : v.toLocaleString("en-US"));
  function niceMax(v) { const p = Math.pow(10, Math.floor(Math.log10(v))); const m = v / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p; }
  function compact(v) { return v >= 1e6 ? (v / 1e6).toFixed(v % 1e6 ? 1 : 0) + "M" : v >= 1e3 ? (v / 1e3).toFixed(v % 1e3 ? 1 : 0) + "K" : String(v); }

  /** Horizontal grouped bars. cfg: {categories, series:[{name,color,values}], format, labelSeries, ref:{value,label}} */
  function hbars(root, cfg) {
    root.innerHTML = "";
    const W = root.clientWidth || 700, rowH = 18, gap = 2, groupPad = 18, left = cfg.left || 170, right = 70, top = 26;
    const n = cfg.series.length, groupH = n * rowH + (n - 1) * gap;
    const H = top + cfg.categories.length * (groupH + groupPad) + 10;
    const all = cfg.series.flatMap((s) => s.values).concat(cfg.ref ? [cfg.ref.value] : []);
    const max = cfg.max || niceMax(Math.max(...all));
    const x = (v) => left + (Math.max(0, v) / max) * (W - left - right);
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": cfg.aria || "bar chart" }, root);
    const g = el("g", { class: "grid" }, svg);
    for (let i = 0; i <= 4; i++) {
      const v = (max / 4) * i, xx = x(v);
      el("line", { x1: xx, x2: xx, y1: top - 8, y2: H - 6 }, g);
      const t = el("text", { x: xx, y: 12, "text-anchor": "middle", class: "lbl-muted" }, svg); t.textContent = cfg.format ? cfg.format(v, true) : compact(v);
    }
    if (cfg.ref) {
      const xx = x(cfg.ref.value);
      el("line", { x1: xx, x2: xx, y1: top - 8, y2: H - 6, stroke: "#16161A", "stroke-width": 1.5 }, svg);
    }
    cfg.categories.forEach((c, ci) => {
      const y0 = top + ci * (groupH + groupPad);
      const lab = el("text", { x: left - 12, y: y0 + groupH / 2 + 4, "text-anchor": "end", "font-weight": 600 }, svg);
      lab.textContent = c;
      cfg.series.forEach((s, si) => {
        const v = s.values[ci]; if (v == null) return;
        const y = y0 + si * (rowH + gap), w = Math.max(2, x(v) - left);
        const r = Math.min(4, w / 2);
        const path = `M${left},${y} H${left + w - r} Q${left + w},${y} ${left + w},${y + r} V${y + rowH - r} Q${left + w},${y + rowH} ${left + w - r},${y + rowH} H${left} Z`;
        const p = el("path", { d: path, fill: s.color }, svg);
        const hit = el("rect", { x: left, y: y - 1, width: W - left - right + 40, height: rowH + 2, fill: "transparent" }, svg);
        const html = `<b>${c}</b><br>${s.name}: ${cfg.format ? cfg.format(v) : fmt(v)}` + (s.notes && s.notes[ci] ? `<br><span style="opacity:.8">${s.notes[ci]}</span>` : "");
        [p, hit].forEach((m) => { m.addEventListener("mousemove", (e) => showTip(e, html)); m.addEventListener("mouseleave", hideTip); });
        if (!cfg.labelSeries || cfg.labelSeries.includes(si)) {
          const t = el("text", { x: left + w + 6, y: y + rowH / 2 + 4, "font-size": 11.5 }, svg);
          t.textContent = cfg.format ? cfg.format(v) : fmt(v);
        }
      });
    });
    return svg;
  }
  return { hbars, fmt, compact };
})();

/* ---------------- v2 engagement layer ---------------- */
(function () {
  const store = window.RallyStore;

  /* call your shot */
  document.querySelectorAll(".shot").forEach((shot) => {
    const key = shot.dataset.key, opts = [...shot.querySelectorAll(".opt")], why = shot.querySelector(".shot-why");
    function reveal(i, animate) {
      opts.forEach((o, j) => {
        o.disabled = true;
        if (o.dataset.correct === "1") o.classList.add("right");
        else if (j === i) o.classList.add("wrong");
      });
      const ok = opts[i] && opts[i].dataset.correct === "1";
      why.querySelector(".verdict").textContent = ok ? "Called it!" : "Not quite.";
      why.hidden = false;
      if (!animate) why.style.animation = "none";
    }
    opts.forEach((o, i) => o.addEventListener("click", () => { store.set(key, String(i)); reveal(i, true); }));
    const saved = store.get(key);
    if (saved !== null) reveal(+saved, false);
  });

  /* sorter drills */
  document.querySelectorAll(".sorter").forEach((sorter) => {
    const key = sorter.dataset.key, items = [...sorter.querySelectorAll(".sort-item")];
    const score = sorter.querySelector(".sort-score"), done = sorter.querySelector(".sort-done");
    function update() {
      const answered = items.filter((it) => it.dataset.chosen).length;
      const right = items.filter((it) => it.classList.contains("is-right")).length;
      score.textContent = `${answered} / ${items.length} sorted · ${right} correct`;
      if (answered === items.length) {
        const pct = right / items.length;
        const msg = pct === 1 ? "Perfect game. You read evidence like an umpire." : pct >= .7 ? "Solid at-bat. Check the ones you missed. They're the ones Copilot misses too." : "Tough inning. Re-read the misses: this is exactly the trap AI summaries fall into.";
        done.innerHTML = `<span>${right}/${items.length}</span>${msg}`;
        done.hidden = false;
      } else done.hidden = true;
    }
    function choose(it, cat) {
      const ans = it.dataset.answer;
      it.dataset.chosen = cat;
      it.querySelectorAll(".sort-btns button").forEach((b) => {
        b.disabled = true;
        if (b.dataset.cat === cat) b.classList.add(cat === ans ? "right" : "wrong");
        else if (b.dataset.cat === ans) b.classList.add("answer");
      });
      it.classList.add(cat === ans ? "is-right" : "is-wrong");
      const fb = it.querySelector(".sort-fb");
      fb.querySelector("b").textContent = cat === ans ? "Correct." : `Actually: ${ans}.`;
      fb.hidden = false;
    }
    items.forEach((it, i) => {
      it.querySelectorAll(".sort-btns button").forEach((b) => b.addEventListener("click", () => {
        store.set(`${key}:${i}`, b.dataset.cat); choose(it, b.dataset.cat); update();
      }));
      const saved = store.get(`${key}:${i}`);
      if (saved) choose(it, saved);
    });
    sorter.querySelector(".sort-reset").addEventListener("click", () => {
      items.forEach((it, i) => {
        store.del(`${key}:${i}`); delete it.dataset.chosen; it.classList.remove("is-right", "is-wrong");
        it.querySelectorAll(".sort-btns button").forEach((b) => { b.disabled = false; b.className = ""; });
        it.querySelector(".sort-fb").hidden = true;
      });
      update();
    });
    update();
  });

  /* base path dots */
  function paintPath() {
    document.querySelectorAll("[data-lab-dot]").forEach((r) => r.classList.toggle("done", store.get("lab:" + r.dataset.labDot) === "1"));
  }
  paintPath();

  /* celebration on inning complete */
  const cbtn = document.querySelector("[data-complete]");
  if (cbtn) cbtn.addEventListener("click", () => {
    paintPath();
    if (store.get("lab:" + document.body.dataset.lab) !== "1") return;
    const s = document.body.dataset.lab.slice(1, 2);
    const total = document.querySelectorAll(".lineup-nav a").length;
    const doneCount = [...document.querySelectorAll(".lineup-nav a")].filter((a) => store.get("lab:" + a.dataset.labLink) === "1").length;
    const t = document.createElement("div");
    t.className = "toast";
    t.innerHTML = `<span class="ball">⚾</span><div><b>${doneCount === total ? "Ballgame! Game " + s + " complete." : "That's a run!"}</b><br>${doneCount} of ${total} innings in the books.</div>`;
    document.body.appendChild(t);
    requestAnimationFrame(() => t.classList.add("show"));
    setTimeout(() => { t.classList.remove("show"); setTimeout(() => t.remove(), 400); }, 3200);
  });

  /* reading progress in lineup bar */
  const bar = document.querySelector(".lineup-progress i"), content = document.querySelector(".lab-content");
  if (bar && content) {
    const onScroll = () => {
      const r = content.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, (window.innerHeight * 0.4 - r.top) / r.height));
      bar.style.width = (p * 100).toFixed(1) + "%";
    };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  /* scroll reveal */
  const targets = document.querySelectorAll(".lab-content > section, .band .card, .ticket, .lab-row, .bcard, .tool, .email, .road .stop, .player, .stat");
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -6% 0px" });
    targets.forEach((el) => { el.classList.add("rv"); io.observe(el); });
  }
})();
