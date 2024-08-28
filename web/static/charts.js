$(document).ready(function () {
    // Default settings: Show short term chart
    $('.chart-content').hide();
    $('#short_term_chart').show();

    // Handle navbar button clicks
    $('.nav-btn').click(function () {
        // Remove 'active' class from all buttons
        $('.nav-btn').removeClass('active');

        // Add 'active' class to the clicked button
        $(this).addClass('active');

        // Hide all charts
        $('.chart-content').hide();

        // Show the corresponding chart
        if ($(this).attr('id') === 'short_term_btn') {
            $('#short_term_chart').show();
        } else if ($(this).attr('id') === 'medium_term_btn') {
            $('#medium_term_chart').show();
        } else if ($(this).attr('id') === 'long_term_btn') {
            $('#long_term_chart').show();
        }
    });
});
