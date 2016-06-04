import API from './api.js'
import noty from 'noty'
import _ from 'underscore'

class Notes {
    constructor() {
        this.noteBox = $('.note-ledger');
        this.textArea = $('.notes-text');
        this.API = new API();
    }
    
    addNote(userId, exerciseId, text) {
        const data = {user_id:userId, exercise_id: exerciseId, text:text};
        let self = this;
        let submit = this.API.submitNote(data)
            .done(function(r) {
                console.log('Submitted Note');
                self.notifySuccess('Note successfully submitted!');
                self.showNote(r['note']['text']);
                self.textArea.val('');
            })
            .fail(function(r) {
                throw new Error('There was a problem trying to submit the note')
            })
    }

    showNote(text) {
        this.noteBox.append($('<div></div>').addClass('note-record border_bottom').html(text));

    }

    loadNotes(userId, exerciseId) {
        let self = this;
        this.noteBox.empty();
        
        let response = this.API.getNotes(userId, exerciseId)
            .done(function(r) {
                let notes = r['notes'];
                _.forEach(notes, function(note) {
                    self.showNote(note.text);
                })

            }).fail(function(r) {
                throw new Error('There was a problem retrieving notes from the API')
            })
    }
    
    notifySuccess(message) {
        new noty({
            text: message,
            layout: 'topRight',
            theme: 'relax',
            type: 'success',
            timeout: 3000
        })
    }


}

export default Notes
