// The dashboard card against the integration: it reads sensor.voeding_status and writes only through baby_feeding actions.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {Window} from 'happy-dom';

const window = new Window({url: 'http://homeassistant.local:8123/dashboard-main/voeding'});
const RealDate = window.Date;
let now = '2026-11-14T14:00:00+01:00';
window.Date = class extends RealDate {
  constructor(...args) { super(...(args.length ? args : [now])); }
  static now() { return new RealDate(now).getTime(); }
};
window.HTMLElement.prototype.scrollIntoView = function () {};
window.eval(fs.readFileSync(new URL('../custom_components/baby_feeding/frontend/baby-feeding-card.js', import.meta.url), 'utf8'));
const Card = window.customElements.get('baby-feeding-card');

const feeds = [
  {uid: 'feed-1', summary: '60 cc', start: '2026-11-14T09:30:47+01:00'},
  {uid: 'feed-2', summary: '70 cc', start: '2026-11-14T12:30:00+01:00'},
];
let status = {
  state: 'opgeslagen',
  attributes: {
    plan: {feed_id: 'feed-2', feed_start: '2026-11-14T12:30:00+01:00', due: '2026-11-14T15:30:00+01:00', alerted: false},
    open_start: null, standaard_cc: 70, maximum_cc: null, nacht_eigen: false, nacht_uren: 4,
    voedingen: feeds.map(feed => ({id: feed.uid, start: feed.start, cc: Number(feed.summary.split(' ')[0])})),
  },
};
const calls = [];
let subscriptions = 0;
let reject = null;
const hass = () => ({
  config: {time_zone: 'Europe/Amsterdam'},
  states: {'sensor.voeding_status': {entity_id: 'sensor.voeding_status', ...structuredClone(status)}},
  connection: {subscribeEvents: async () => { subscriptions++; return () => {}; }},
  callApi: async () => feeds.map(feed => ({uid: feed.uid, summary: feed.summary, start: {dateTime: feed.start}, end: {dateTime: feed.start}})),
  callWS: async request => {
    if (request.type === 'get_states') return [{entity_id: 'sensor.voeding_status', ...structuredClone(status)}];
    calls.push(structuredClone(request));
    if (reject) { const error = reject; reject = null; throw error; }
    return {response: {plan_feed_id: 'feed-3', next_due: null, open_start: null}};
  },
});
const actions = () => calls.filter(call => call.type === 'call_service').map(call => [call.domain + '.' + call.service, call.service_data]);
const input = (card, id, value) => { card.$(id).value = String(value); card.$(id).dispatchEvent(new window.Event('input', {bubbles: true, composed: true})); };

const card = new Card();
card.setConfig({mode: 'main'});
window.document.body.append(card);
card.hass = hass();
await card._refreshAll();

// The clock and the saved view come from the plan in the status sensor.
assert.equal(card.$('countdown').textContent, '01:30:00');
assert.equal(card.$('deadline').textContent, 'om 15:30');
assert.equal(card.$('last-feed').textContent, 'Laatste fles 12:30');
assert.equal(card.$('saved').hidden, false);
assert.match(card.$('saved-meta').textContent, /12:30 · 70 cc/);
assert.equal(card.$('today-total').textContent, '130 cc');
assert.equal(subscriptions, 0, 'the card must not subscribe to custom events; non-admin users are refused');

// A new bottle opens through the integration and the form starts at the opened minute.
await card._startNew(false);
assert.deepEqual(actions().at(-1), ['baby_feeding.new_bottle', {}]);
status = {...status, state: 'open', attributes: {...status.attributes, open_start: '2026-11-14T14:00:00+01:00'}};
card.hass = hass();
assert.equal(card.$('current-form').hidden, false);
assert.equal(card.$('current-time').value, '14:00');
assert.equal(card.$('current-amount').value, '70');

