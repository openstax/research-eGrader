class LocalStorageManager {
    constructor() {
        this.lastExerciseKey = 'lastExercise';
        var supported = this.localStorageSupported();
        if (supported) {
            console.log('localStorage is supported');
            this.storage = window.localStorage;
        }
        else {
            this.initFakeStorage()
        }
    }

    localStorageSupported() {
        let testKey = "test";
        let storage = window.localStorage;

        try {
            storage.setItem(testKey, "1");
            storage.removeItem(testKey);
            return true;
        } catch (error) {
            return false;
        }
    }

    initFakeStorage() {
        window.fakeStorage = {

            _data: {},

            setItem: function(id, val) {
                return this._data[id] = String(val);
            },

            getItem: function(id) {
                return this._data.hasOwnProperty(id) ? this._data[id] : undefined;
            },

            removeItem: function(id) {
                return delete this._data[id];
            },

            clear: function() {
                return this._data = {};
            }
        };
        this.storage = window.fakeStorage
    }

    setLastExercise(exerciseId) {
        this.storage.setItem(this.lastExerciseKey, exerciseId)
    }

    getLastExercise() {
        return this.storage.getItem(this.lastExerciseKey)
    }


}

export default LocalStorageManager
