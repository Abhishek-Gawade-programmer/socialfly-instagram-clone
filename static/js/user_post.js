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
  acceptedFiles: ".jpg,.png,.jpeg,.gif",
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
    caption_text = document.getElementById("caption_text").value.trim();
    tag_usernames=document.getElementById('tag_friends').value+',';
    console.warn(tag_usernames);

    if (caption_text) {
        $j.ajax({
          type: "POST",

          url: window.location.origin + "/posts/post-submit/",

          data: {
            csrfmiddlewaretoken: csrftoken,
            post_pk: post_pk,
            caption_text: caption_text,
            tag_usernames_list:tag_usernames
          },

          success: function (response) {
            md.removeAllFiles();
            removetheimage.removeAttribute("post_pk");
            removetheimage.innerHTML =
              '<i class="fas fa-ban"></i> Remove all Images';
            uploadtheimage.innerHTML =
              '<i class="fas fa-upload"></i> Upload All Images';
            $j(caption_for_image).hide();
            $('#exampleModalLong').modal('hide');
            location.reload()
            $('#postsucessmodel').modal('show');
          },
        });
  };
  

  } 


  else {
    md.processQueue();
  }
});

$j("#removetheimage").click(function (e) {
  post_pk = removetheimage.getAttribute("post_pk");
  e.preventDefault();
  md.removeAllFiles();
  if (post_pk) {
    $j.ajax({
      type: "POST",

      url: window.location.origin + "/posts/delete-post/",

      data: {
        csrfmiddlewaretoken: csrftoken,
        post_pk: post_pk,
      },

      success: function (response) {
        removetheimage.removeAttribute("post_pk");
        removetheimage.innerHTML =
          '<i class="fas fa-ban"></i> Remove  Images';
        uploadtheimage.innerHTML =
          '<i class="fas fa-upload"></i> Upload  Images';
        $j(caption_for_image).hide();
      },
    });
  }
});
