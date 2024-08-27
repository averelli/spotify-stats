// scripts.js
$(document).ready(function() {
    // Initially, show the short-term chart and hide others
    $('#short_term_chart').show();
    $('#medium_term_chart').hide();
    $('#long_term_chart').hide();

    // Set the short-term button as active by default
    $('#short_term_btn').addClass('active');

    // Handle button clicks
    $('.nav-btn').click(function() {
        // Remove active class from all buttons and add to the clicked one
        $('.nav-btn').removeClass('active');
        $(this).addClass('active');

        // Hide all chart contents
        $('.chart-content').hide();

        // Show the selected chart
        const selectedChart = $(this).attr('id').replace('_btn', '_chart');
        $('#' + selectedChart).show();
    });
});
