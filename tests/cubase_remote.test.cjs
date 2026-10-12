// Host mock: validates bridge behavior, not compatibility with a running Cubase.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
let identity = 'instance-1', raw = 0.3, writes = 0, sent = [], rootID = 1;
const access = {
  activate() {}, deactivate() {}, update() {}, getBaseObjectID: () => rootID,
  getObjectUniqueIDString: () => identity, getObjectTitle: () => 'Serum',
  getObjectUniqueName: () => 'Instrument', getObjectTypeName: () => 'Plugin',
  getNumberOfChildObjects: () => 0, getNumberOfParameters: () => 1,
  getParameterTagByIndex: () => 42, getParameterTitle: () => 'Cutoff',
  getParameterProcessValue: () => raw, getParameterDisplayValue: () => String(raw),
  getParameterDisplayUnits: () => '',
  setParameterProcessValue(am, id, tag, value) { raw = value; writes++; }
};
const selected = {}, midiIn = {}, midiOut = { sendMidi(ad, frame) { sent.push(frame); } };
const value = () => ({ setProcessValue() {} });
const page = {
  mHostAccess: { mTrackSelection: {mMixerChannel: selected}, makeDirectAccess: () => access,
    mTransport: {mValue: {mStart: {}, mRecord: {}}},
    mMixConsole: {makeMixerBankZone: () => ({includeInstrumentChannels() {},
      makeMixerBankChannel: () => ({mValue: {mSelected: {}}})})}},
  makeCommandBinding: () => ({}), makeValueBinding() {}
};
const detection = {detectPortPair() {return this;}, expectInputNameContains() {return this;},
  expectOutputNameContains() {return this;}};
const driver = {mPorts: {makeMidiInput: () => midiIn, makeMidiOutput: () => midiOut},
  makeDetectionUnit: () => detection, mMapping: {makePage: () => page},
  mSurface: {makeButton: () => ({mSurfaceValue: value()})}};
const context = vm.createContext({require: () => ({makeDeviceDriver: () => driver}), Date, JSON, Math,
                                 Object, Array, String, isFinite});
vm.runInContext(fs.readFileSync(path.join(__dirname, '../src/midi_creator/studio/cubase_remote.js'), 'utf8'), context);
page.mOnActivate({}, {});
function request(operation, fields = {}, direction = 0) {
  sent = [];
  const payload = JSON.stringify({operation, ...fields});
  const count = Math.ceil(payload.length / 480);
  for (let part = count - 1; part >= 0; part--) {
    midiIn.mOnSysex({}, [0xf0, 0x7d, 0x4d, 0x43, 1, direction, 7, 0,
      part & 127, part >> 7, count & 127, count >> 7,
      ...Buffer.from(payload.slice(part * 480, (part + 1) * 480)), 0xf7]);
  }
  for (let n = 0; n < 300; n++) page.mOnIdle({}, {});
  if (!sent.length) return null;
  assert(sent.every(frame => frame[5] === 1));
  const chunks = sent.map(frame => Buffer.from(frame.slice(12, -1)).toString('ascii'));
  return JSON.parse(chunks.join(''));
}
assert.equal(request('ping').plugin_assignment_available, false);
assert.equal(request('command', {action: 'save'}, 1), null); // Replies cannot execute actions.
let discovered = request('objects');
let object = {token: discovered.token, object_id: 1};
assert.equal(request('parameters', object).parameters[0].tag, 42);
assert.equal(request('set_parameters', {...object, values: [{tag: 42, raw: .7}, {tag: 999, raw: .2}]}).ok, false);
assert.equal(writes, 0); // Reject entire invalid batch before changing anything.
assert.equal(request('set_parameters', {...object, values: [{tag: 42, raw: .7}]}).verified, true);
assert.equal(writes, 1);
identity = 'instance-2';
assert.equal(request('set_parameters', {...object, values: [{tag: 42, raw: .2}]}).ok, false);
assert.equal(writes, 1); // A replacement plugin never inherits a stale write token.
assert.equal(request('plugins', object).ok, false);
discovered = request('objects');
selected.mOnTitleChange({}, {}, 'Different track');
assert.equal(request('parameters', {token: discovered.token, object_id: 1}).ok, false);
rootID = -1; // Cubase's sentinel when no selected project/track is available.
assert.equal(request('ping').selected_track_available, false);
const unavailable = request('objects');
assert.equal(unavailable.target_available, false);
assert.equal(unavailable.objects.length, 0);
assert.equal(unavailable.token, undefined);
console.log('MIDI Remote host mock passed (live Cubase remains unverified).');
