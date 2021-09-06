removetheimage = document.getElementById("removetheimage");
uploadtheimage = document.getElementById("uploadtheimage");
caption_for_image = document.getElementById("caption_for_image");

$j(caption_for_image).hide();
let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
Dropzone.autoDiscover = false;

const md = new Dropzone("#my-dropzone", {
  url: window.location.origin + "/posts/post-image-upload/",
  parallelUploads: 5,
  maxFiles: 5,
  clickable: true,
  maxFilesize: 3,
  acceptedFiles: ".jpg,.png,.jpeg",
  autoProcessQueue: false,
  uploadMultiple: true,
  success: function (file, response) {
    removetheimage.setAttribute("post_pk", response.post_pk);
    uploadtheimage.setAttribute("sumbit_post", true);
    uploadtheimage.innerHTML = "Post To Soicalfy";
    removetheimage.innerHTML = '<i class="fas fa-ban"></i> Delete the post';
    $j(caption_for_image).show();
  },
});
$j("#uploadtheimage").click(function (e) {
  e.preventDefault();
  post_pk = removetheimage.getAttribute("post_pk");
  if (post_pk) {
    var caption_text = document.getElementById("caption_text").value.trim();
    var form_data=$j("#mytagegedfrom").serializeArray();
    var tag_user_str='';
    
     for (i in form_data) {
        tag_user_str=tag_user_str+form_data[i].value+','
      }
    console.log('taged user',form_data);

    if (caption_text.length) {
      $j.ajax({
        type: "POST",

        url: window.location.origin + "/posts/post-submit/",

        data: {
          csrfmiddlewaretoken: csrftoken,
          post_pk: post_pk,
          caption_text: caption_text,
          tag_usernames: tag_user_str,
        },

        success: function (response) {
          md.removeAllFiles();
          removetheimage.removeAttribute("post_pk");
          removetheimage.innerHTML =
            '<i class="fas fa-ban"></i> Remove all Images';
          uploadtheimage.innerHTML =
            '<i class="fas fa-upload"></i> Upload All Images';
          $j(caption_for_image).hide();
          $("#exampleModalLong").modal("hide");
          var url=window.location.origin + "/posts/explore/";
          window.location.replace(url)
          $("#postsucessmodel").modal("show");
        },
      });
    }else{
      document.getElementById("caption_text").focus();
    }

  } else {
    md.processQueue();
  }
});

$j("#removetheimage").click(function (e) {
  post_id = removetheimage.getAttribute("post_pk");
  e.preventDefault();
  md.removeAllFiles();
  if (post_id) {
    $j.ajax({
      type: "POST",

      url: window.location.origin + "/posts/delete-post/",

      data: {
        csrfmiddlewaretoken: csrftoken,
        post_id: post_id,
      },

      success: function (response) {
        removetheimage.removeAttribute("post_pk");
        removetheimage.innerHTML = '<i class="fas fa-ban"></i> Remove  Images';
        uploadtheimage.innerHTML =
          '<i class="fas fa-upload"></i> Upload  Images';
        $j(caption_for_image).hide();
      },
    });
  }
});