// Saving sends the entered moment and amount; a refusal from the integration is shown and not reported as saved.
input(card, 'current-time', '14:05'); input(card, 'current-amount', 75);
reject = Object.assign(new Error('Er staat al een voeding op deze minuut. Pas die voeding aan of kies de werkelijke begintijd.'), {code: 'service_validation_error'});
await card._saveCurrent();
assert.match(card.$('current-error').textContent, /al een voeding op deze minuut/);
assert.doesNotMatch(card.$('notice').textContent, /Opgeslagen/);
await card._saveCurrent();
assert.deepEqual(actions().at(-1), ['baby_feeding.save_bottle', {start: '2026-11-14T13:05:00.000Z', amount: 75}]);
assert.match(card.$('notice').textContent, /Opgeslagen · 14:05 · 75 cc/);

// A bottle may be saved ahead; the preview says so first.
status = {...status, state: 'open'};
card.hass = hass();
input(card, 'current-time', '14:20');
assert.match(card.$('current-preview').textContent, /^Fles staat 20 min vooruit\. Volgende melding om 17:20/);

// Changing only the amount keeps the exact stored start, including seconds.
const row = uid => card._mapEvents(feeds.map(feed => ({uid: feed.uid, summary: feed.summary, start: {dateTime: feed.start}, end: {dateTime: feed.start}}))).find(item => item.uid === uid);
card._openHistory(row('feed-1'));
card.$('edit-amount').value = '65';
await card._saveHistory();
assert.deepEqual(actions().at(-1), ['baby_feeding.update_feed', {feed_id: 'feed-1', start: '2026-11-14T09:30:47+01:00', amount: 65}]);

// Moving a feed sends the new minute.
card._openHistory(row('feed-1'));
card.$('edit-time').value = '09:40';
await card._saveHistory();
assert.deepEqual(actions().at(-1), ['baby_feeding.update_feed', {feed_id: 'feed-1', start: '2026-11-14T08:40:00.000Z', amount: 60}]);

// An earlier feed goes through add_earlier_feed.
card._openHistory(null);
card.$('edit-date').value = '2026-11-14'; card.$('edit-time').value = '11:00'; card.$('edit-amount').value = '40';
await card._saveHistory();
assert.deepEqual(actions().at(-1), ['baby_feeding.add_earlier_feed', {start: '2026-11-14T10:00:00.000Z', amount: 40}]);

// Settings are saved in one action and confirmed from the status sensor.
const settingsCard = new Card();
settingsCard.setConfig({mode: 'settings'});
window.document.body.append(settingsCard);
settingsCard.hass = hass();
input(settingsCard, 'standard-amount', 80); input(settingsCard, 'maximum-amount', 90);
settingsCard.$('night-toggle').click(); input(settingsCard, 'night-hours', 5);
status = {...status, attributes: {...status.attributes, standaard_cc: 80, maximum_cc: 90, nacht_eigen: true, nacht_uren: 5}};
await settingsCard._saveSettings();
assert.deepEqual(actions().at(-1), ['baby_feeding.set_settings', {standard_amount: 80, maximum_amount: 90, night_custom_enabled: true, night_hours: 5}]);
assert.equal(settingsCard.$('settings-status').textContent, 'Instellingen opgeslagen');

// After the reminder the clock says it is time.
now = '2026-11-14T15:31:00+01:00';
status = {...status, state: 'open', attributes: {...status.attributes, plan: {...status.attributes.plan, alerted: true}, open_start: '2026-11-14T15:30:00+01:00'}};
card.hass = hass();
assert.equal(card.$('countdown').textContent, 'Tijd voor de fles');
assert.equal(card.$('current-time').value, '15:30');

assert.ok(actions().every(([name]) => name.startsWith('baby_feeding.')), 'the card only writes through the integration');
card.remove(); settingsCard.remove();
await window.happyDOM.cancelAsync(); await window.close();
console.log('Card PASS: reads the status sensor and writes only through baby_feeding actions.');
