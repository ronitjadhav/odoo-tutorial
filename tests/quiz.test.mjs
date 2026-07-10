// node tests/quiz.test.mjs — self-check for the pure logic in tutorial.js
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';

new Function(readFileSync(new URL('../docs/assets/js/tutorial.js', import.meta.url), 'utf8'))();
const { parseQuiz, streakFrom } = globalThis.__z2oe;

const qs = parseQuiz(`
Q: Which field type renders a dropdown?
- Char
+ Selection
- Text
> Selection stores one value from a fixed list.
Q: Second question?
+ Yes
- No
`);
assert.equal(qs.length, 2);
assert.equal(qs[0].options.length, 3);
assert.equal(qs[0].options.filter(o => o.correct).length, 1);
assert.equal(qs[0].options[1].text, 'Selection');
assert.match(qs[0].explanation, /fixed list/);
assert.equal(qs[1].options[0].correct, true);
assert.deepEqual(parseQuiz('no quiz here'), []);

assert.equal(streakFrom(['2026-07-10', '2026-07-09', '2026-07-08'], '2026-07-10'), 3);
assert.equal(streakFrom(['2026-07-10', '2026-07-08'], '2026-07-10'), 1); // gap breaks it
assert.equal(streakFrom([], '2026-07-10'), 0);
assert.equal(streakFrom(['2026-07-09'], '2026-07-10'), 0); // yesterday only, today not recorded

console.log('quiz.test.mjs: all assertions passed');
