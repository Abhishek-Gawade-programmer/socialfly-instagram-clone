var spiner_box = document.getElementById("spiner_box");
var page = 1;
var empty_page = false;
var block_request = false;

function report_post_function(post_id) {
  let description_box = document.getElementById("description_box");
  let report_post_button = document.getElementById("report_post_button");
  let postsucessmodelLabel = document.getElementById("postsucessmodelLabel");
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
          postsucessmodelLabel.textContent='Thanks for feedback !!'
            $j('#post_id'+post_id).fadeOut(300, function() {
              $j('#post_id'+post_id).remove();
          });
          $("#postsucessmodel").modal("show");
      },
      error :function (response) {
          console.log('sth happen bad')
      },
    });
  });
};




function like_unlike_the_post (post_id) {
  let post=document.getElementById('post_id'+post_id);
  var like_unlike_frame=document.getElementById('postlike_unlike'+post_id)
  let icon = document.querySelector(".icon");



    $j.ajax({
      type: "POST",

      url: window.location.origin + "/posts/like-unlike-post/",

      data: {
        csrfmiddlewaretoken: csrftoken,
        post_id: post_id,
      },
      success: function (response) {


        if (response.action === 'like') {
               like_unlike_frame.innerHTML=` 
                   <svg aria-label="Unlike" class="_8-yf5 " fill="#ed4956" height="24" role="img" viewBox="0 0 48 48" width="24">
                        <path d="M34.6 3.1c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5s1.1-.2 1.6-.5c1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z">
                    
                           </path>
                   </svg>`

              icon.classList.add("like");
              post.classList.add("post_js");

              setTimeout(() => {
                icon.classList.remove("like");
                post.classList.remove("post_js");
              }, 1200);
    
        } else {

          like_unlike_frame.innerHTML=`
                  <svg aria-label="Like" class="_8-yf5 " fill="#262626" height="24" role="img" viewBox="0 0 48 48" width="24">
                    <path d="M34.6 6.1c5.7 0 10.4 5.2 10.4 11.5 0 6.8-5.9 11-11.5 16S25 41.3 24 41.9c-1.1-.7-4.7-4-9.5-8.3-5.7-5-11.5-9.2-11.5-16C3 11.3 7.7 6.1 13.4 6.1c4.2 0 6.5 2 8.1 4.3 1.9 2.6 2.2 3.9 2.5 3.9.3 0 .6-1.3 2.5-3.9 1.6-2.3 3.9-4.3 8.1-4.3m0-3c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5.6 0 1.1-.2 1.6-.5 1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z">
                    </path>
                 </svg>`
        
        }

         
      },
      error :function (response) {
          console.log('sth happen bad')
      },
    });
 
  
};




function delete_post_function(post_id) {
  let delete_post = document.getElementById("delete_post");
  console.log(delete_post)
  let postsucessmodelLabel = document.getElementById("postsucessmodelLabel");
  delete_post.addEventListener("click", (event) => {
    $j.ajax({
      type: "POST",

      url: window.location.origin + "/posts/delete-post/",

      data: {
        csrfmiddlewaretoken: csrftoken,
        post_id: post_id,
      },
      success: function (response) {
          console.log('post_id'+post_id);
          postsucessmodelLabel.textContent='Your post is deleted !!'
            $j('#post_id'+post_id).fadeOut(300, function() {
              $j('#post_id'+post_id).remove();
          });
          $("#postsucessmodel").modal("show");
      },
      error :function (response) {
          console.log('sth happen bad')
      },
    });
  });
};

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
