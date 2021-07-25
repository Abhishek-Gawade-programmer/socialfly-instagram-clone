var spiner_box = document.getElementById("spiner_box");
var page = 1;
var empty_page = false;
var block_request = false;

function report_post_function(post_id) {
  let description_box = document.getElementById("description_box");
  let report_post_button = document.getElementById("report_post_button");
  report_post_button.addEventListener("click", (event) => {
    $j.ajax({
      type: "POST",

      url: window.location.origin + "/posts/report-post/",

      data: {
        csrfmiddlewaretoken: csrftoken,
        post_id: post_id,
        description: description_box.value,
      },
      success: function (response) {
          console.log('post_id'+post_id);
            $j('#post_id'+post_id).fadeOut(300, function() {
              $j('#post_id'+post_id).remove();
          });
          // $j("#postsucessmodel").modal("show");
      },
      error :function (response) {
          console.log('sth happen bad')
      },
    });
  });
}

// report_post_buttons.forEach((report_button) =>
//     report_button.addEventListener("click", (event) => {
//         post_id = report_button.getAttribute('post-id');
//         console.log(post_id)

// }));

$j(window).scroll(function () {
  var margin = $j(document).height() - $j(window).height() - 200;
  if (
    $j(window).scrollTop() > margin &&
    empty_page == false &&
    block_request == false
  ) {
    spiner_box.style.removeProperty("display");
    block_request = true;
    page += 1;
    $j.get("?page=" + page, function (data) {
      if (data == "") {
        empty_page = true;
      } else {
        block_request = false;
        $j("#feed").append(data);

        spiner_box.style.display = "none";
      }
    });
  }
});
