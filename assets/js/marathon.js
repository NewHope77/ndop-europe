/* ==========================================================================
   Prayer Marathon 28/30 — interactive map module

   Nations are plotted from real coordinates onto a Mercator projection, so the
   map is geographically correct without shipping a country-outline dataset.
   Content (day, focus, status) lives in the DATA array below and is intended
   to be replaced with the movement's own schedule.
   ========================================================================== */
(function () {
  'use strict';

  var map = document.getElementById('marathonMap');
  if (!map) return;

  /* ---------- Data ---------- */
  // status: 'established' | 'progress' | 'open'
  var DATA = [
    { day: 1,  name: 'Ukraine',        lat: 49.0, lon: 31.2, status: 'established',
      note: 'First country in Europe with a National Day of Prayer in law (24 February).',
      focus: ['Peace and a just end to the war', 'Protection for soldiers and the release of prisoners', 'Comfort for the displaced and the bereaved'] },
    { day: 2,  name: 'Poland',         lat: 52.1, lon: 19.4, status: 'progress',
      note: 'Steering committee formed; parliamentary consultations under way.',
      focus: ['Unity among churches and confessions', 'Wisdom for national leaders', 'The generation now growing up'] },
    { day: 3,  name: 'Romania',        lat: 45.9, lon: 24.9, status: 'progress',
      note: 'Interdenominational working group established.',
      focus: ['Continued spiritual renewal', 'Integrity in public life', 'Families and communities'] },
    { day: 4,  name: 'Moldova',        lat: 47.2, lon: 28.5, status: 'progress',
      note: 'Initiative introduced to church leaders.',
      focus: ['Peace and stability', 'Protection of freedom', 'Hope for young people'] },
    { day: 5,  name: 'Hungary',        lat: 47.2, lon: 19.5, status: 'progress',
      note: 'Vision document in preparation.',
      focus: ['Reconciliation and neighbourliness', 'Wisdom for those who govern', 'The strengthening of families'] },
    { day: 6,  name: 'Slovakia',       lat: 48.7, lon: 19.7, status: 'progress',
      note: 'Church leaders consulted; committee forming.',
      focus: ['Unity of the churches', 'Care for the vulnerable', 'Honest and responsible leadership'] },
    { day: 7,  name: 'Czechia',        lat: 49.8, lon: 15.5, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Spiritual renewal', 'Hope for a new generation', 'Peace within society'] },
    { day: 8,  name: 'Austria',        lat: 47.6, lon: 14.1, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Unity across confessions', 'Welcome for the stranger', 'Wisdom for leaders'] },
    { day: 9,  name: 'Germany',        lat: 51.1, lon: 10.4, status: 'progress',
      note: 'Building on the heritage of the Leipzig Peace Prayers.',
      focus: ['Peace in Europe', 'Renewal of faith in public life', 'Reconciliation between peoples'] },
    { day: 10, name: 'Switzerland',    lat: 46.8, lon: 8.2,  status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Wisdom in international mediation', 'Care for the poor', 'Unity of the churches'] },
    { day: 11, name: 'France',         lat: 46.6, lon: 2.4,  status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Social cohesion and mutual respect', 'Wisdom for national leaders', 'Renewal of hope'] },
    { day: 12, name: 'Belgium',        lat: 50.6, lon: 4.6,  status: 'progress',
      note: 'Connected with the European Prayer Breakfast in Brussels.',
      focus: ['European institutions and those who serve in them', 'Peace across the continent', 'Integrity in leadership'] },
    { day: 13, name: 'Netherlands',    lat: 52.2, lon: 5.6,  status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Spiritual renewal', 'Strong families', 'Compassion in public life'] },
    { day: 14, name: 'United Kingdom', lat: 53.5, lon: -1.8, status: 'progress',
      note: 'Heir to the national days of prayer of 1588 and 1940.',
      focus: ['Renewal of the nation’s faith', 'Wisdom for Parliament', 'Peace and security'] },
    { day: 15, name: 'Ireland',        lat: 53.2, lon: -8.0, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Healing of old divisions', 'Hope for young people', 'Strong communities'] },
    { day: 16, name: 'Iceland',        lat: 64.9, lon: -18.6, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Spiritual renewal', 'Care for creation', 'Unity of the churches'] },
    { day: 17, name: 'Norway',         lat: 61.0, lon: 9.0,  status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Wisdom for national leaders', 'Peace in the North', 'Strong families'] },
    { day: 18, name: 'Sweden',         lat: 62.0, lon: 15.0, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Renewal of faith', 'Social cohesion', 'Hope for the young'] },
    { day: 19, name: 'Denmark',        lat: 56.0, lon: 9.5,  status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Unity of the churches', 'Wisdom for leaders', 'Care for the vulnerable'] },
    { day: 20, name: 'Finland',        lat: 63.5, lon: 26.0, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Peace and national security', 'Renewal of faith', 'Strong families'] },
    { day: 21, name: 'Estonia',        lat: 58.7, lon: 25.5, status: 'progress',
      note: 'Heir to the Singing Revolution; consultations under way.',
      focus: ['Freedom and national identity', 'Spiritual revival', 'Peace on the eastern border'] },
    { day: 22, name: 'Latvia',         lat: 56.9, lon: 24.6, status: 'progress',
      note: 'Interdenominational conversations begun.',
      focus: ['Freedom and security', 'Renewal of faith', 'Unity of the people'] },
    { day: 23, name: 'Lithuania',      lat: 55.3, lon: 23.9, status: 'progress',
      note: 'Interdenominational conversations begun.',
      focus: ['Freedom and security', 'Wisdom for leaders', 'Hope for the young'] },
    { day: 24, name: 'Spain',          lat: 40.2, lon: -3.7, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Unity and social solidarity', 'Renewal of faith', 'Care for the unemployed'] },
    { day: 24, name: 'Portugal',       lat: 39.6, lon: -8.0, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Hope and resilience', 'Strong families', 'Wisdom for leaders'] },
    { day: 25, name: 'Italy',          lat: 42.8, lon: 12.6, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Unity of the churches', 'Welcome for the stranger', 'Renewal of public life'] },
    { day: 25, name: 'Croatia',        lat: 45.1, lon: 15.5, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Peace and reconciliation', 'Strong families', 'Hope for the young'] },
    { day: 26, name: 'Serbia',         lat: 44.2, lon: 20.9, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Reconciliation among the peoples of the Balkans', 'Peace', 'Wisdom for leaders'] },
    { day: 27, name: 'Greece',         lat: 39.0, lon: 22.0, status: 'open',
      note: 'A national coordinator is needed.',
      focus: ['Renewal of the nation’s spiritual life', 'Hope in hardship', 'Peace in the region'] },
    { day: 28, name: 'Bulgaria',       lat: 42.7, lon: 25.3, status: 'progress',
      note: 'First conversations with church leaders held.',
      focus: ['Spiritual renewal', 'Integrity in public life', 'Care for the vulnerable'] }
  ];

  /* ---------- Projection (Mercator) ----------
     The background raster is the Europe map from the movement's brochure. Its
     own projection was measured (Iceland and Iberia as control points) and the
     <image> in the markup is placed so that the two projections coincide, which
     is why a plotted lat/lon lands on the right piece of land. Keep the four
     bounds below and the <image> geometry in marathon.html in step.        */
  var VB = { w: 800, h: 865 };
  var LON0 = -25.5, LON1 = 34.1, LAT0 = 34.2, LAT1 = 70.5;
  var merc = function (lat) { return Math.log(Math.tan(Math.PI / 4 + (lat * Math.PI / 180) / 2)); };
  var M0 = merc(LAT0), M1 = merc(LAT1);

  function project(lat, lon) {
    return {
      x: (lon - LON0) / (LON1 - LON0) * VB.w,
      y: (M1 - merc(lat)) / (M1 - M0) * VB.h
    };
  }

  /* ---------- Relay path, in day order ---------- */
  var ordered = DATA.slice().sort(function (a, b) { return a.day - b.day; });
  document.getElementById('relayPath').setAttribute('d',
    ordered.map(function (n, i) {
      var p = project(n.lat, n.lon);
      return (i ? 'L' : 'M') + p.x.toFixed(1) + ' ' + p.y.toFixed(1);
    }).join(' ')
  );

  /* ---------- Nodes ---------- */
  var NS = 'http://www.w3.org/2000/svg';
  var nodesGroup = document.getElementById('mapNodes');
  var nodeEls = {};

  DATA.forEach(function (n, i) {
    var p = project(n.lat, n.lon);
    var g = document.createElementNS(NS, 'g');
    g.setAttribute('class', 'map-node st-' + n.status);
    g.setAttribute('tabindex', '0');
    g.setAttribute('role', 'button');
    g.setAttribute('aria-label', n.name + ' — day ' + n.day);
    g.dataset.index = String(i);

    var halo = document.createElementNS(NS, 'circle');
    halo.setAttribute('class', 'halo');
    halo.setAttribute('cx', p.x); halo.setAttribute('cy', p.y); halo.setAttribute('r', '14');

    var dot = document.createElementNS(NS, 'circle');
    dot.setAttribute('class', 'dot');
    dot.setAttribute('cx', p.x); dot.setAttribute('cy', p.y); dot.setAttribute('r', '5');
    dot.setAttribute('stroke-width', '1.5');

    var hit = document.createElementNS(NS, 'circle');
    hit.setAttribute('cx', p.x); hit.setAttribute('cy', p.y); hit.setAttribute('r', '16');
    hit.setAttribute('fill', 'transparent');

    var flip = p.x > VB.w * 0.66;                 // keep eastern labels inside the frame
    var label = document.createElementNS(NS, 'text');
    label.setAttribute('x', flip ? p.x - 11 : p.x + 11);
    label.setAttribute('y', p.y + 3.5);
    if (flip) label.setAttribute('text-anchor', 'end');
    label.textContent = n.name;

    g.appendChild(halo); g.appendChild(dot); g.appendChild(label); g.appendChild(hit);
    nodesGroup.appendChild(g);
    nodeEls[i] = g;

    var pick = function () { select(i); };
    g.addEventListener('click', pick);
    g.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); }
    });
  });

  /* ---------- List ---------- */
  var list = document.getElementById('countryList');
  var detail = document.getElementById('countryDetail');
  var search = document.getElementById('countrySearch');
  var activeIndex = 0;
  var filter = 'all';

  var LABEL = { established: 'Established', progress: 'Under way', open: 'Open' };

  function renderList() {
    var q = (search.value || '').trim().toLowerCase();
    var html = '';
    var shown = 0;

    ordered.forEach(function (n) {
      var i = DATA.indexOf(n);
      var matchesFilter = filter === 'all' || n.status === filter;
      var matchesQuery = !q || n.name.toLowerCase().indexOf(q) !== -1;
      var visible = matchesFilter && matchesQuery;

      nodeEls[i].classList.toggle('is-dimmed', !visible);
      if (!visible) return;
      shown++;

      html += '<li class="c-item' + (i === activeIndex ? ' is-active' : '') + '" data-index="' + i + '">'
        + '<button type="button">'
        + '<span class="c-day">' + n.day + '<small>Day</small></span>'
        + '<span class="c-name">' + n.name + '<em>' + n.note + '</em></span>'
        + '<span class="pill st-' + n.status + '">' + LABEL[n.status] + '</span>'
        + '</button></li>';
    });

    list.innerHTML = shown
      ? html
      : '<li class="c-item"><div style="padding:22px 16px;color:var(--muted);font-size:.92rem">No nation matches that search.</div></li>';
  }

  function renderDetail() {
    var n = DATA[activeIndex];
    detail.innerHTML =
      '<h3>' + n.name + '</h3>'
      + '<p class="detail__meta">Day ' + n.day + ' of 28 · ' + LABEL[n.status] + '</p>'
      + '<p>' + n.note + '</p>'
      + '<ul class="detail__focus">' + n.focus.map(function (f) { return '<li>' + f + '</li>'; }).join('') + '</ul>';
  }

  function select(i) {
    activeIndex = i;
    Object.keys(nodeEls).forEach(function (k) {
      nodeEls[k].classList.toggle('is-active', Number(k) === i);
    });
    renderList();
    renderDetail();
  }

  list.addEventListener('click', function (e) {
    var li = e.target.closest('.c-item[data-index]');
    if (li) select(Number(li.dataset.index));
  });

  search.addEventListener('input', renderList);

  document.getElementById('filters').addEventListener('click', function (e) {
    var chip = e.target.closest('.chip');
    if (!chip) return;
    filter = chip.dataset.filter;
    this.querySelectorAll('.chip').forEach(function (c) { c.classList.toggle('is-active', c === chip); });
    renderList();
  });

  /* ---------- Counts ---------- */
  var counts = DATA.reduce(function (acc, n) { acc[n.status]++; acc.all++; return acc; },
    { all: 0, established: 0, progress: 0, open: 0 });
  document.getElementById('cAll').textContent = counts.all;
  document.getElementById('cEst').textContent = counts.established;
  document.getElementById('cProg').textContent = counts.progress;
  document.getElementById('cOpen').textContent = counts.open;

  select(0);
})();
