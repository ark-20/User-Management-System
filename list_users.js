$(document).ready(function() {
    function loadUsers() {

        const apiUrl = window.location.protocol + "//" + window.location.hostname + ":8001/users/search/";

        $.ajax({
            url: apiUrl,  // Correct: Absolute URL with port 8001 (or dynamically determined)
            type: "GET",
            dataType: "json",
            success: function(data) {
                const tableBody = $("#userTable tbody");
                tableBody.empty(); // Clear existing table rows

                if (data.length === 0) {
                    tableBody.append("<tr><td colspan='4'>No users found.</td></tr>");
                } else {
                    $.each(data, function(index, user) {
                        const row = $("<tr>");
                        row.append($("<td>").text(user.first_name));
                        row.append($("<td>").text(user.last_name));
                        row.append($("<td>").text(user.email));
                        row.append($("<td>").text(user.username));
                        tableBody.append(row);
                    });
                }
            },
            error: function(error) {
                console.error("Error fetching users:", error);
                $("#userTable tbody").append("<tr><td colspan='4'>Error fetching users.</td></tr>");
            }
        });
    }

    loadUsers(); // Load users when the page is ready

    $("#search").on("keyup", function() {
        const searchTerm = $(this).val();
        // Implement search filtering here (we'll add this later)
    });
});