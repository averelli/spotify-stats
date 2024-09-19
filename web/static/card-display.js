document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll('.graph-btn');
    const graphImage = document.getElementById('graph-image');
    const loadingPlaceholder = document.getElementById('loading-placeholder');

    // Function to load the graph based on the selected time frame
    function loadGraph(timeFrame) {
        // Show loading placeholder
        loadingPlaceholder.style.display = 'block';
        graphImage.style.display = 'none';  // Hide the image while loading

        // Fetch the graph from the server
        const chartType = "{{ graph_info['chart_type'] }}";  // Assume chart_type is passed in the context
        const itemId = "{{ graph_info['item_id'] }}";  // Pass the correct item_id dynamically

        // Update the graph image src
        graphImage.src = `/plot_graph/${chartType}/${itemId}?time_frame=${timeFrame}`;

        // Show the image after it's loaded
        graphImage.onload = function() {
            loadingPlaceholder.style.display = 'none';
            graphImage.style.display = 'block';
        };
    }

    // Add event listeners to buttons
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active state from all buttons
            buttons.forEach(btn => btn.classList.remove('active'));

            // Set this button as active
            this.classList.add('active');

            // Load the corresponding graph
            const timeFrame = this.dataset.timeFrame;
            loadGraph(timeFrame);
        });
    });

    // Load the default graph (short term)
    loadGraph('short_term');
});
