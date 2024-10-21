/* Copyright (c) 2012 Ian Zamojc, Marco Ceppi, & Nathan Osman.
   All rights reserved.
   
   Redistribution and use in source and binary forms are permitted
   provided that the above copyright notice and this paragraph are
   duplicated in all such forms and that any documentation,
   advertising materials, and other materials related to such
   distribution and use acknowledge that the software was developed
   by Ian Zamojc.  The name of the University may not be used to
   endorse or promote products derived from this software without
   specific prior written permission. THIS SOFTWARE IS PROVIDED
   ``AS IS'' AND WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
   WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
   FITNESS FOR A PARTICULAR PURPOSE. */

(function() {
    
    var StackTack = function($) {
        
        /* @if embed-css */
        
        $('head').append('<style>' + /* @include stacktack.css minify quote */ + '</style>');
        
        /* @endif */
        
        // Utility method to retrieve a list of data attributes for an element with fallback for non-HTML5 browsers
        function RetrieveDataAttributes(element) {
            
            // If the dataset is available, then return the default value
            if(typeof element.dataset != 'undefined')
                return element.dataset;
            
            // Otherwise, enumerate each of the attributes in the element
            var data_attrs = {}
            $.each(element.attributes, function(key, attribute) {
                
                if(attribute['name'].match(/^data-/) !== null)
                    data_attrs[attribute['name'].replace(/^data-/, '')] = attribute['value'];
                
            });
            
            return data_attrs;
            
        }
        
        // Utility method that sends a request to the API
        function SendAPIRequest(options, site_domain, method, parameters, success_callback, error_callback) {
            
            // Begin by constructing the URL that will be used for the request
            var url = ((options['secure'] == 'true')?'https://':'http://') + 'api.stackexchange.com/2.0' + method;
            
            // Add the API key and site to the list of parameters
            parameters['key']    = options['key'];
            parameters['site']   = site_domain;
            parameters['filter'] = options['filter'];
            
            // Lastly, make the request
            $.ajax({ 'url': url, 'data': parameters, 'dataType': 'jsonp',
                     'success': function(data) {
                         
                         // If an error message was supplied, then invoke the error callback
                         if(typeof data['error_message'] != 'undefined')
                             error_callback(data['error_message']);
                         else
                             success_callback(data['items']);
                         
                     }});
        }
        
        // Generates the HTML for question tags
        function GenerateTagHTML(tags) {
            
            var html = '<div class="tags">';
            
            // Generate the html for each of the tags and return it
            $.each(tags, function(key, tag) { html += '<span>' + tag + '</span>' });
            return html + '</div>';
            
        }
        
        // Generates the HTML for a user profile
        function GenerateProfileHTML(user) {
            
            if(typeof user['link'] != 'undefined')
                return '<a href="' + user['link'] + '" class="user-link">by ' + user['display_name'] + '</a>';
            else
                return '<span class="user-link">' + user['display_name'] + '</span>'
            
        }
        
        // Generates the HTML for an answer
        function GenerateAnswerHTML(options, answer) {
            
            var content = '';
            if(options['votes'] == 'true')
                content += '<div class="hr" /><a href="' + answer['link'] + '" target="_blank" class="heading answer-count">' +
                           answer['score'] + ' votes' + (answer['is_accepted']?' - <span class="accepted">Accepted</span>':'') + '</a>';
            
            content += GenerateProfileHTML(answer['owner']) + answer['body'];
            return content;
            
        }
        
        // Processes the answers to a question, returning the HTML for the answers
        function ProcessAnswers(options, data) {
            
            // Unfortunately we need to manually sort the answers because the API does not do this for us and then
            // convert the answers into a map where the key becomes the answer's ID
            var sorted_answers = data['answers'].sort(function (a, b) { return b['score'] - a['score']; });
            var answer_key = {};
            $.each(sorted_answers, function(key, value) { answer_key[value['answer_id']] = value; });
            
            // Add different answers to the output list depending on the 'answers' option
            var output_answers = [];
            if(options['answers'] == 'all')
                output_answers = sorted_answers;
            else if(options['answers'] == 'accepted') {
                
                if(typeof data['accepted_answer_id'] != 'undefined' && typeof answer_key[data['accepted_answer_id']] != 'undefined')
                    output_answers.push(answer_key[data['accepted_answer_id']]);
                else
                    output_answers.push(sorted_answers[0]);
            }
            else {
                
                var id_list = options['answers'].split(',');
                $.each(id_list, function(key, value) {
                    
                    if(typeof answer_key[value] != 'undefined')
                        output_answers.push(answer_key[value]);
                    
                });
            }
            
            // Concatenate the output to the question
            var html = '';
            
            if(output_answers.length)
                $.each(output_answers, function(key, value) { html += GenerateAnswerHTML(options, value); });
            else
                html += '<div class="hr" /><p class="tip">No answers matched the specified criteria.</p>';
            
            return html;
        }
        
        // Processes a list of questions for a particular site
        function ProcessQuestionList(question_list, api_data) {
            
            // First, convert the data into a map [question ID] => [API data]
            var questions = {};
            $.each(api_data, function(key, question) { questions[question['question_id']] = question; });
            
            // Now go through each instance in question list, generating the HTML for it
            $.each(question_list, function(key, instance) {
                
                // Find the right API data for the instance and generate it
                var instance_data = questions[instance['id']];
                var element = $(instance['element']);
                
                // Set the element's style
                element.addClass('stacktack-container');
                element.css('width', instance['width'] + ((instance['width'].toString().match(/^\d+$/) !== null)?'px':''));
                
                // Generate the contents
                var contents = '<div class="branding">Stack<span>Tack</span></div>';
                contents += '<a href="' + instance_data['link'] + '" target="_blank" class="heading">' + instance_data['title'] + '</a>';
                
                // Display the question if requested
                if(instance['question'] == 'true') {
                    
                    contents += GenerateProfileHTML(instance_data['owner']) + '<div class="hr" />' + instance_data['body'];
                    
                    // Display tags if requested
                    if(instance['tags'] == 'true')
                        contents += GenerateTagHTML(instance_data['tags']);
                    
                }
                
                // Display answers if the user requests them
                if(instance['answers'] != 'none') {
                    
                    if(typeof instance_data['answers'] != 'undefined')
                        contents += ProcessAnswers(instance, instance_data);
                    else
                        contents += '<div class="hr" /><p class="tip">This question does not have any answers.</p>';
                    
                }
                
                element.html(contents);
                
            });
        }
        
        // The application of options is done on three different levels. The initial values for all instances
        // are taken from $.fn.stacktack.defaults. Then each invocation of .stacktack() can supply a list of
        // parameters that override the default values. Finally, each element itself can override an option
        // by specifying a data-* attribute in the container element.
        $.fn.stacktack = function(custom_options) {
            
            // The second level of options that apply to all elements in this invocation
            var second_level_options = $.extend({}, $.fn.stacktack.defaults, custom_options);
            
            // As we loop over the elements, we will be generating a list of post IDs for various
            // sites in the Stack Exchange network. Keep a list of them here:
            var site_list = {};
            
            // Begin looping over the current set of matched elements, applying StackTack to them
            this.each(function() {
                
                // Retrieve all of the data-* attributes in the element and use it to override
                // the second level options we calculated above
                var third_level_options = $.extend({}, second_level_options, RetrieveDataAttributes(this), { 'element': this });
                
                // Make sure that ID was specified since it is not guaranteed to exist
                if(typeof third_level_options['id'] != 'undefined') {
                    
                    // Determine the site (and remove '.com' from the end for consistency)
                    var site = third_level_options['site'].replace(/\.com$/, '');
                    
                    // Add the item to the list for that site
                    if(typeof site_list[site] == 'undefined')
                        site_list[site] = [];
                    
                    site_list[site].push(third_level_options);
                    
                }
            });
            
            // Now loop over each site and fetch the questions for that site
            $.each(site_list, function(site, question_list) {
                
                // Concatenate the list of question IDs
                var question_id_list = [];
                $.each(question_list, function(key, instance) { question_id_list.push(instance['id']); });
                var question_id_str = $.unique(question_id_list).join(';');
                
                // Make the API request for the question data (using the second level options)
                SendAPIRequest(second_level_options, site, '/questions/' + question_id_str, {},
                               function(data) { ProcessQuestionList(question_list, data); },
                               /* TODO */
                               function(error_message) {});
                
            });
        };

        // These are the default settings that are applied to each element in the matched set
        $.fn.stacktack.defaults = {
            answers:      'accepted',                  // any one of the following:
                                                       //   - 'all' for all of the answers
                                                       //   - 'none' for none of the answers
                                                       //   - 'accepted' for only the accepted answer or top voted
                                                       //   - a list of comma-separated values
            key:          'CRspH1WAlZKCeCinkGOLHw((',  // the API key to use with StackTack
            filter:       '!-)dQB3E8g_ab',             // the filter to use when fetching question data
            question:     'true',                      // whether to display the question or not
            secure:       'false',                     // true to use HTTPS when accessing the API
            site:         'stackoverflow',             // the default site to use for API lookups
            tags:         'true',                      // display tags under the question
            votes:        'true',                      // display vote count for each answer
            width:        'auto'                       // the width of each instance (in pixels)
        };
    }
    
    /* @if jquery-check */
    
    // By default, StackTack checks to ensure that jQuery is included in the current page
    // and if it isn't it will load it from jQuery's CDN.
    if(typeof window.jQuery == 'undefined') {
        
        // Insert the script into the DOM
        var jquery_script = document.createElement('script');
        jquery_script.type = 'text/javascript';
        jquery_script.src = 'http://code.jquery.com/jquery-latest.min.js';
        jquery_script.onload = function() {
            
            // Once the script has loaded, we can safely use jQuery
            StackTack(jQuery);
            
            // Run StackTack on all elements on the page with the 'stacktack' class
            $(document).ready(function() {
                
                $('.stacktack').stacktack();
                
            });
            
        };
        
        document.getElementsByTagName('head')[0].appendChild(jquery_script);
        
    }

    /* @else */
    
    // Otherwise, just run the StackTack initialization method
    StackTack(jQuery);
    
    /* @endif */
    
})();