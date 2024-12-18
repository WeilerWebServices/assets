"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fsStat = require("@nodelib/fs.stat");
const constants_1 = require("../constants");
const utils = require("../utils/index");
function read(dir, settings) {
    if (!settings.stats && constants_1.IS_SUPPORT_READDIR_WITH_FILE_TYPES) {
        return readdirWithFileTypes(dir, settings);
    }
    return readdir(dir, settings);
}
exports.read = read;
function readdirWithFileTypes(dir, settings) {
    const dirents = settings.fs.readdirSync(dir, { withFileTypes: true });
    return dirents.map((dirent) => {
        const entry = {
            dirent,
            name: dirent.name,
            path: `${dir}${settings.pathSegmentSeparator}${dirent.name}`
        };
        if (entry.dirent.isSymbolicLink() && settings.followSymbolicLinks) {
            try {
                const stats = settings.fs.statSync(entry.path);
                entry.dirent = utils.fs.createDirentFromStats(entry.name, stats);
            }
            catch (error) {
                if (settings.throwErrorOnBrokenSymbolicLink) {
                    throw error;
                }
            }
        }
        return entry;
    });
}
exports.readdirWithFileTypes = readdirWithFileTypes;
function readdir(dir, settings) {
    const names = settings.fs.readdirSync(dir);
    return names.map((name) => {
        const entryPath = `${dir}${settings.pathSegmentSeparator}${name}`;
        const stats = fsStat.statSync(entryPath, settings.fsStatSettings);
        const entry = {
            name,
            path: entryPath,
            dirent: utils.fs.createDirentFromStats(name, stats)
        };
        if (settings.stats) {
            entry.stats = stats;
        }
        return entry;
    });
}
exports.readdir = readdir;
