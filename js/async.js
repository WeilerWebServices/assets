"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fsStat = require("@nodelib/fs.stat");
const rpl = require("run-parallel");
const constants_1 = require("../constants");
const utils = require("../utils/index");
function read(dir, settings, callback) {
    if (!settings.stats && constants_1.IS_SUPPORT_READDIR_WITH_FILE_TYPES) {
        return readdirWithFileTypes(dir, settings, callback);
    }
    return readdir(dir, settings, callback);
}
exports.read = read;
function readdirWithFileTypes(dir, settings, callback) {
    settings.fs.readdir(dir, { withFileTypes: true }, (readdirError, dirents) => {
        if (readdirError) {
            return callFailureCallback(callback, readdirError);
        }
        const entries = dirents.map((dirent) => ({
            dirent,
            name: dirent.name,
            path: `${dir}${settings.pathSegmentSeparator}${dirent.name}`
        }));
        if (!settings.followSymbolicLinks) {
            return callSuccessCallback(callback, entries);
        }
        const tasks = entries.map((entry) => makeRplTaskEntry(entry, settings));
        rpl(tasks, (rplError, rplEntries) => {
            if (rplError) {
                return callFailureCallback(callback, rplError);
            }
            callSuccessCallback(callback, rplEntries);
        });
    });
}
exports.readdirWithFileTypes = readdirWithFileTypes;
function makeRplTaskEntry(entry, settings) {
    return (done) => {
        if (!entry.dirent.isSymbolicLink()) {
            return done(null, entry);
        }
        settings.fs.stat(entry.path, (statError, stats) => {
            if (statError) {
                if (settings.throwErrorOnBrokenSymbolicLink) {
                    return done(statError);
                }
                return done(null, entry);
            }
            entry.dirent = utils.fs.createDirentFromStats(entry.name, stats);
            return done(null, entry);
        });
    };
}
function readdir(dir, settings, callback) {
    settings.fs.readdir(dir, (readdirError, names) => {
        if (readdirError) {
            return callFailureCallback(callback, readdirError);
        }
        const filepaths = names.map((name) => `${dir}${settings.pathSegmentSeparator}${name}`);
        const tasks = filepaths.map((filepath) => {
            return (done) => fsStat.stat(filepath, settings.fsStatSettings, done);
        });
        rpl(tasks, (rplError, results) => {
            if (rplError) {
                return callFailureCallback(callback, rplError);
            }
            const entries = [];
            for (let index = 0; index < names.length; index++) {
                const name = names[index];
                const stats = results[index];
                const entry = {
                    name,
                    path: filepaths[index],
                    dirent: utils.fs.createDirentFromStats(name, stats)
                };
                if (settings.stats) {
                    entry.stats = stats;
                }
                entries.push(entry);
            }
            callSuccessCallback(callback, entries);
        });
    });
}
exports.readdir = readdir;
function callFailureCallback(callback, error) {
    callback(error);
}
function callSuccessCallback(callback, result) {
    callback(null, result);
}
