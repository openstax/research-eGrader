import $ from 'jquery'
import jQuery from 'jquery';
import _ from 'underscore'
import {activateFormWidget, activateNoteWidget, activateGraderSubmitButton} from './events.js'
import API from './api.js'
import getFormData from './utils.js'
import Handlebars from 'handlebars'
import {startMathJax, typesetMath} from './mathjax.js'

import selectric from 'selectric'

var App = {

    start(userId, exerciseId) {
        this.userId = userId;
        this.exerciseId = exerciseId;

        this.activateEvents();
        this.API = new API();

        // Load the exercise
        this.loadExercise(this.exerciseId);
        // Load the next response
        this.nextResponse(this.userId, this.exerciseId);
        startMathJax();

    },

    activateEvents() {
        activateNoteWidget();
    },

    getNextExercise() {
        console.log('Getting new exercise');
        let self = this;
        let exercise = this.API.getNextExercise(self.userId)
            .done(function(r) {
                let exerciseId = r['exercise_id'];
                self.exerciseId = exerciseId;
                self.loadExercise(exerciseId);
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

        // clear out any options.
        $feedback.empty();
        // place the first option
        $feedback.append($("<option></option>"))
            .attr("value", "" )
            .text("---Select an option---");
        // for each feedback choice append an option
        _.forEach(feedbackChoices, function(choice, index) {
            $feedback.append($("<option></option>")
                    .attr("value",choice[0])
                    .text(choice[1]));
        });


        typesetMath(document);
        activateFormWidget();

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
        
        // inject the userId to the data as it's used by the 
        // backend to save.. maybe better placed in a hidden form field? 
        data['user_id'] = this.userId;
        
        let submit = this.API.submitGradedResponse(data)
            .done(function(r) {
                // If successfull we need to get the next response
                // If there is no more responses then get a new exercise
                // TODO: Code the get next exercise part
                console.log('Load the next response');
                self.nextResponse(self.userId, self.exerciseId)
            })
            .fail(function(r) {
                throw new Error('There was a problem trying to save the graded response')
            });
    }

};

window.App = App;
