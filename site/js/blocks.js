/* Five Blocks: chain verification and the labs. All hashing uses the browser's Web Crypto. */
(function () {
  "use strict";
  var enc = new TextEncoder();
  var $ = function (id) { return document.getElementById(id); };

  function hex(buf) {
    return Array.prototype.map.call(new Uint8Array(buf), function (b) { return b.toString(16).padStart(2, "0"); }).join("");
  }
  function sha256(bytes) { return crypto.subtle.digest("SHA-256", bytes).then(hex); }
  function concat(parts) {
    var n = parts.reduce(function (a, p) { return a + p.length; }, 0), out = new Uint8Array(n), o = 0;
    parts.forEach(function (p) { out.set(p, o); o += p.length; });
    return out;
  }
  function fromHex(h) { var a = new Uint8Array(h.length / 2); for (var i = 0; i < a.length; i++) a[i] = parseInt(h.substr(i * 2, 2), 16); return a; }
  function short(h) { return h.slice(0, 10) + "…" + h.slice(-6); }
  var cryptoOk = !!(window.crypto && crypto.subtle);

  /* home: recompute the whole chain from the payload files */
  var verify = $("verify");
  if (verify) {
    var blocks = JSON.parse($("manifest").textContent);
    var out = $("verify-out");
    verify.addEventListener("click", function () {
      if (!cryptoOk) { out.textContent = "This browser can't run Web Crypto here (it needs a secure https page)."; return; }
      verify.disabled = true;
      out.innerHTML = "<p>Fetching payloads and hashing…</p>";
      var prev = "0".repeat(64), log = [];
      var rows = function () {
        return '<ol class="vrows">' + log.map(function (r) {
          return '<li class="' + (r.ok ? "ok" : "bad") + '"><span class="mono">#' + r.i + '</span><span class="mono vh">' + short(r.h) + "</span><span>" + (r.ok ? "✓ matches" : "× expected " + short(r.want)) + "</span></li>";
        }).join("") + "</ol>";
      };
      var say = function (head, body) { out.innerHTML = '<p class="vhead">' + head + "</p>" + (body || ""); };
      blocks.reduce(function (p, b, i) {
        return p.then(function () {
          return Promise.all(b.files.map(function (f) {
            return fetch("data/" + f, { cache: "no-store" }).then(function (r) { if (!r.ok) throw new Error(f + ": HTTP " + r.status); return r.arrayBuffer(); });
          })).then(function (bufs) {
            var payload = concat([enc.encode(prev)].concat(bufs.map(function (x) { return new Uint8Array(x); })));
            return sha256(payload).then(function (h) {
              var ok = h === b.hash && prev === b.prev;
              var st = document.querySelector('[data-state="' + i + '"]');
              st.className = "state " + (ok ? "ok" : "bad");
              log.push({ i: i, h: h, ok: ok, want: b.hash });
              prev = h;
              if (!ok) throw new Error("Block #" + i + " does not match.");
            });
          });
        });
      }, Promise.resolve()).then(function () {
        say("Chain intact · 5 of 5 blocks verified", rows());
      }).catch(function (err) {
        say(err.name === "TypeError" ? "Couldn't fetch the payloads. Open the site from a web server, not a local file." : err.message + " Every later block depends on it.", rows());
      }).then(function () { verify.disabled = false; });
    });
  }

  /* SHA-256 playground */
  var hin = $("h-in");
  if (hin) {
    var hrun = function () {
      if (!cryptoOk) { $("h-out").textContent = "Web Crypto is unavailable on this page."; return; }
      sha256(enc.encode(hin.value)).then(function (h) { $("h-out").textContent = h; });
    };
    hin.addEventListener("input", hrun); hrun();
  }

  /* Merkle tree with RFC 6962 domain separation: leaf = H(0x00 || data), node = H(0x01 || left || right) */
  var tree = $("mk-tree");
  if (tree && cryptoOk) {
    var leafInputs = document.querySelectorAll("[data-leaf]");
    var names = ["A", "B", "C", "D"];
    var mrun = function () {
      var pick = +document.querySelector('input[name="mk-proof"]:checked').value;
      Promise.all(Array.prototype.map.call(leafInputs, function (inp) {
        return sha256(concat([new Uint8Array([0]), enc.encode(inp.value)]));
      })).then(function (L) {
        return Promise.all([
          sha256(concat([new Uint8Array([1]), fromHex(L[0]), fromHex(L[1])])),
          sha256(concat([new Uint8Array([1]), fromHex(L[2]), fromHex(L[3])]))
        ]).then(function (N) {
          return sha256(concat([new Uint8Array([1]), fromHex(N[0]), fromHex(N[1])])).then(function (R) {
            var sib = pick ^ 1, parent = pick >> 1, uncle = parent ^ 1;
            var node = function (label, h, cls) {
              return '<div class="mk-node ' + cls + '"><span class="lbl">' + label + '</span><span class="hv" title="' + h + '">' + h + "</span></div>";
            };
            var edges = function (cls, n) { var s = ""; for (var k = 0; k < n; k++) s += "<span></span>"; return '<div class="mk-edges ' + cls + '" aria-hidden="true">' + s + "</div>"; };
            tree.innerHTML =
              '<div class="mk-row l0">' + node("Root", R, "root path") + "</div>" + edges("e1", 1) +
              '<div class="mk-row l1">' + N.map(function (h, i) {
                return node(i ? "Hash CD" : "Hash AB", h, i === parent ? "path" : i === uncle ? "proof" : "");
              }).join("") + "</div>" + edges("e2", 2) +
              '<div class="mk-row l2">' + L.map(function (h, i) {
                return node("Leaf " + names[i], h, i === pick ? "path" : i === sib ? "proof" : "");
              }).join("") + "</div>" +
              '<p class="mk-key"><span><i class="kp"></i>Proof for record ' + names[pick] + ": 2 hashes</span><span><i></i>Path you recompute</span></p>";
          });
        });
      });
    };
    document.querySelectorAll("[data-leaf], input[name='mk-proof']").forEach(function (el) { el.addEventListener("input", mrun); el.addEventListener("change", mrun); });
    mrun();
  }

  /* Byzantine generals: n >= 3f + 1 */
  var gn = $("g-n"), gf = $("g-f");
  if (gn) {
    var grun = function () {
      var n = +gn.value, f = +gf.value;
      if (f > n) { f = n; gf.value = n; }
      gf.max = n;
      $("g-n-out").textContent = n; $("g-f-out").textContent = f;
      var maxF = Math.floor((n - 1) / 3), ok = f <= maxF;
      var dots = "";
      for (var i = 0; i < n; i++) dots += '<i class="' + (i >= n - f ? "t" : "") + '"></i>';
      $("g-dots").innerHTML = dots;
      $("g-out").textContent = n + " generals can survive up to " + maxF + " traitor" + (maxF === 1 ? "" : "s") + ". " +
        (ok ? "With " + f + ", agreement is possible." : "With " + f + ", the traitors can stop agreement: you need at least " + (3 * f + 1) + " generals.");
    };
    gn.addEventListener("input", grun); gf.addEventListener("input", grun); grun();
  }

  /* EIP-1559 fee */
  var gu = $("gas-used");
  if (gu) {
    var fmt = function (x) { return x.toLocaleString("en-US", { maximumFractionDigits: 9 }); };
    var frun = function () {
      var used = +gu.value, base = +$("gas-base").value, tip = +$("gas-tip").value;
      if (!(used >= 0) || !(base >= 0) || !(tip >= 0)) { $("gas-out").textContent = "Enter numbers of zero or more."; return; }
      var total = used * (base + tip);
      $("gas-out").textContent = fmt(used) + " × (" + fmt(base) + " + " + fmt(tip) + ") gwei = " + fmt(total) + " gwei = " +
        fmt(total / 1e9) + " ETH. Burned: " + fmt(used * base) + " gwei; to the validator: " + fmt(used * tip) + " gwei.";
    };
    ["gas-used", "gas-base", "gas-tip"].forEach(function (id) { $(id).addEventListener("input", frun); }); frun();
  }

  /* oracle median vs mean */
  var liar = $("or-liar");
  if (liar) {
    var honest = [21.1, 21.3, 21.4, 21.4, 21.5, 21.6];
    var lo = -50, hi = 150, pos = function (v) { return ((v - lo) / (hi - lo) * 100) + "%"; };
    var orun = function () {
      var v = +liar.value, all = honest.concat([v]).sort(function (a, b) { return a - b; });
      var median = all[3], mean = all.reduce(function (a, b) { return a + b; }, 0) / all.length;
      $("or-liar-out").textContent = v.toFixed(1);
      var html = "";
      [-50, 0, 50, 100, 150].forEach(function (t) { html += '<span class="tick" style="left:' + pos(t) + '">' + t + "</span>"; });
      honest.forEach(function (h, i) { html += '<span class="nd" style="left:' + pos(h) + ";bottom:" + (8 + i * 9) + 'px"></span>'; });
      html += '<span class="nd liar" style="left:' + pos(v) + '"></span>';
      html += '<span class="mark" style="left:' + pos(median) + '"><span>median</span></span>';
      html += '<span class="mark mean" style="left:' + pos(mean) + '"><span>mean</span></span>';
      $("or-nodes").innerHTML = html;
      $("or-out").textContent = "Median " + median.toFixed(1) + " °C · mean " + mean.toFixed(1) + " °C";
    };
    liar.addEventListener("input", orun); orun();
  }
})();
