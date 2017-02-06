$(document).ready(function(){

    // Prepare the tooltips on all buttons.
    $('[data-toggle="tooltip"]').tooltip();

    // Press complete button and complete the task.
    $('.complete-task').click(function() {

        var task_id = $(this).data("task-id")

        $.post(
            "/todo/task/",
            { "_method": "PUT",
              "task_id": task_id,
              "completed": "true",
              "csrfmiddlewaretoken": CSRF_TOKEN
            },
            function() { window.location.reload(true); }
        );
    });

    // Press task delete button and delete the task.
    $('.delete-task').click(function() {

        var task_id = $(this).data("task-id")

        $.post(
            "/todo/task/",
            { "_method": "DELETE",
              "task_id": task_id,
              "csrfmiddlewaretoken": CSRF_TOKEN
            },
            function() { window.location.reload(true); }
        );
    });


    // Toggle hide all task panels that are completed.
    $('#hide-completed').click(function() {
        $('.task-completed').toggle()
    });
});
