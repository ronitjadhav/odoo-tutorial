/* Zero to Odoo Expert — quizzes, chapter progress, streak.
   All state lives in localStorage; no accounts, no backend. */
(function () {
  'use strict';

  // ponytail: 40 hardcoded; bump if the syllabus ever changes
  var TOTAL = 40;
  var KEY = 'z2oe-progress';

  /* ---- pure helpers (also exercised by tests/quiz.test.mjs) ---- */

  // Quiz source format, one block per ```quiz fence:
  //   Q: question text?
  //   - wrong option
  //   + correct option
  //   > explanation shown after answering
  function parseQuiz(text) {
    var questions = [];
    var q = null;
    text.split('\n').forEach(function (raw) {
      var line = raw.trim();
      if (line.indexOf('Q:') === 0) {
        q = { text: line.slice(2).trim(), options: [], explanation: '' };
        questions.push(q);
      } else if (!q) {
        return;
      } else if (line.indexOf('+ ') === 0) {
        q.options.push({ text: line.slice(2), correct: true });
      } else if (line.indexOf('- ') === 0) {
        q.options.push({ text: line.slice(2), correct: false });
      } else if (line.indexOf('> ') === 0) {
        q.explanation += (q.explanation ? ' ' : '') + line.slice(2);
      }
    });
    return questions;
  }

  // consecutive days ending at `today` (YYYY-MM-DD strings)
  function streakFrom(days, today) {
    var n = 0;
    var d = new Date(today + 'T12:00:00Z');
    while (days.indexOf(d.toISOString().slice(0, 10)) !== -1) {
      n++;
      d.setUTCDate(d.getUTCDate() - 1);
    }
    return n;
  }

  var root = typeof window !== 'undefined' ? window : globalThis;
  root.__z2oe = { parseQuiz: parseQuiz, streakFrom: streakFrom };
  if (typeof document === 'undefined') return; // loaded by the node self-check

  /* ---- state ---- */

  var state = JSON.parse(localStorage.getItem(KEY) || '{"done":{},"days":[]}');
  function save() { localStorage.setItem(KEY, JSON.stringify(state)); }

  var today = new Date().toISOString().slice(0, 10);
  if (state.days.indexOf(today) === -1) {
    state.days.push(today);
    state.days = state.days.slice(-366);
    save();
  }

  function chapterId() {
    var m = location.pathname.match(/\/(\d{2})-[^\/]+\/?$/);
    return m ? m[1] : null;
  }

  /* ---- header pill: progress + streak ---- */

  var pill;
  function renderPill() {
    var done = Object.keys(state.done).length;
    var s = streakFrom(state.days, today);
    pill.textContent = done + '/' + TOTAL + (s > 1 ? ' · 🔥 ' + s : '');
    pill.title = done + ' of ' + TOTAL + ' chapters complete' +
      (s > 1 ? ' — ' + s + '-day streak' : '');
  }

  /* ---- quizzes ---- */

  function renderQuizzes() {
    document.querySelectorAll('pre.quiz, div.quiz').forEach(function (block) {
      var questions = parseQuiz(block.textContent);
      if (!questions.length) return;
      var box = document.createElement('div');
      box.className = 'z2oe-quiz';
      questions.forEach(function (q) {
        var qd = document.createElement('div');
        qd.className = 'z2oe-q';
        var p = document.createElement('p');
        p.className = 'z2oe-qtext';
        p.textContent = q.text;
        qd.appendChild(p);
        var fb = document.createElement('p');
        fb.className = 'z2oe-fb';
        q.options.forEach(function (o) {
          var b = document.createElement('button');
          b.type = 'button';
          b.textContent = o.text;
          b.addEventListener('click', function () {
            var buttons = qd.querySelectorAll('button');
            buttons.forEach(function (x, i) {
              x.disabled = true;
              if (q.options[i].correct) x.classList.add('ok');
            });
            if (!o.correct) b.classList.add('no');
            fb.textContent = (o.correct ? '✔ Correct. ' : '✘ Not quite. ') + q.explanation;
            fb.classList.add(o.correct ? 'ok' : 'no');
          });
          qd.appendChild(b);
        });
        qd.appendChild(fb);
        box.appendChild(qd);
      });
      block.replaceWith(box);
    });
  }

  /* ---- mark-complete button on chapter pages ---- */

  function renderComplete(ch) {
    var article = document.querySelector('article.md-content__inner');
    if (!article) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'z2oe-done md-button';
    function label() {
      b.textContent = state.done[ch] ? '✔ Chapter complete — undo' : 'Mark chapter complete';
      b.classList.toggle('is-done', !!state.done[ch]);
    }
    b.addEventListener('click', function () {
      if (state.done[ch]) delete state.done[ch];
      else state.done[ch] = today;
      save();
      label();
      renderPill();
    });
    label();
    article.appendChild(b);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var header = document.querySelector('.md-header__inner');
    if (header) {
      pill = document.createElement('span');
      pill.className = 'z2oe-pill';
      header.appendChild(pill);
      renderPill();
    }
    renderQuizzes();
    var ch = chapterId();
    if (ch) renderComplete(ch);
  });
})();
