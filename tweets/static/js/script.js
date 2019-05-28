
$(document).ready(function(){
  $('form.cansubmit .vote').click(function() {

    let post_id = $(this).parents('form').children('input[name=post_id]').val();
    let csrf = $(this).parents('form').children('input[name=csrfmiddlewaretoken]').val();
    let vote = $(this).hasClass('fa-thumbs-up') ? 1 : -1

    data = {
      "post_id": post_id,
      "vote": vote,
      'csrfmiddlewaretoken': csrf
    }

    $.ajax({
         type: "POST",
         url: "tweets/vote/",
         data: data,
         dataType: "json",
         success: function(json) {

            post_id = json['post_id'];

            $("input[value=" + post_id + "]").siblings('.up_count').text(json['num_up_votes']);
            $("input[value=" + post_id + "]").siblings('.down_count').text(json['num_down_votes']);

          },
          error: function(rs, e) {
              //  alert(rs.responseText);
          }
    });

  });

});
