// Cubase MIDI Remote v1, including optional DirectAccess plugin manager in v1.3.
// Only framed requests are executed. Replies on a shared LoopBe bus are ignored.
var api = require('midiremote_api_v1');
var driver = api.makeDeviceDriver('MIDI Creator', 'Studio Bridge', 'MIDI Creator');
var midiIn = driver.mPorts.makeMidiInput();
var midiOut = driver.mPorts.makeMidiOutput();
driver.makeDetectionUnit().detectPortPair(midiIn, midiOut)
    .expectInputNameContains('__INPUT_MATCH__').expectOutputNameContains('__OUTPUT_MATCH__');
var page = driver.mMapping.makePage('Studio');
var selected = page.mHostAccess.mTrackSelection.mMixerChannel;
var access = page.mHostAccess.makeDirectAccess(selected);
var activeDevice = null, activeMapping = null, queue = [], incoming = {};
var snapshot = null, generation = 0, outgoing = [];
var state = {selected_track: '', playing: false, recording: false};
selected.mOnTitleChange = function (ad, am, title) { state.selected_track = title; snapshot = null; };
page.mHostAccess.mTransport.mValue.mStart.mOnProcessValueChange = function (ad, am, value) { state.playing = value > 0.5; };
page.mHostAccess.mTransport.mValue.mRecord.mOnProcessValueChange = function (ad, am, value) { state.recording = value > 0.5; };
access.mOnObjectWillBeRemoved = function () { snapshot = null; };

var commandDefinitions = {
    play: ['Transport', 'Start'], stop: ['Transport', 'Stop'],
    rewind: ['Transport', 'Return to Zero'], save: ['File', 'Save']
};
var commands = {};
var index = 0;
for (var name in commandDefinitions) {
    var button = driver.mSurface.makeButton(index++, 0, 1, 1);
    var binding = page.makeCommandBinding(button.mSurfaceValue, commandDefinitions[name][0], commandDefinitions[name][1]);
    commands[name] = {surface: button.mSurfaceValue, binding: binding};
}
var bank = page.mHostAccess.mMixConsole.makeMixerBankZone('Instrument tracks');
bank.includeInstrumentChannels();
var instrumentTracks = [];
for (var i = 0; i < 16; i++) {
    var channel = bank.makeMixerBankChannel();
    var selector = driver.mSurface.makeButton(i, 2, 1, 1);
    page.makeValueBinding(selector.mSurfaceValue, channel.mValue.mSelected);
    var track = {surface: selector.mSurfaceValue, title: ''};
    instrumentTracks.push(track);
    (function (entry) {
        channel.mOnTitleChange = function (ad, am, title) { entry.title = title; };
    })(track);
}

