$(document).ready(function(){
  $('form.cansubmit .vote').click(function() {

    let post_id = $(this).parents('form').children('input[name=post_id]').val();
    let csrf = $(this).parents('form').children('input[name=csrfmiddlewaretoken]').val();
    let vote = $(this).hasClass('fa-thumbs-up') ? 1 : -1

    // reset vote
    $(this).parent().find('i').removeClass('text-success text-danger');

    data = {
      "post_id": post_id,
      "vote": vote,
      'csrfmiddlewaretoken': csrf
    }

    $.ajax({
         type: "POST",
         url: "/tweets/vote/",
         data: data,
         dataType: "json",
         success: function(json) {

            let post_id = json['post_id'];
            let vote = json['vote'];

            input_element = $("input[value=" + post_id + "]");
            input_element.siblings('.up_count').text(json['num_up_votes']);
            input_element.siblings('.down_count').text(json['num_down_votes']);

            //mark new vote
            if (vote == 1)
              input_element.siblings('.fa-thumbs-up').addClass('text-success');

            if (vote == -1)
              input_element.siblings('.fa-thumbs-down').addClass('text-danger');
          },
    });

  });

});
