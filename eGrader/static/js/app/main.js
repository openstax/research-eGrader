import $ from 'jquery'
import jQuery from 'jquery';
import _ from 'underscore'
import noty from 'noty'
import {activateFormWidget, activateNoteWidget, activateGraderSubmitButton, activateQualButton} from './events.js'
import API from './api.js'
import getFormData from './utils.js'
import Handlebars from 'handlebars'
import {startMathJax, typesetMath} from './mathjax.js'
import SocketManager from './socket.js'


window.$ = window.jQuery = $;

var App = {

    start(userId, exerciseId) {
        startMathJax();
        this.userId = userId;
        this.exerciseId = exerciseId;

        // setup interfaces
        this.API = new API();
        this.socketManager = new SocketManager();
        this.sessionId = this.socketManager.getSessionId();
        console.log(this.sessionId);

        this.activateEvents();

        // Load the exercise
        this.loadExercise(this.exerciseId);
        // Load the next response
        this.nextResponse(this.userId, this.exerciseId);
    },

    activateEvents() {
        activateNoteWidget();
        // activateQualButton(this.submitUnqualifiedExercise.bind(this))
    },

    getNextExercise() {
        console.log('Getting new exercise');
        let self = this;
        let exercise = this.API.getNextExercise(self.userId)
            .done(function(r) {
                let exerciseId = r['exercise_id'];
                self.exerciseId = exerciseId;
                self.loadExercise(exerciseId);
                console.log(exerciseId);
            })
            .fail(function(r) {
                throw new Error('There was a problem retrieving an exercise from the API')
            })
    },

    loadExercise(exerciseId) {
        let self = this;
        let exercise = this.API.getExercise(exerciseId)
            .done(function(r) {
                self.showExercise(r);
            })
            .fail(function(r) {
                // console.log(r);
                throw new Error('There was a problem retrieving an exercise from the API')
            });
    },

    showExercise(r) {
        let $eText = $('.exercise-text');
        let $eAnswer = $('.exercise-answer');
        
        $eText.empty();
        $eAnswer.empty();
        
        console.log('loading exercise...');
        console.log(r);

        $eText.html(r['exercise_html']);
        $eAnswer.html(r['answer_html']);
        this.feedbackChoices = r['feedback_choices']

    },

    showResponse(r) {
        let $stuResponse = $('.stu-response');
        console.log('loading response...');
        $stuResponse.html(r['response']['free_response']);
        console.log(r['response']['free_response']);

        // Need to set hidden field for response_id in the form
        this.loadGraderForm(this.feedbackChoices);
        $('#responseId').val(r['response']['id']);
    },

    nextResponse(userId, exerciseId) {
        let self = this;

        let response = this.API.getNextResponse(userId, exerciseId)
            .done(function(r) {
                if (r['success']){
                    self.showResponse(r);
                } else {
                    self.getNextExercise();
                    console.log('No more responses for that exercise')
                }
            })
            .fail(function(r) {
                throw new Error('There was a problem retrieving a student response')
            })
    },

    loadFeedbackOptions(feedbackChoices) {
        // Grab feedback form element

        let $feedback = $('.feedback');

        _.forEach(feedbackChoices, function(choice, index) {
            $feedback.append($("<option></option>")
                    .attr("value",choice[0])
                    .text(choice[1]));
        });

        activateFormWidget();
        typesetMath(document);

    },
    
    loadGraderForm(feedbackChoices) {
        let $container = $('.grader-form-container');
        let source = $('#grader-form-template').html();
        let template = Handlebars.compile(source);
        $container.empty();
        $container.html(template());

        activateGraderSubmitButton(this.submitGraderResponse.bind(this));
        this.loadFeedbackOptions(feedbackChoices);
        console.log(feedbackChoices)
    },

    submitGraderResponse() {
        let self = this;
        let data = getFormData($('form'));

        const valid = this.validateForm(data);
        
        // inject the userId to the data as it's used by the 
        // backend to save.. maybe better placed in a hidden form field? 
        data['user_id'] = this.userId;
        data['session_id'] = this.socketManager.getSessionId();

        if (valid) {
            let submit = this.API.submitGradedResponse(data)
            .done(function(r) {
                // If successfull we need to get the next response
                // If there is no more responses then get a new exercise
                console.log('Load the next response');
                self.nextResponse(self.userId, self.exerciseId)
            })
            .fail(function(r) {
                throw new Error('There was a problem trying to save the graded response')
            });
        }

    },

    submitUnqualifiedExercise() {
        let self = this;
        let data = {
            user_id: self.userId,
            exercise_id: self.exerciseId
        };
        console.log(data);

        let submit = this.API.submitUnqualifiedExercise(data)
            .done(function(r) {
                console.log('Submitted Qualification');
                self.getNextExercise()
            })
            .fail(function(r) {
                throw new Error('There was a problem trying to save the qualification')
            })
    },
    
    notifySuccess(message) {
        new noty({
            text: message,
            layout: 'topRight',
            theme: 'relax',
            type: 'success',
            timeout: 3000
        })
    },
    
    notifyError(message) {
    new noty({
      text: message,
      layout: 'topRight',
      theme: 'relax',
      type: 'error',
      timeout: 3000 
    });
  },

    validateForm(data) {
        console.log(data);
        // map form elements other than qualtiy to a variable
        const score = data['score'] ? true:false;
        const misconception = data['misconception'] ? true:false;
        const feedback = data['feedback_id'] ? true:false;
        console.log(score, misconception, feedback);

        if (data['quality'] == 't') {
            // Return true immediately if junk = true
            return true
        } else if (data['quality'] == 'f') {
            //if junk = false then we need to validate the rest of the form
            if (score == false || misconception == false || feedback == false) {
                this.notifyError('There was an error. Please make sure you made all selections')
            } else {
                return true
            }
        } else {
            this.notifyError('There was an error. Please make a quality selection')
        }



    }

};

window.App = App;