function safeInteger(value) { return typeof value === 'number' && isFinite(value) && Math.floor(value) === value; }
function asciiJSON(value) {
    return JSON.stringify(value).replace(/[\u007f-\uffff]/g, function (c) {
        return '\\u' + ('0000' + c.charCodeAt(0).toString(16)).slice(-4);
    });
}
function reply(id, value) {
    var text = asciiJSON(value);
    if (text.length > 131072) text = asciiJSON({ok: false, error: 'Response too large; narrow the query'});
    var count = Math.ceil(text.length / 480);
    for (var part = 0; part < count; part++) {
        var frame = [0xf0, 0x7d, 0x4d, 0x43, 1, 1, id & 127, id >> 7,
                     part & 127, part >> 7, count & 127, count >> 7];
        var chunk = text.slice(part * 480, (part + 1) * 480);
        for (var j = 0; j < chunk.length; j++) frame.push(chunk.charCodeAt(j));
        frame.push(0xf7);
        outgoing.push(frame);
    }
}
function discover() {
    access.update(activeMapping);
    var root = access.getBaseObjectID(activeMapping);
    if (!safeInteger(root) || root < 0) {
        snapshot = null;
        return {ok: true, target_available: false, objects: [],
                next_step: 'Open a Cubase project and select an instrument track, then discover again.'};
    }
    var pending = [{id: root, depth: 0}], objects = [], identities = {};
    while (pending.length && objects.length < 256) {
        var item = pending.shift(), objectID = item.id;
        var identity = access.getObjectUniqueIDString(activeMapping, objectID);
        if (identities[objectID] !== undefined) continue;
        identities[objectID] = identity;
        objects.push({object_id: objectID, parent_id: item.parent,
                      title: access.getObjectTitle(activeMapping, objectID),
                      unique_name: access.getObjectUniqueName(activeMapping, objectID),
                      type: access.getObjectTypeName ? access.getObjectTypeName(activeMapping, objectID) : '',
                      unique_id: identity,
                      parameter_count: access.getNumberOfParameters(activeMapping, objectID)});
        if (item.depth < 8) {
            var count = access.getNumberOfChildObjects(activeMapping, objectID);
            for (var n = 0; n < count; n++) pending.push({id: access.getChildObjectID(activeMapping, objectID, n),
                                                        parent: objectID, depth: item.depth + 1});
        }
    }
    var token = String(++generation) + ':' + String(Date.now());
    snapshot = {token: token, time: Date.now(), identities: identities, track: state.selected_track};
    return {ok: true, target_available: true, token: token, selected_track: state.selected_track, objects: objects,
            truncated: pending.length > 0};
}
function requireObject(request) {
    if (!snapshot || request.token !== snapshot.token || Date.now() - snapshot.time > 30000 ||
        snapshot.track !== state.selected_track) throw new Error('Stale object token; discover again');
    if (!safeInteger(request.object_id) || snapshot.identities[request.object_id] === undefined)
        throw new Error('Object was not in the discovery snapshot');
    if (access.getObjectUniqueIDString(activeMapping, request.object_id) !== snapshot.identities[request.object_id])
        throw new Error('Object identity changed; discover again');
    return request.object_id;
}
function parameters(request) {
    var objectID = requireObject(request), result = [];
    var count = access.getNumberOfParameters(activeMapping, objectID);
    var query = String(request.query || '').toLowerCase();
    var offset = request.offset === undefined ? 0 : request.offset;
    var limit = request.limit === undefined ? 50 : request.limit;
    if (!safeInteger(offset) || offset < 0 || !safeInteger(limit) || limit < 1 || limit > 100)
        throw new Error('Parameter page must use offset >= 0 and limit 1..100');
    var matches = 0;
    for (var n = 0; n < count; n++) {
        var tag = access.getParameterTagByIndex(activeMapping, objectID, n);
        var title = access.getParameterTitle(activeMapping, objectID, tag, 128);
        if (title.toLowerCase().indexOf(query) < 0) continue;
        if (matches++ < offset || result.length >= limit) continue;
        result.push({tag: tag, title: title, raw: access.getParameterProcessValue(activeMapping, objectID, tag),
                     display: access.getParameterDisplayValue(activeMapping, objectID, tag),
                     units: access.getParameterDisplayUnits(activeMapping, objectID, tag)});
    }
    return {ok: true, parameters: result, total_matches: matches};
}
function handle(request) {
    if (!activeMapping) throw new Error('Activate the Studio MIDI Remote page first');
    if (request.operation === 'ping') {
        var tracks = [];
        for (var n = 0; n < instrumentTracks.length; n++)
            if (instrumentTracks[n].title) tracks.push({index: n, name: instrumentTracks[n].title});
        return {ok: true, bridge_version: 1, selected_track: state.selected_track,
                selected_track_available: access.getBaseObjectID(activeMapping) >= 0,
                playing: state.playing, recording: state.recording, instrument_tracks: tracks,
                plugin_assignment_available: !!(access.mPluginManager && access.mPluginManager.trySetSlotPlugin),
                note_editing_available: false, preset_file_loading_available: false,
                project_creation_available: false};
    }
    if (request.operation === 'objects') return discover();
    if (request.operation === 'parameters') return parameters(request);
    if (request.operation === 'set_parameters') {
        var objectID = requireObject(request), values = request.values;
        if (!Array.isArray(values) || values.length < 1 || values.length > 64) throw new Error('Use 1..64 parameter writes');
        var known = {}, count = access.getNumberOfParameters(activeMapping, objectID);
        for (var k = 0; k < count; k++) known[access.getParameterTagByIndex(activeMapping, objectID, k)] = true;
        // Validate the complete batch before the first write.
        for (var v = 0; v < values.length; v++) {
            var value = values[v];
            if (!safeInteger(value.tag) || !known[value.tag] || typeof value.raw !== 'number' ||
                !isFinite(value.raw) || value.raw < 0 || value.raw > 1) throw new Error('Unknown tag or raw value outside 0..1');
        }
        var readback = [], verified = true;
        for (var x = 0; x < values.length; x++) access.setParameterProcessValue(activeMapping, objectID, values[x].tag, values[x].raw);
        for (var y = 0; y < values.length; y++) {
            var actual = access.getParameterProcessValue(activeMapping, objectID, values[y].tag);
            var equal = Math.abs(actual - values[y].raw) < 0.002;
            verified = verified && equal;
            readback.push({tag: values[y].tag, requested: values[y].raw, actual: actual, verified: equal});
        }
        return {ok: true, verified: verified, readback: readback};
    }
    if (request.operation === 'plugins' || request.operation === 'assign_serum') {
        var slot = requireObject(request), manager = access.mPluginManager;
        if (!manager || !manager.trySetSlotPlugin) throw new Error('Plugin assignment requires MIDI Remote API 1.3');
        var available = [], collections = manager.getNumberOfPluginCollections(activeMapping, slot);
        for (var ci = 0; ci < collections; ci++) {
            var entries = manager.getPluginCollectionByIndex(activeMapping, slot, ci).mEntries;
            for (var ei = 0; ei < entries.length; ei++) {
                var entry = entries[ei];
                if (entry.mPluginUID) available.push({uid: entry.mPluginUID, title: entry.mTitle || entry.mName || ''});
            }
        }
        if (request.operation === 'plugins') return {ok: true, plugins: available};
        var selectedPlugin = null;
        for (var pi = 0; pi < available.length; pi++) if (available[pi].uid === request.plugin_uid) selectedPlugin = available[pi];
        if (!selectedPlugin || request.plugin_uid !== '__SERUM_UID__') throw new Error('Only the configured Serum instrument UID may be assigned');
        if (!request.replace_existing && access.getNumberOfChildObjects(activeMapping, slot) > 0)
            throw new Error('Slot has children; inspect it and explicitly allow replacement if intended');
        var accepted = manager.trySetSlotPlugin(activeMapping, slot, request.plugin_uid, false);
        snapshot = null;
        return {ok: true, assignment_accepted: accepted, verified: false,
                next_step: 'Rediscover the instrument slot to verify the loaded plugin; load a preset through Cubase.'};
    }
    if (request.operation === 'select_track') {
        if (!safeInteger(request.index) || request.index < 0 || request.index >= instrumentTracks.length ||
            !instrumentTracks[request.index].title) throw new Error('Instrument track index is unavailable');
        instrumentTracks[request.index].surface.setProcessValue(activeDevice, 1);
        snapshot = null;
        return {ok: true, selection_dispatched: true, verified: false};
    }
    if (request.operation === 'command') {
        var command = commands[request.action];
        if (!command) throw new Error('Supported commands: play, stop, rewind, save');
        if (command.binding.canPerform && !command.binding.canPerform(activeMapping)) throw new Error('Cubase command is unavailable now');
        command.surface.setProcessValue(activeDevice, 0);
        command.surface.setProcessValue(activeDevice, 1);
        command.surface.setProcessValue(activeDevice, 0);
        return {ok: true, command_dispatched: true, verified: false,
                next_step: 'Check transport state or the saved project file to verify the effect.'};
    }
    throw new Error('Unsupported operation: ' + request.operation);
}
page.mOnActivate = function (ad, am) {
    activeDevice = ad; activeMapping = am; snapshot = null; access.activate(am);
};
page.mOnDeactivate = function (ad, am) {
    access.deactivate(am); activeMapping = null; snapshot = null; queue = []; incoming = {}; outgoing = [];
};
midiIn.mOnSysex = function (ad, message) {
    var data = Array.prototype.slice.call(message);
    if (data[0] === 0xf0) data.shift();
    if (data[data.length - 1] === 0xf7) data.pop();
    if (data.length < 11 || data[0] !== 0x7d || data[1] !== 0x4d || data[2] !== 0x43 ||
        data[3] !== 1 || data[4] !== 0) return;
    var id = data[5] + 128 * data[6], part = data[7] + 128 * data[8], count = data[9] + 128 * data[10];
    if (id < 1 || count < 1 || count > 274 || part >= count || data.length > 491) return;
    var now = Date.now();
    for (var old in incoming) if (now - incoming[old].time > 6000) delete incoming[old];
    if (Object.keys(incoming).length >= 8 && !incoming[id]) return;
    if (!incoming[id]) incoming[id] = {count: count, parts: {}, time: now};
    var assembly = incoming[id];
    if (assembly.count !== count) { delete incoming[id]; return; }
    var chunk = '';
    for (var n = 11; n < data.length; n++) chunk += String.fromCharCode(data[n]);
    if (assembly.parts[part] !== undefined && assembly.parts[part] !== chunk) { delete incoming[id]; return; }
    assembly.parts[part] = chunk;
    if (Object.keys(assembly.parts).length !== count) return;
    var json = '';
    for (var c = 0; c < count; c++) json += assembly.parts[c];
    delete incoming[id];
    try {
        if (json.length > 131072 || queue.length >= 8) throw new Error('Request queue or payload too large');
        queue.push({id: id, request: JSON.parse(json)});
    } catch (error) { reply(id, {ok: false, error: String(error.message || error)}); }
};
page.mOnIdle = function (ad, am) {
    activeDevice = ad;
    if (queue.length) {
        var item = queue.shift();
        try { reply(item.id, handle(item.request)); }
        catch (error) { reply(item.id, {ok: false, error: String(error.message || error)}); }
    }
    // Throttle shared-bus replies rather than emitting a burst of hundreds of packets.
    if (outgoing.length) midiOut.sendMidi(ad, outgoing.shift());
};
