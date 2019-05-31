$(document).ready(function(){
  $("form.cansubmit .vote").click(function() {

    const post_id = $(this).parents("form")
                          .children("input[name=post_id]").val();
    const csrf = $(this).parents("form")
                          .children("input[name=csrfmiddlewaretoken]").val();
    const vote = ($(this).hasClass("fa-thumbs-up") ? 1 : -1);

    // reset vote
    $(this).parent().find("i").removeClass("text-success text-danger");

    const data = {
      "post_id": post_id,
      "vote": vote,
      "csrfmiddlewaretoken": csrf
    };

    $.ajax({
         type: "POST",
         url: "/tweets/vote/",
         data: data,
         dataType: "json",
         success: function(json) {

            const ret_post_id = json.post_id;
            const new_vote = json.vote;

            const input_element = $("input[value=" + ret_post_id + "]");

            // set new vote counts
            input_element.siblings(".up_count").text(json.num_up_votes);
            input_element.siblings(".down_count").text(json.num_down_votes);

            //mark new vote
            if (new_vote === 1) {
              input_element.siblings(".fa-thumbs-up").addClass("text-success");
            }

            if (new_vote === -1) {
              input_element.siblings(".fa-thumbs-down").addClass("text-danger");
            }
          }
    });
  });
});
