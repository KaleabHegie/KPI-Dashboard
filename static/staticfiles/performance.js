$(document).ready(function() {
    // Function to handle modal opening and data retrieval
    function openPerformanceModal(kpiName, annualTarget, annualPerformance) {
        // Set the modal content
        $('#kpiName').val(kpiName);
        $('#annualTarget').val(annualTarget);
        $('#newPerformance').val(annualPerformance); // Set performance if available

        // Show the modal
        $('#performanceModal').modal('show');
    }

    // Event handler for target and performance buttons
    $('.btn').on('click', function() {
        var kpiName = $(this).data('kpi-name');
        var annualTarget = $(this).data('annual-target');
        var annualPerformance = $(this).data('annual-performance');

        // Check which button was clicked
        if (annualTarget !== undefined) {
            // Target button clicked, open modal with target data
            openPerformanceModal(kpiName, annualTarget, annualPerformance);
        } else if (annualPerformance !== undefined) {
            // Performance button clicked, open modal with performance data
            openPerformanceModal(kpiName, annualTarget, annualPerformance);
        }
    });

    // AJAX request to save performance data
    $('#savePerformance').on('click', function() {
        var newPerformance = $('#newPerformance').val();
        var kpiName = $('#kpiName').val();

        // Perform AJAX request to update performance data
        $.ajax({
            type: 'POST',
            url: '{% url "update_performance" %}',
            data: {
                'performance': newPerformance,
                'kpi_name': kpiName,
                csrfmiddlewaretoken: '{{ csrf_token }}', // Include CSRF token
            },
            success: function(response) {
                if (response.success) {
                    // Update the button text with the new performance value
                    $('.btn[data-kpi-name="' + kpiName + '"][data-annual-performance]').text(newPerformance);
                } else {
                    alert('Failed to update performance.');
                }

                // Close the modal
                $('#performanceModal').modal('hide');
            },
            error: function() {
                alert('An error occurred while updating performance.');
            },
        });
    });
});